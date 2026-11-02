import {parseArtifact, PARSER_VERSION} from './parser.js';
self.onmessage = event => {
  const {requestId, items} = event.data || {};
  try {
    if (!Array.isArray(items)) throw new Error('Invalid index request');
    const parsed = items.map(item => ({
      ...parseArtifact(item),
      hash:item.hash,
      parserVersion:PARSER_VERSION,
      indexedAt:new Date().toISOString()
    }));
    self.postMessage({requestId, parsed});
  } catch (error) {
    self.postMessage({requestId, error:String(error?.message || error)});
  }
};
