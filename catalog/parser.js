/**
 * MultivacIA 0.9: static parser and inverted-index extraction.
 * No network access; imported source is never executed.
 * Dynamic references are unresolved, never confirmed.
 */
export const PARSER_VERSION = 2;
export function normalizeName(value) {
  return String(value || '').trim().toUpperCase();
}
export function artifactId(library, name) {
  return normalizeName(library || 'LOCAL') + '::' + normalizeName(name);
}
export function tokenize(text) {
  const norm = String(text || '').toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  return (norm.match(/[A-Z0-9][A-Z0-9#$@_-]*/g) || []).filter(term => term.length > 1);
}
export function parseArtifact({name, library = 'LOCAL', content = ''}) {
  name = normalizeName(name);
  library = normalizeName(library);
  const id = artifactId(library, name);
  const ext = name.split('.').pop();
  const type = ({JCL:'JCL',PROC:'PROC',CBL:'COBOL',COB:'COBOL',CPY:'COPYBOOK',TXT:'TEXTO'})[ext] || 'OUTRO';
  const lines = String(content).replace(/\r\n?/g, '\n').split('\n');
  const postings = [];
  const edges = [];
  const unique = new Set();
  function addEdge(type, target, line, evidence) {
    target = normalizeName(target).replace(/[.,;]+$/, '');
    if (!target) return;
    const unresolved = type === 'CALL_DYNAMIC' || target.includes('&') || target.includes('
    const key = [type,target,line].join('|');
    if (unique.has(key)) return;
    unique.add(key);
    edges.push({sourceId:id,target,type,line,evidence:evidence.trim().slice(0,500),
      confidence:unresolved ? 'unresolved' : 'static'});
  }
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i], line = i+1, clean = raw.trim();
    if (/^\/\/\*/.test(clean) || /^\*>/.test(clean) || (type==='COBOL' && /^.{6}\*/.test(raw))) continue;
    for (const term of new Set(tokenize(raw))) postings.push({term,id,line});
    if (type==='JCL' || type==='PROC' || type==='TEXTO') {
      const execute = /\bEXEC\s+(?:PROC\s*=\s*([A-Z0-9_#$@&-]+)|PGM\s*=\s*([A-Z0-9_#$@&-]+)|([A-Z0-9_#$@&-]+))/i.exec(raw);
      if (execute) {
        if (execute[1]) addEdge('EXEC_PROC',execute[1],line,raw);
        else if (execute[2]) addEdge('EXEC_PGM',execute[2],line,raw);
        else if (execute[3]) addEdge('EXEC_PROC',execute[3],line,raw);
      }
      const ds = /\bDSN\s*=\s*([A-Z0-9_#$@&.-]+)/i.exec(raw);
      if (ds) addEdge('DD_DSN',ds[1],line,raw);
      const param = /\b(?:PROGRAMA|PROGRAM)\s*=\s*([A-Z0-9_#$@&-]+)/i.exec(raw);
      if (param && /\bEXEC\b/i.test(raw)) addEdge('PARAM_PROGRAM',param[1],line,raw);
    }
    if (type==='COBOL' || type==='COPYBOOK' || type==='TEXTO') {
      const copy = /\bCOPY\s+["']?([A-Z0-9_#$@&-]+)/ig;
      const call = /\bCALL\s+["']([A-Z0-9_#$@&-]+)["']/ig;
      for (const m of raw.matchAll(copy)) addEdge('COPY',m[1],line,raw);
      for (const m of raw.matchAll(call)) addEdge('CALL_LITERAL',m[1],line,raw);
      if (/\bCALL\s+[A-Z][A-Z0-9_-]*\b/i.test(raw) && !/\bCALL\s+["']/i.test(raw)) {
        const indirect = /\bCALL\s+([A-Z0-9_#$@&-]+)/i.exec(raw);
        if (indirect) addEdge('CALL_DYNAMIC',indirect[1],line,raw);
      }
    }
  }
  for (const term of new Set(tokenize(name))) postings.push({term,id,line:0});
  return {id,name,library,type,content:String(content),lineCount:lines.length,postings,edges};
}
 + '{');
    const key = [type,target,line].join('|');
    if (unique.has(key)) return;
    unique.add(key);
    edges.push({sourceId:id,target,type,line,evidence:evidence.trim().slice(0,500),
      confidence:unresolved ? 'unresolved' : 'static'});
  }
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i], line = i+1, clean = raw.trim();
    if (/^\/\/\*/.test(clean) || /^\*>/.test(clean) || (type==='COBOL' && /^.{6}\*/.test(raw))) continue;
    for (const term of new Set(tokenize(raw))) postings.push({term,id,line});
    if (type==='JCL' || type==='PROC' || type==='TEXTO') {
      const execute = /\bEXEC\s+(?:PROC\s*=\s*([A-Z0-9_#$@&-]+)|PGM\s*=\s*([A-Z0-9_#$@&-]+)|([A-Z0-9_#$@&-]+))/i.exec(raw);
      if (execute) {
        if (execute[1]) addEdge('EXEC_PROC',execute[1],line,raw);
        else if (execute[2]) addEdge('EXEC_PGM',execute[2],line,raw);
        else if (execute[3]) addEdge('EXEC_PROC',execute[3],line,raw);
      }
      const ds = /\bDSN\s*=\s*([A-Z0-9_#$@&.-]+)/i.exec(raw);
      if (ds) addEdge('DD_DSN',ds[1],line,raw);
      const param = /\b(?:PROGRAMA|PROGRAM)\s*=\s*([A-Z0-9_#$@&-]+)/i.exec(raw);
      if (param && /\bEXEC\b/i.test(raw)) addEdge('PARAM_PROGRAM',param[1],line,raw);
    }
    if (type==='COBOL' || type==='COPYBOOK' || type==='TEXTO') {
      const copy = /\bCOPY\s+["']?([A-Z0-9_#$@&-]+)/ig;
      const call = /\bCALL\s+["']([A-Z0-9_#$@&-]+)["']/ig;
      for (const m of raw.matchAll(copy)) addEdge('COPY',m[1],line,raw);
      for (const m of raw.matchAll(call)) addEdge('CALL_LITERAL',m[1],line,raw);
      if (/\bCALL\s+[A-Z][A-Z0-9_-]*\b/i.test(raw) && !/\bCALL\s+["']/i.test(raw)) {
        const indirect = /\bCALL\s+([A-Z0-9_#$@&-]+)/i.exec(raw);
        if (indirect) addEdge('CALL_DYNAMIC',indirect[1],line,raw);
      }
    }
  }
  for (const term of new Set(tokenize(name))) postings.push({term,id,line:0});
  return {id,name,library,type,content:String(content),lineCount:lines.length,postings,edges};
}
