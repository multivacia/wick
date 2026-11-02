import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {classifyInventory} from '../catalog/sync.js';

const hash=s=>createHash('sha256').update(s).digest('hex');
const incoming=(name,content,library='DEMO')=>({id:library+'::'+name,name,library,content,hash:hash(content)});
const stored=(name,content,library='DEMO',parserVersion=1)=>({
  id:library+'::'+name,name,library,hash:hash(content),parserVersion
});
test('partial inventory never removes absent members',()=>{
  const plan=classifyInventory([incoming('NEW.JCL','//A JOB')],[stored('OLD.JCL','//B JOB')]);
  assert.equal(plan.counts.new,1);
  assert.equal(plan.counts.removed,0);
});
test('complete inventory proposes removal only inside explicit library',()=>{
  const plan=classifyInventory([incoming('NEW.JCL','//A JOB')],
    [stored('OLD.JCL','//B JOB'),stored('OTHER.JCL','//X','LOCAL')],
    {mode:'complete',library:'DEMO'});
  assert.deepEqual(plan.removed.map(x=>x.id),['DEMO::OLD.JCL']);
});
test('hash match with same parser means unchanged; changed contents mean modified',()=>{
  const a=incoming('RFJ0001.JCL','//STEP EXEC PROC=X');
  const b=incoming('RFP0001.PROC','//RUN EXEC PGM=ABC');
  const plan=classifyInventory([a,b],
    [stored(a.name,a.content),stored(b.name,'//RUN EXEC PGM=XYZ')]);
  assert.deepEqual(plan.counts,{new:0,modified:1,unchanged:1,removed:0,conflicts:0});
});
test('parser update reindexes unchanged source',()=>{
  const a=incoming('RFP0001.PROC','//RUN EXEC PGM=ABC');
  const old=stored(a.name,a.content,'DEMO',0);
  const plan=classifyInventory([a],[old]);
  assert.equal(plan.counts.modified,1);
});
test('duplicate identities are conflicts not last-write-wins',()=>{
  const item=incoming('FILE.CPY','01 FIELD PIC X.');
  const plan=classifyInventory([item,{...item,name:'file.cpy'}],[]);
  assert.equal(plan.counts.conflicts,1);
});
test('complete mode requires library and rejects cross-library input',()=>{
  assert.throws(()=>classifyInventory([],[],{mode:'complete'}),/biblioteca/);
  const plan=classifyInventory([incoming('X.JCL','', 'LOCAL')],[],
    {mode:'complete',library:'DEMO'});
  assert.equal(plan.counts.conflicts,1);
});
test('1562-file inventory only reprocesses changed components',()=>{
  const old=Array.from({length:1562},(_,i)=>stored('A'+i+'.JCL','SOURCE '+i));
  const changed=old.slice(0,1559).map((s,i)=>incoming(s.name,i<12?'UPDATED '+i:'SOURCE '+i));
  const added=Array.from({length:7},(_,i)=>incoming('NEW'+i+'.JCL','NEW '+i));
  const plan=classifyInventory([...changed,...added],old,{mode:'complete',library:'DEMO'});
  assert.deepEqual(plan.counts,{new:7,modified:12,unchanged:1547,removed:3,conflicts:0});
});
