# MultivacIA 0.9 — arquitetura do catálogo indexado

## Objetivo

Evitar reler e reinterpretar todos os fontes a cada consulta. A análise é feita na indexação; pesquisas posteriores consultam o banco estruturado.

A implementação atual é **uma prévia isolada na branch `feature/catalogo-indexado-0.9`**. Não há integração com z/OS ou serviços externos, nem importação de fontes corporativos.

## Componentes

| Componente | Papel |
| --- | --- |
| `catalog/parser.js` | Parser determinístico JCL/PROC/COBOL/COPYBOOK; extrai tokens, linhas e dependências com evidências |
| `catalog/indexer.worker.js` | Executa o parser fora da thread da interface |
| `catalog/catalog-db.js` | Mantém catálogo persistente, índices, atualização incremental e consultas |
| `catalog/ui.js` | Operações da aba CATÁLOGO; indexação explícita e pesquisa |
| IndexedDB | Armazenamento local por navegador e origem HTTPS |

## Schema do IndexedDB (`multivacia_catalog_v1`, versão 1)

**artifacts** (PK `id = BIBLIOTECA::NOME`): `name`, `library`, `type`, `content`, `lineCount`, `hash` SHA-256, `parserVersion`, `indexedAt`. Índice secundário `by_name`.

**postings** (PK composta `[term,id,line]`): índice invertido das ocorrências; `by_term` permite busca textual sem varredura dos fontes, `by_id` permite invalidar termos do artefato atualizado.

**edges** (PK composta `[sourceId,type,target,line]`): ligações declaradas e evidência da linha de origem. Índices `by_source` e `by_target`, permitindo consulta no sentido direto e inverso. Atributo `confidence`: `static` ou `unresolved`.

**meta** (PK `key`): reservado para a evolução de metadados de migração e execução. A versão do schema fica sob controle do IndexedDB; a versão do parser é armazenada em cada artefato.

## Fluxos

1. O usuário abre a aba **CATÁLOGO** e clica **INDEXAR ARTEFATOS CARREGADOS**. Não persistimos automaticamente arquivos importados.
2. O banco compara `SHA-256` e versão do parser dos artefatos com os registros existentes. Iguais são ignorados.
3. Somente os modificados passam pelo Web Worker; o parser gera ocorrências e arestas.
4. Cada atualização é atômica por artefato: remove ocorrências e arestas anteriores e grava os novos registros na mesma transação.
5. Uma busca consulta `postings.by_term`, encontra os IDs e recupera apenas os artefatos e linhas relacionados.
6. O usuário pode **LIMPAR ÍNDICE LOCAL**; isso remove as informações das três tabelas do catálogo, mas não apaga os documentos carregados na sessão atual.

## Semântica do grafo

- `EXEC_PROC`: a linha JCL/PROC identifica uma chamada de procedimento.
- `EXEC_PGM`: programa do `EXEC PGM=`, que pode ser dinâmico (`&PROGRAMA`).
- `PARAM_PROGRAM`: valor de um parâmetro `PROGRAMA=` em um EXEC. Não prova por si só execução do programa pelo procedimento.
- `COPY` e `CALL_LITERAL`: dependências reconhecíveis pela sintaxe.
- `CALL_DYNAMIC`: o programa chamado é variável/indireto.
- `DD_DSN`: associação de um DD a um dataset, não dependência de programa.

Relações dinâmicas, macros e construções não reconhecidas exigem validação posterior. A versão 1.0 deverá resolver encadeamentos com contexto, exibir o grafo e produzir análise de impacto rastreável.

## Segurança e privacidade

- O repositório e o GitHub Pages da demonstração são **públicos**. Só utilizar fontes fictícios ou explicitamente autorizados.
- IndexedDB armazena inclusive o texto completo no dispositivo do usuário. NÃO constitui armazenamento corporativo protegido, não é sincronizado e pode ser removido pelo navegador.
- A aplicação não faz `fetch` ou upload do catálogo; a voz do navegador é funcionalidade separada e pode usar serviços externos do navegador.
- A atualização da base só ocorre com clique explícito; ao tentar indexar arquivos importados, a interface solicita confirmação.
- Código corporativo exigirá ambiente interno autorizado, autenticação, segregação, criptografia e auditoria; não será integrado ao GitHub Pages público.

## Sincronização incremental 0.9B/C (implementação em homologação)

- `catalog/sync.js` classifica fontes por biblioteca e hash: novos, alterados, inalterados, candidatos à exclusão e identidades em conflito.
- Inventário **PARCIAL** é o padrão e nunca remove ausentes. Inventário **COMPLETO** exige seleção expressa da biblioteca `DEMO` ou `LOCAL`; todo arquivo ausente no escopo vira candidato à remoção (exige duas confirmações).
- A tela oferece **GERAR PRÉVIA** antes de **APLICAR ALTERAÇÕES**. Arquivos com identidades duplicadas/bibliotecas incompatíveis bloqueiam a publicação.
- A análise dos componentes alterados é concluída antes da abertura da transação; uma transação IndexedDB com `artifacts`, `postings`, `edges` e `meta` aplica o lote inteiro. Leitura e checagem de hash/versão anteriores impedem publicar uma prévia obsoleta sem erro.
- Uma cópia **exata do estado anterior dos componentes afetados**, incluindo fonte, ocorrências e relações, fica em `meta.sync:undo` junto da publicação, para **desfazer apenas a última sincronização incremental**. Não equivale a uma estratégia definitiva de backup nem ao histórico ilimitado de snapshots.
- `meta.sync:last` e `meta.sync:run:<id>` registram hora, modo, biblioteca e contagens; **LIMPAR ÍNDICE LOCAL** também remove esse histórico e o checkpoint de reversão.
- O navegador pode negar a operação por quota e toda a transação deverá falhar sem publicação parcial. É necessário homologar esse comportamento em navegadores reais.
- O teste de 1.562 arquivos é de **classificação sintética**; não é uma medição de performance do IndexedDB ou do parser em 1.562 fontes.

## Limitações e próximos incrementos

- A pesquisa inicial é baseada em termos exatos normalizados, com `AND` entre termos significativos. Busca semântica e perguntas livres serão etapa posterior.
- O parser cobre um subconjunto das variantes JCL/COBOL; condicionais, substituições, macros e resoluções interbibliotecas precisam de parsers especializados.
- A interface atual mostra resultados e relações textuais, **não** um grafo visual. Grafo e impacto visual: 1.0.
- Ainda falta importar inventários com proveniência formal, reconhecer renomeações, medir armazenamento, testar interrupções no IndexedDB real e oferecer histórico completo de múltiplos snapshots.
- Processamento por lotes de 20 artefatos; a latência e o consumo real em bases maiores devem ser medidos em dispositivo e navegador.
- O armazenamento e seus limites de quota são definidos pelo navegador, sem garantia de permanência.

## Testes

```sh
node --test tests/*.test.mjs
```

Validações previstas para homologação: primeira indexação, segunda indexação com zero reprocessamentos, atualização de um fonte, limpeza, busca e consulta de relações após recarregar o navegador.
