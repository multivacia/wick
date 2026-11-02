import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const parserSource=await readFile(new URL('../catalog/parser.js',import.meta.url),'utf8');
// Load the module without introducing a build step or third-party dependencies.
const {parseArtifact,tokenize,artifactId,PARSER_VERSION}=await import(
  'data:text/javascript;base64,'+Buffer.from(parserSource).toString('base64')
);
const jcl={name:'RFJ0001.JCL',library:'DEMO',content:
  "//RFJ0001 JOB (0000),'DEMO',CLASS=A\n//STEP050 EXEC PROC=RFP0001,PROGRAMA=RFB0002\n//SAIDA DD DSN=DEMO.CADASTRO.SAIDA,DISP=SHR"};
test('catalog v1 parser remains deterministic',()=>{
  assert.equal(PARSER_VERSION,2);
  assert.equal(artifactId('DEMO','rfj0001.jcl'),'DEMO::RFJ0001.JCL');
  assert.deepEqual(tokenize('Não existe STEP050'),['NAO','EXISTE','STEP050']);
});
test('JCL step -> PROC and parameter are evidence-backed, separate relationships',()=>{
  const record=parseArtifact(jcl);
  assert.ok(record.edges.some(x=>x.type==='EXEC_PROC'&&x.target==='RFP0001'&&x.line===2));
  assert.ok(record.edges.some(x=>x.type==='PARAM_PROGRAM'&&x.target==='RFB0002'&&x.line===2));
  assert.ok(record.postings.some(x=>x.term==='STEP050'&&x.line===2));
  assert.ok(record.postings.some(x=>x.term==='RFJ0001'&&x.line===0));
});
test('dynamic program references must remain unresolved',()=>{
  const record=parseArtifact({name:'RFP0001.PROC',library:'DEMO',
    content:'//RUN EXEC PGM=&PROGRAMA'});
  assert.deepEqual(record.edges.map(x=>[x.type,x.target,x.confidence]),
    [['EXEC_PGM','&PROGRAMA','unresolved']]);
});
test('COBOL COPY, literal CALL, and comments',()=>{
  const record=parseArtifact({name:'RFB0002.CBL',library:'DEMO',content:
    '      * COPY IGNORAR.\n       COPY CLIPAG.\n           CALL "OUTROPGM".'});
  assert.equal(record.edges.length,2);
  assert.ok(record.edges.some(x=>x.type==='COPY'&&x.target==='CLIPAG'&&x.line===2));
  assert.ok(record.edges.some(x=>x.type==='CALL_LITERAL'&&x.target==='OUTROPGM'&&x.line===3));
});
test('repeated words are indexed once per line',()=>{
  const record=parseArtifact({name:'T.TXT',library:'DEMO',content:'ABC ABC ABC'});
  assert.equal(record.postings.filter(x=>x.term==='ABC'&&x.line===1).length,1);
});

test('COBOL indirect CALL is never treated as confirmed dependency',()=>{
  const record=parseArtifact({name:'DYNAMIC.CBL',library:'DEMO',content:'           CALL PROG-VARIAVEL.'});
  assert.equal(record.edges.find(x=>x.type==='CALL_DYNAMIC')?.confidence,'unresolved');
});
