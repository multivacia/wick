import {openCatalog} from './catalog-db.js';

const $ = id => document.getElementById(id);
const catalog = {db:null,busy:false};
const tr = (pt,en) => $('language').value==='pt-BR' ? pt : en;
function status(text,error=false) {
  $('catalogStatus').textContent=text;
  $('catalogStatus').className=error?'warn':'info';
}
async function ready() {
  if(!catalog.db) catalog.db=await openCatalog();
  return catalog.db;
}
async function refresh() {
  const db=await ready(), count=await db.stats();
  $('catalogStats').textContent=tr(
    'Catálogo local: '+count.artifacts+' artefatos · '+count.postings+' ocorrências · '+count.edges+' relações',
    'Local catalog: '+count.artifacts+' artifacts · '+count.postings+' postings · '+count.edges+' relations');
}
function resultNode(record) {
  const outer=document.createElement('article');
  outer.className='catalog-hit';
  const title=document.createElement('strong');
  title.textContent=record.name+' · '+record.type;
  outer.append(title);
  const lib=document.createElement('small');
  lib.textContent=record.library+' · '+record.id;
  outer.append(lib);
  if(record.matches.length){
    const list=document.createElement('div');
    for (const match of record.matches) {
      const line=document.createElement('pre');
      line.textContent='L'+match.line+': '+match.text;
      list.append(line);
    }
    outer.append(list);
  }
  const relationButton=document.createElement('button');
  relationButton.type='button';
  relationButton.textContent=tr('VER REFERÊNCIAS','SHOW REFERENCES');
  relationButton.addEventListener('click',async()=>{
    relationButton.disabled=true;
    try{
      const links=await (await ready()).relationships(record.name,record.library);
      const details=document.createElement('pre');
      details.textContent=[
        ...links.outgoing.map(e=>'→ '+e.type+' '+e.target+' · L'+e.line+' ['+e.confidence+']'),
        ...links.incoming.map(e=>'← '+e.sourceId+' · '+e.type+' · L'+e.line+' ['+e.confidence+']')
      ].join('\n')||tr('Nenhuma relação identificada.','No identified relationships.');
      outer.append(details);
    }catch(e){status(String(e.message||e),true);}
  },{once:true});
  outer.append(relationButton);
  return outer;
}
async function runSearch() {
  if(catalog.busy)return;
  catalog.busy=true;$('catalogSearchButton').disabled=true;
  try {
    const query=$('catalogQuery').value.trim();
    const results=await (await ready()).search(query);
    const target=$('catalogResults');
    target.replaceChildren();
    for(const result of results)target.append(resultNode(result));
    status(results.length
      ? tr(results.length+' artefatos encontrados.',results.length+' artifacts found.')
      : tr('Nenhum resultado. Use nome, STEP ou campo do componente.','No matches. Search for a component name, STEP, or field.'));
  }catch(e){status(String(e?.message||e),true);}
  finally{catalog.busy=false;$('catalogSearchButton').disabled=false;}
}
$('catalogSearchForm').addEventListener('submit',e=>{e.preventDefault();runSearch();});
$('catalogIndex').addEventListener('click',async()=>{
  if(catalog.busy)return;
  const source=window.multivaciaCatalogSources;
  if(typeof source!=='function'){status(tr('Artefatos indisponíveis.','No available artifacts.'),true);return;}
  catalog.busy=true;$('catalogIndex').disabled=true;
  try{
    const items=source();
    if(!items.every(item=>item.library==='DEMO')){
      const approved=window.confirm(tr(
        'Você importou outros arquivos. Deseja armazenar seu conteúdo no banco local deste navegador? Não use código corporativo neste GitHub Pages público.',
        'You imported other files. Save their source in this browser local catalog? Do not use corporate code on public GitHub Pages.'));
      if(!approved){status(tr('Indexação cancelada.','Indexing cancelled.'));return;}
    }
    status(tr('Indexando artefatos localmente...','Indexing artifacts locally...'));
    const indexed=await(await ready()).index(items,{onProgress:p=>status(tr(
      'Processados '+p.done+' de '+p.total+' arquivos alterados.',
      'Processed '+p.done+' of '+p.total+' changed files.'))});
    status(tr(
      'Indexação concluída: '+indexed.indexed+' atualizados, '+indexed.unchanged+' inalterados.',
      'Index complete: '+indexed.indexed+' updated, '+indexed.unchanged+' unchanged.'));
    await refresh();
  }catch(e){status(String(e?.message||e),true);}
  finally{catalog.busy=false;$('catalogIndex').disabled=false;}
});
$('catalogClear').addEventListener('click',async()=>{
  if(catalog.busy)return;
  if(!window.confirm(tr('Apagar o catálogo local deste navegador?','Delete the catalog on this browser?')))return;
  catalog.busy=true;$('catalogClear').disabled=true;
  try{
    await(await ready()).clear();$('catalogResults').replaceChildren();
    await refresh();status(tr('Catálogo local apagado.','Local catalog cleared.'));
  }catch(e){status(String(e?.message||e),true);}
  finally{catalog.busy=false;$('catalogClear').disabled=false;}
});
refresh().then(()=>status(tr('Pronto. Indexe os exemplos para começar.','Ready. Index the samples to start.')))
 .catch(error=>status('IndexedDB: '+String(error?.message||error),true));
