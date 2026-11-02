/**
 * MultivacIA 0.9B: deliberate, locally atomic inventory synchronization.
 * No upload/network traffic. Absence in partial inventories never implies deletion.
 */
import {artifactId, normalizeName, parseArtifact, PARSER_VERSION} from './parser.js';

const validName = /^[A-Z0-9_#$@.\-]{1,200}$/;
const on = request => new Promise((resolve,reject) => {
  request.onsuccess = () => resolve(request.result);
  request.onerror = () => reject(request.error);
});
const settled = tx => new Promise((resolve,reject) => {
  tx.oncomplete = () => resolve();
  tx.onerror = () => reject(tx.error || new Error('Erro IndexedDB'));
  tx.onabort = () => reject(tx.error || new Error('Sincronização abortada'));
});

async function digest(content) {
  if (!globalThis.crypto?.subtle) throw new Error('SHA-256 requer HTTPS ou localhost');
  const hash = await crypto.subtle.digest('SHA-256',new TextEncoder().encode(content));
  return [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2,'0')).join('');
}

/**
 * Pure comparison: incoming entries MUST already have SHA-256 hashes.
 * A complete inventory requires a single explicit library scope.
 */
export function classifyInventory(incoming,stored,{mode='partial',library}={}) {
  if (mode!=='partial' && mode!=='complete') throw new Error('Modo de inventário inválido');
  const scope = normalizeName(library);
  if (mode==='complete' && !validName.test(scope)) throw new Error('Inventário completo exige biblioteca explícita');
  const old = new Map(stored.map(x => [x.id,x]));
  const seen = new Set();
  const entries = [], conflicts = [];
  for (const entry of incoming) {
    const name=normalizeName(entry.name), lib=normalizeName(entry.library);
    if (!validName.test(name) || !validName.test(lib) || typeof entry.content!=='string' ||
        !/^[a-f0-9]{64}$/.test(entry.hash||'')) {
      conflicts.push({id:entry.id||name,reason:'Componente, biblioteca, conteúdo ou hash inválido'});continue;
    }
    const id=artifactId(lib,name);
    if (seen.has(id)) { conflicts.push({id,reason:'Identidade repetida no lote'});continue; }
    seen.add(id);
    if (mode==='complete' && lib!==scope) {
      conflicts.push({id,reason:'Arquivo fora do escopo da biblioteca '+scope});continue;
    }
    const previous=old.get(id);
    const state=!previous?'new':previous.hash!==entry.hash || previous.parserVersion!==PARSER_VERSION?'modified':'unchanged';
    entries.push({...entry,id,name,library:lib,state,
      expectedHash:previous?.hash??null,expectedParser:previous?.parserVersion??null});
  }
  const removed=[];
  if(mode==='complete')for(const previous of stored) {
    if (normalizeName(previous.library)===scope && !seen.has(previous.id)) {
      removed.push({id:previous.id,name:previous.name,library:previous.library,state:'removed',
        expectedHash:previous.hash,expectedParser:previous.parserVersion});
    }
  }
  return {mode,library:scope,entries,removed,conflicts,counts:{
    new:entries.filter(x=>x.state==='new').length,
    modified:entries.filter(x=>x.state==='modified').length,
    unchanged:entries.filter(x=>x.state==='unchanged').length,
    removed:removed.length,conflicts:conflicts.length}};
}

export async function prepareInventory(catalog,items,options={}) {
  if(!Array.isArray(items))throw new TypeError('Inventário deve ser um conjunto de arquivos');
  if(items.length>10000)throw new RangeError('Inventário excede limite de 10 mil arquivos');
  const incoming=[];
  for(const item of items) {
    if(typeof item?.name!=='string' || typeof item?.content!=='string')
      throw new TypeError('Cada arquivo precisa ter nome e conteúdo');
    if(item.content.length>1500000)throw new RangeError('Fonte excede limite de 1,5 milhão de caracteres');
    incoming.push({...item,hash:await digest(item.content)});
  }
  const tx=catalog.db.transaction('artifacts','readonly');
  const old=await on(tx.objectStore('artifacts').getAll());
  const plan=classifyInventory(incoming,old,options);
  return {...plan,createdAt:new Date().toISOString()};
}

