import {openCatalog} from './catalog-db.js';
import {prepareInventory,applyInventory} from './sync.js';

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

/* 0.9B: explicit preview -> apply. The old one-click incremental button stays
 * for backwards compatibility, but NEVER infers removals. */
const syncPanel=document.createElement('section');
syncPanel.className='catalog-hit';
syncPanel.setAttribute('aria-label','Sincronização de inventário');
syncPanel.innerHTML=[
  '<strong>ATUALIZAÇÃO INCREMENTAL · PRÉVIA</strong>',
  '<small>Parcial: inclui e atualiza, nunca exclui. Completo: compara somente a biblioteca selecionada; ausências viram candidatas à remoção.</small>',
  '<div class="catalog-controls">',
  '<label>Inventário <select id="syncMode"><option value="partial">PARCIAL (SEGURO)</option><option value="complete">COMPLETO</option></select></label>',
  '<label>Biblioteca <select id="syncLibrary"><option value="DEMO">DEMO</option><option value="LOCAL">LOCAL</option></select></label>',
  '</div>',
  '<div class="catalog-controls"><button id="syncPreview" type="button">1. GERAR PRÉVIA</button>',
  '<button id="syncApply" type="button" disabled>2. APLICAR ALTERAÇÕES</button></div>',
  '<div id="syncReport" class="info" aria-live="polite">Nenhuma prévia gerada.</div>',
  '<div id="syncDetails" class="catalog-sync-details"></div>'
].join('');
$('catalogStats').insertAdjacentElement('afterend',syncPanel);
const syncMode=$('syncMode'),syncLibrary=$('syncLibrary');
let syncPlan=null;
function discardPreview(){
  syncPlan=null;$('syncApply').disabled=true;
  $('syncReport').textContent='Altere o inventário e gere uma nova prévia.';
  $('syncDetails').replaceChildren();
}
syncMode.addEventListener('change',discardPreview);
syncLibrary.addEventListener('change',discardPreview);
$('syncPreview').addEventListener('click',async()=>{
  if(catalog.busy)return;
  catalog.busy=true;$('syncPreview').disabled=true;
  discardPreview();
  try{
    const fn=window.multivaciaCatalogSources;
    if(typeof fn!=='function')throw new Error('Fonte de arquivos indisponível');
    const mode=syncMode.value,library=syncLibrary.value;
    const sources=fn();
    const items=mode==='complete'?sources.filter(x=>x.library===library):sources;
    if(items.some(x=>x.library!=='DEMO')){
      if(!window.confirm('A prévia calcula hashes de fontes importados. A aplicação salvará o texto integral no IndexedDB deste navegador. Não utilize código corporativo neste site público. Continuar?'))return;
    }
    syncPlan=await prepareInventory(await ready(),items,{mode,library});
    const n=syncPlan.counts;
    $('syncReport').textContent=
      'Novos: '+n.new+' · Alterados: '+n.modified+' · Inalterados: '+n.unchanged+
      ' · Candidatos à remoção: '+n.removed+' · Conflitos: '+n.conflicts;
    const lines=[
      ...syncPlan.entries.filter(x=>x.state!=='unchanged').map(x=>x.state.toUpperCase()+' · '+x.id),
      ...syncPlan.removed.map(x=>'REMOVER? · '+x.id),
      ...syncPlan.conflicts.map(x=>'CONFLITO · '+x.id+' · '+x.reason)
    ];
    const output=$('syncDetails');output.replaceChildren();
    const pre=document.createElement('pre');pre.style.minHeight='0';
    pre.textContent=lines.slice(0,80).join('\n')+
      (lines.length>80?'\n... e mais '+(lines.length-80)+' registros':'')||
      'Nenhuma inclusão, alteração ou exclusão identificada.';
    output.append(pre);
    $('syncApply').disabled=n.conflicts>0 || n.new+n.modified+n.removed===0;
    if(mode==='complete' && n.removed){
      status('Prévia gerada. Revise os candidatos à remoção e confirme antes de aplicar.');
    }else status('Prévia gerada sem modificar o catálogo.');
  }catch(error){status('Prévia: '+String(error.message||error),true);discardPreview();}
  finally{catalog.busy=false;$('syncPreview').disabled=false;}
});
$('syncApply').addEventListener('click',async()=>{
  if(catalog.busy||!syncPlan)return;
  const plan=syncPlan;
  const n=plan.counts;
  const desc='Aplicar '+n.new+' novos, '+n.modified+' alterados e '+n.removed+' remoções? Esta operação modifica a base local deste navegador.';
  if(!window.confirm(desc))return;
  if(n.removed && !window.confirm('ATENÇÃO: '+n.removed+' componentes ausentes serão removidos da biblioteca '+plan.library+'. Você confirmou que o inventário é COMPLETO e confiável?'))return;
  catalog.busy=true;$('syncApply').disabled=true;$('syncPreview').disabled=true;
  try {
    const result=await applyInventory(await ready(),plan);
    syncPlan=null;
    $('syncReport').textContent='Aplicado: '+result.applied+' indexados · '+result.removed+' removidos · '+result.unchanged+' inalterados.';
    $('syncDetails').replaceChildren();$('catalogResults').replaceChildren();
    await refresh();
    status('Sincronização local aplicada de forma atômica.');
  }catch(error){
    const quota=error?.name==='QuotaExceededError';
    status(quota?'Espaço local insuficiente: transação cancelada; preserve sua fonte e libere armazenamento.':
      'Sincronização não aplicada: '+String(error.message||error),true);
    discardPreview();
  }finally{catalog.busy=false;$('syncPreview').disabled=false;}
});
