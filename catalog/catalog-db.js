/**
 * MultivacIA 0.9 — IndexedDB catalog, postings and dependency edges.
 * Persistent per origin/browser; never synchronized to a server.
 * Only user-authorized, non-sensitive sources should be imported into this demo.
 */
import {artifactId, normalizeName, parseArtifact, tokenize, PARSER_VERSION} from './parser.js';

export const DATABASE_NAME = 'multivacia_catalog_v1';
export const DATABASE_VERSION = 1;
const IGNORED = new Set(['QUAIS','QUAL','ONDE','COMO','PARA','QUE','DOS','DAS','POR','UMA','UM','OS','AS','DE','DA','DO','THE','WHICH','WITH','FROM','AND','ARE']);
const DB_RANGE = () => IDBKeyRange;

function requestResult(request) {
  return new Promise((resolve,reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
function txDone(transaction) {
  return new Promise((resolve,reject) => {
    transaction.oncomplete = () => resolve();
    transaction.onerror = () => reject(transaction.error || new Error('IndexedDB transaction error'));
    transaction.onabort = () => reject(transaction.error || new Error('IndexedDB transaction aborted'));
  });
}
export async function openCatalog() {
  if (!('indexedDB' in globalThis)) throw new Error('IndexedDB indisponível neste navegador');
  const req = indexedDB.open(DATABASE_NAME,DATABASE_VERSION);
  req.onupgradeneeded = () => {
    const db = req.result;
    if (!db.objectStoreNames.contains('artifacts')) {
      const artifacts = db.createObjectStore('artifacts',{keyPath:'id'});
      artifacts.createIndex('by_name','name',{unique:false});
    }
    if (!db.objectStoreNames.contains('postings')) {
      const postings = db.createObjectStore('postings',{keyPath:['term','id','line']});
      postings.createIndex('by_term','term',{unique:false});
      postings.createIndex('by_id','id',{unique:false});
    }
    if (!db.objectStoreNames.contains('edges')) {
      const edges = db.createObjectStore('edges',{keyPath:['sourceId','type','target','line']});
      edges.createIndex('by_source','sourceId',{unique:false});
      edges.createIndex('by_target','target',{unique:false});
    }
    if (!db.objectStoreNames.contains('meta')) db.createObjectStore('meta',{keyPath:'key'});
  };
  const db = await requestResult(req);
  db.onversionchange = () => db.close();
  return new Catalog(db);
}
async function sha256(content) {
  if (!globalThis.crypto?.subtle) throw new Error('Web Crypto requer HTTPS/ambiente seguro');
  const bytes = new TextEncoder().encode(content);
  const digest = await crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2,'0')).join('');
}
function workerParse(items) {
  if (typeof Worker === 'undefined') return Promise.resolve(items.map(x => ({
    ...parseArtifact(x),hash:x.hash,parserVersion:PARSER_VERSION,indexedAt:new Date().toISOString()
  })));
  return new Promise((resolve,reject) => {
    let worker;
    try { worker = new Worker(new URL('./indexer.worker.js',import.meta.url),{type:'module'}); }
    catch (error) { reject(error); return; }
    const requestId = 'index-1';
    worker.onmessage = event => {
      if (event.data?.requestId !== requestId) return;
      worker.terminate();
      if (event.data.error) reject(new Error(event.data.error));
      else resolve(event.data.parsed);
    };
    worker.onerror = event => { worker.terminate();reject(new Error(event.message || 'Falha no worker de indexação')); };
    worker.postMessage({requestId,items});
  });
}
export class Catalog {
  constructor(db) { this.db = db; }
  close() { this.db.close(); }
  async get(id) {
    return requestResult(this.db.transaction('artifacts').objectStore('artifacts').get(id));
  }
  async getByName(name) {
    return requestResult(this.db.transaction('artifacts').objectStore('artifacts').index('by_name')
      .getAll(normalizeName(name)));
  }
  async stats() {
    const tx=this.db.transaction(['artifacts','postings','edges'],'readonly');
    const done=txDone(tx);
    const out=await Promise.all([
      requestResult(tx.objectStore('artifacts').count()),
      requestResult(tx.objectStore('postings').count()),
      requestResult(tx.objectStore('edges').count())
    ]);
    await done;
    return {artifacts:out[0],postings:out[1],edges:out[2],version:DATABASE_VERSION};
  }
  async replace(record) {
    const tx=this.db.transaction(['artifacts','postings','edges'],'readwrite');
    const done=txDone(tx);
    const postingStore=tx.objectStore('postings'), edgeStore=tx.objectStore('edges');
    // Read old compound keys BEFORE adding new postings/edges.
    const a=postingStore.index('by_id').getAllKeys(DB_RANGE().only(record.id));
    const b=edgeStore.index('by_source').getAllKeys(DB_RANGE().only(record.id));
    let aReady=false,bReady=false, aKeys=[],bKeys=[];
    function commit() {
      if (!aReady || !bReady) return;
      for(const key of aKeys) postingStore.delete(key);
      for(const key of bKeys) edgeStore.delete(key);
      for(const posting of record.postings) postingStore.put(posting);
      for(const edge of record.edges) edgeStore.put(edge);
      const {postings,edges,...meta}=record;
      tx.objectStore('artifacts').put(meta);
    }
    a.onsuccess=()=>{aKeys=a.result;aReady=true;commit();};
    b.onsuccess=()=>{bKeys=b.result;bReady=true;commit();};
    await done;
  }
  async clear() {
    const tx=this.db.transaction(['artifacts','postings','edges','meta'],'readwrite');
    const done=txDone(tx);
    for(const name of ['artifacts','postings','edges','meta']) tx.objectStore(name).clear();
    await done;
  }
  async remove(library,name) {
    const id=artifactId(library,name);
    const tx=this.db.transaction(['artifacts','postings','edges'],'readwrite');
    const done=txDone(tx);
    const p=tx.objectStore('postings'),e=tx.objectStore('edges');
    p.index('by_id').openKeyCursor(DB_RANGE().only(id)).onsuccess=event=>{
      const cursor=event.target.result;if(cursor){p.delete(cursor.primaryKey);cursor.continue();}
    };
    e.index('by_source').openKeyCursor(DB_RANGE().only(id)).onsuccess=event=>{
      const cursor=event.target.result;if(cursor){e.delete(cursor.primaryKey);cursor.continue();}
    };
    tx.objectStore('artifacts').delete(id);
    await done;
  }
  async index(items,{batchSize=20,onProgress}={}) {
    if(!Array.isArray(items)) throw new TypeError('index expects an array');
    const latest=new Map();
    for(const item of items) {
      if(typeof item?.name!=='string' || typeof item?.content!=='string') throw new TypeError('Cada artefato requer nome e texto');
      if(item.content.length>1500000) throw new RangeError('Artefato excede 1,5 milhão de caracteres');
      const name=normalizeName(item.name), library=normalizeName(item.library||'DEMO');
      latest.set(artifactId(library,name),{name,library,content:item.content});
    }
    const changed=[];
    for (const item of latest.values()) {
      const hash=await sha256(item.content);
      const stored=await this.get(artifactId(item.library,item.name));
      if(!stored || stored.hash!==hash || stored.parserVersion!==PARSER_VERSION) changed.push({...item,hash});
    }
    let indexed=0;
    for(let i=0;i<changed.length;i+=batchSize) {
      const group=changed.slice(i,i+batchSize);
      const parsed=await workerParse(group);
      for (const record of parsed) { await this.replace(record);indexed++; }
      onProgress?.({done:indexed,total:changed.length});
    }
    return {seen:latest.size,indexed,unchanged:latest.size-indexed};
  }
  async search(query,{limit=30}={}) {
    const tokens=[...new Set(tokenize(query).filter(t=>!IGNORED.has(t)))].slice(0,8);
    if(!tokens.length) return [];
    const score=new Map();
    const tx=this.db.transaction('postings','readonly');
    const done=txDone(tx);
    const requests=tokens.map(term=>requestResult(tx.objectStore('postings').index('by_term')
      .getAll(DB_RANGE().only(term))));
    const hits=await Promise.all(requests);
    await done;
    hits.forEach((rows,i)=>{
      for(const row of rows){
        let item=score.get(row.id);
        if(!item){item={id:row.id, terms:new Set(),lines:new Set()};score.set(row.id,item);}
        item.terms.add(tokens[i]);
        if(row.line>0 && item.lines.size<6)item.lines.add(row.line);
      }
    });
    const ranked=[...score.values()].filter(item=>item.terms.size===tokens.length)
      .sort((a,b)=>b.terms.size-a.terms.size||a.id.localeCompare(b.id)).slice(0,Math.max(1,Math.min(100,limit)));
    const records=await Promise.all(ranked.map(item=>this.get(item.id)));
    return ranked.map((item,i)=>{
      const record=records[i], lines=record.content.replace(/\r\n?/g,'\n').split('\n');
      return {id:item.id,name:record.name,library:record.library,type:record.type,
        matches:[...item.lines].sort((a,b)=>a-b).map(line=>({line,text:lines[line-1]?.trim().slice(0,220)||''}))};
    });
  }
  async relationships(name,library='DEMO') {
    const id=artifactId(library,name);
    const tx=this.db.transaction('edges','readonly');
    const done=txDone(tx);
    const source=tx.objectStore('edges').index('by_source').getAll(DB_RANGE().only(id));
    const base=normalizeName(name).replace(/\.[^.]+$/,'');
    const target=tx.objectStore('edges').index('by_target').getAll(DB_RANGE().only(base));
    const [outgoing,incoming]=await Promise.all([requestResult(source),requestResult(target)]);
    await done;
    return {outgoing,incoming};
  }
}