function parseInWorker(items) {
  if(!items.length)return Promise.resolve([]);
  if(typeof Worker==='undefined')return Promise.resolve(items.map(item=>({
    ...parseArtifact(item),hash:item.hash,parserVersion:PARSER_VERSION,indexedAt:new Date().toISOString()
  })));
  return new Promise((resolve,reject)=>{
    const worker=new Worker(new URL('./indexer.worker.js',import.meta.url),{type:'module'});
    worker.onmessage=({data})=>{
      if(data?.requestId!=='sync')return;
      worker.terminate();
      if(data.error)reject(new Error(data.error));else resolve(data.parsed);
    };
    worker.onerror=e=>{worker.terminate();reject(new Error(e.message||'Falha no indexador'));};
    worker.postMessage({requestId:'sync',items});
  });
}

/**
 * Validate and parse BEFORE opening the write transaction.
 * All writes (including deletions and audit metadata) commit together or not at all.
 * Optimistic hash/version checks prevent stale previews overwriting another tab's edits.
 */
export async function applyInventory(catalog,plan) {
  if(plan.conflicts.length)throw new Error('Resolva os conflitos antes de publicar o inventário');
  const changed=plan.entries.filter(e=>e.state!=='unchanged');
  const targets=[...changed,...plan.removed];
  if(!targets.length)return {applied:0,removed:0,unchanged:plan.counts.unchanged};
  for(const item of changed) {
    if(await digest(item.content)!==item.hash)throw new Error('Fonte alterado após a prévia: '+item.id);
  }
  const parsed=await parseInWorker(changed);
  if(parsed.length!==changed.length)throw new Error('Indexador retornou quantidade inconsistente');
  for(let i=0;i<parsed.length;i++) {
    const r=parsed[i];
    if(r.id!==changed[i].id || r.hash!==changed[i].hash || !Array.isArray(r.postings) ||
       !Array.isArray(r.edges))throw new Error('Resultado inválido do parser: '+changed[i].id);
  }

  const tx=catalog.db.transaction(['artifacts','postings','edges','meta'],'readwrite');
  const finished=settled(tx);
  const a=tx.objectStore('artifacts'),p=tx.objectStore('postings'),e=tx.objectStore('edges');
  const staged=[];
  let outstanding=targets.length*3, aborted=false;
  const abort=e=>{if(!aborted){aborted=true;tx.abort();}};
  const finishRead=()=>{
    outstanding--;
    if(outstanding!==0 || aborted)return;
    for(const row of staged) {
      if((row.current?.hash??null)!==(row.item.expectedHash??null) ||
         (row.current?.parserVersion??null)!==(row.item.expectedParser??null)) {
        abort();return;
      }
    }
    for(const row of staged) {
      for(const key of row.postingKeys)p.delete(key);
      for(const key of row.edgeKeys)e.delete(key);
      a.delete(row.item.id);
    }
    for(const record of parsed) {
      for(const posting of record.postings)p.put(posting);
      for(const edge of record.edges)e.put(edge);
      const {postings,edges,...metadata}=record;
      a.put(metadata);
    }
    const runId=(crypto.randomUUID?.()||String(Date.now()));
    const audit={key:'sync:last',runId,finishedAt:new Date().toISOString(),
      mode:plan.mode,library:plan.library,counts:plan.counts};
    tx.objectStore('meta').put(audit);
    tx.objectStore('meta').put({...audit,key:'sync:run:'+runId});
  };
  for(const item of targets) {
    const row={item,postingKeys:[],edgeKeys:[],current:null};
    staged.push(row);
    a.get(item.id).onsuccess=ev=>{row.current=ev.target.result;finishRead();};
    p.index('by_id').getAllKeys(IDBKeyRange.only(item.id)).onsuccess=ev=>{
      row.postingKeys=ev.target.result;finishRead();
    };
    e.index('by_source').getAllKeys(IDBKeyRange.only(item.id)).onsuccess=ev=>{
      row.edgeKeys=ev.target.result;finishRead();
    };
  }
  await finished;
  return {applied:changed.length,removed:plan.removed.length,unchanged:plan.counts.unchanged};
}
