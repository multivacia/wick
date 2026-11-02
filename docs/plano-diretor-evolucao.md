# Plano Diretor de Evolução — MultivacIA

**Status:** proposta de planejamento (não autoriza implementação, merge nem deploy).  
**Atualizado:** 2026-11-02.  
**Repositório:** multivacia/wick.  
**Referência técnica:** [Arquitetura do catálogo 0.9](arquitetura-catalogo-09.md) e PR #148.  
**Publicação:** main = versão pública 0.8.1. A 0.9 está em branch de trabalho, sem merge.

## 1. Objetivos e princípios

1. Consultar índices pré-calculados, em vez de reler todos os fontes por pergunta.
2. Identificar com precisão componentes novos, alterados, inalterados, renomeados e removidos.
3. Manter evidência de origem (biblioteca, componente, linha e versão) para cada afirmação técnica.
4. Diferenciar referências comprovadas, parâmetros e dependências dinâmicas/não resolvidas.
5. Garantir atualização recuperável e auditável: não perder um catálogo válido por uma importação incompleta.
6. Entregar incrementos pequenos com critérios de aprovação objetivos.
7. Usar **somente artefatos fictícios ou autorizados** na demonstração pública. Não conectar fontes bancários ou corporativos ao GitHub Pages.
8. Alterações apenas no repositório multivacia/wick e branch de trabalho; sem tocar em SGP+, VPS ou outros repositórios.

## 2. Glossário e modelo de dados

- **Origem:** de onde veio um conjunto de arquivos (ex.: pacote demonstrativo, biblioteca local autorizada, conector interno futuro).
- **Inventário (manifest):** relação de arquivos de uma origem, escopo, tipo de varredura (completa/parcial) e versão/captura.
- **Identidade de componente:** \`origem + biblioteca + nome + tipo\` com regras explícitas para homônimos. Na implementação inicial: \`biblioteca::nome\`; a migração da chave requer planejamento.
- **Revisão de componente:** hash dos bytes/conteúdo original, data de captura, versão do parser, estado de validação e proveniência.
- **Ocorrência (posting):** termo, componente, linha, opcionalmente coluna/trecho.
- **Relação (edge):** origem, alvo, tipo, evidência, linha, escopo de biblioteca, confiança e situação de resolução.
- **Snapshot:** visão consistente de todos os componentes e relações aprovados em uma sincronização.
- **Execução de sincronização:** ID, origem, início/fim, inventário, contagens, erros, resultados e decisão.
- **Mudança semântica:** alteração relevante para programa, interface, arquivos, campos ou chamadas, distinta de comentário/formatação.

## 3. Fluxo operacional padronizado (oito etapas)

### 01 — Receber e identificar a origem
- Usuário seleciona um conjunto autorizado, com identificação de fonte, biblioteca e ambiente.
- Informa se o inventário é **completo** ou **parcial**. Sem essa informação, assumir **parcial**.
- Normaliza nomes e separa homônimos de bibliotecas distintas.
- Não enviar código corporativo ao GitHub Pages; ambiente interno é pré-requisito para fontes corporativos.

**Saída:** \`sync_run\` em estado recebido e manifest com proveniência.

### 02 — Comparar com o catálogo aprovado
- Diferenciar \`NOVO\`, \`ALTERADO\`, \`INALTERADO\`, \`POSSIVEL_RENOMEACAO\`, \`AUSENTE\`, \`CONFLITO\`.
- Comparar hash do conteúdo **e** versão do parser. Se um parser mudou, o artefato precisa ser reprocessado mesmo sem alteração de fonte.
- Se a origem disponibilizar hashes confiáveis no manifest, evitar ler os corpos inalterados; no navegador atual, é necessário ler o arquivo para calcular seu hash.
- Ausência só vira candidato a remoção após inventário **completo e confiável**. Importação parcial jamais deve disparar exclusão.

**Saída:** plano de diferenças preliminar.

### 03 — Processar novos e modificados
- Enviar somente itens alterados ou ainda não indexados ao Web Worker.
- Extrair tokens/ocorrências, comandos, referências, alvos e linhas.
- Não assumir que um valor \`PROGRAMA=\` confirma uma chamada; \`EXEC PGM=&VAR\` é dinâmico e permanece não resolvido sem contexto.
- Erros de um arquivo não cancelam a análise dos demais, mas devem bloquear sua substituição no catálogo aprovado.

**Saída:** registros candidatos, isolados do catálogo consultável.

### 04 — Resolver relações e validar
- Aplicar precedência de bibliotecas, aliases e contexto quando disponíveis.
- Distinguir: confirmado por fonte, inferido, dinâmico, alvo ausente e ambíguo.
- Validar unicidade de chave, hash, número de linhas, consistência de relações e origem da evidência.
- Gerar lista de pendências para revisão humana; nunca inventar vínculo que não foi demonstrado.

**Saída:** relatório de qualidade e candidatos aptos/quarentenados.

### 05 — Exibir prévia das mudanças
- Mostrar quantitativos e lista: novos, alterados, inalterados, candidatos à exclusão, conflitos e falhas.
- Para cada modificado, oferecer diff e resumo das referências adicionadas/retiradas.
- Exibir impacto potencial no grafo atual (quando estiver disponível), sem tratar hipóteses como fatos.
- Operação de limpeza/exclusão requer confirmação explícita.

**Saída:** decisão de aprovar, rejeitar ou corrigir a sincronização.

### 06 — Publicar catálogo consistente
- Preparar snapshot candidato; preservar o snapshot anterior.
- Aplicar dados novos, mudanças e exclusões aprovadas sem expor estado intermediário incoerente às consultas.
- Avançar ponteiro do catálogo ativo **somente após validação**. No MVP atual há atomicidade por artefato; a publicação de um lote/snapshot completo ainda precisa ser implementada.
- Atualizar índices, arestas de ida e volta e referências não resolvidas; invalidar resultados em cache apenas dos elementos afetados.

**Saída:** snapshot publicado com ID de execução e versão do parser.

### 07 — Verificar e recuperar
- Repetir buscas de referência (suite padrão), verificar contagens, dependências, ausência de links órfãos indevidos e evidências de linha.
- Em caso de falha, manter ou restaurar o snapshot anterior. Não substituir um índice válido por conteúdo parcial.
- Garantir idempotência: repetir o mesmo inventário não deve duplicar fontes, ocorrências ou relações.

**Saída:** publicação validada ou reversão documentada.

### 08 — Auditar e medir
- Registrar: usuário/ação (quando houver autenticação), origem, hora, hashes, parser, snapshot, itens tratados, erros, decisão e métricas.
- Painel: tempo de indexação, tempo de consulta, tamanho ocupado, relações não resolvidas, fontes desatualizados.
- Reindexação integral somente quando necessária: mudança de algoritmo, corrupção, alteração de esquema ou reconstrução solicitada.

**Saída:** histórico verificável, pronto para repetir o ciclo.

## 4. Casos de uso e regras

| Evento | Comportamento esperado |
| --- | --- |
| Arquivo novo | Criar identidade, indexar, gerar relações, validar e incluir no snapshot |
| Conteúdo modificado | Preservar referência anterior, gerar novo índice e substituir relações ao publicar |
| Mesmo conteúdo/hash e mesmo parser | Não reprocessar |
| Hash igual, parser atualizado | Reindexar |
| Arquivo ausente em lote parcial | Não excluir |
| Arquivo ausente em inventário completo | Propor exclusão/arquivamento, exigir confirmação |
| Renomeação | Tratar como possibilidade até confirmar identidade; preservar histórico |
| Mesmo nome em bibliotecas diferentes | Manter identidades e contextos distintos |
| Dependência dinâmica | Marcar como não resolvida, com evidência da linha |
| Falha de parser | Quarentena, preservando versão aprovada |
| Sincronização repetida | Resultado idempotente, sem duplicatas |
| Quota do navegador esgotada | Mensagem clara e preservação dos dados válidos; plano de recuperação |

### Exemplo de atualização
Inventário completo hipotético de 1.562 arquivos: 1.540 inalterados, 12 modificados, 7 novos e 3 candidatos a remoção. Reprocessar 19 arquivos (além de revisões que dependam da versão do parser), reconciliar vínculos e apresentar prévia das 3 remoções. Não reindexar 1.540 fontes sem motivo. Esses números são ilustrativos.

## 5. Roteiro evolutivo e marcos de aprovação

### Entrega MV-09A — Estrutura do catálogo (0.9, PR #148)
**Existe na branch:** IndexedDB, quatro stores, SHA-256, parsing em worker, índice invertido, relações básicas, busca e aba CATÁLOGO.

**Pendente para aceite:**
- [ ] Testar IndexedDB real em Chrome/Edge e Android, incluindo reload.
- [ ] Confirmar busca, evidências e relações nos quatro arquivos fictícios.
- [ ] Rodar primeira e segunda indexações (a segunda deve mostrar zero reprocessamentos).
- [ ] Rodar alteração e exclusão explícita; conferir remoção de referências obsoletas.
- [ ] Medir uso de armazenamento e tratar erros de quota.
- [ ] Revisar segurança, permissões e regressões da voz.
- [ ] Aprovar PR antes de promover para main.

**Portão de aprovação:** CI verde + roteiro manual validado + aprovação expressa de merge/publicação.

### Entrega MV-09B — Motor de sincronização incremental (0.9.x)
**Construir:**
- [ ] Registro de origens e inventários com modo completo/parcial.
- [ ] Detecção de novos, alterados, inalterados, conflitos, possíveis renomeações e ausentes.
- [ ] Atualização e remoção controlada em lote, sem inferir exclusões de importações parciais.
- [ ] Tratamento individual de erros, retomada e idempotência.
- [ ] Tela de prévia, diferenças e aprovação.

**Portão de aprovação:** testar cenários de adição, mudança, exclusão, conflito, interrupção e reexecução.

### Entrega MV-09C — Histórico, snapshots e confiabilidade (0.9.x)
**Construir:**
- [ ] Execuções de sincronização, snapshots e versões de fonte.
- [ ] Publicação consistente de lote e restauração do snapshot anterior.
- [ ] Referências ambíguas/dinâmicas com status de resolução.
- [ ] Relatório de qualidade e métricas.
- [ ] Teste de carga com 1.562 artefatos **sintéticos**, sem qualquer fonte corporativo.

**Portão de aprovação:** integridade demonstrada após falhas e retomadas; baseline de desempenho documentada.

### Entrega MV-10A — Grafo visual e análise de impacto (1.0)
**Construir:**
- [ ] Navegação bidirecional entre componentes, agrupada por biblioteca/tipo.
- [ ] Diferenciação visual de ligações confirmadas, inferidas e não resolvidas.
- [ ] Destaque das linhas de evidência e explicação do caminho de dependência.
- [ ] Pesquisa inversa: “quem usa este COPYBOOK/programa?”.
- [ ] Comparação de grafos entre snapshots e análise de impacto.
- [ ] Interface adaptada para desktop e celular; evitar grafos ilegíveis por excesso de nós.

**Portão de aprovação:** consultas reproduzíveis com origem e linha; impacto reconhece lacunas e ambiguidades.

### Entrega MV-11A — Inteligência conversacional ancorada (1.1)
**Construir:**
- [ ] Tradutor de perguntas em consultas do catálogo/grafo.
- [ ] Recuperação de evidências e apresentação das fontes usados.
- [ ] Explicação de alterações e impactos sem inventar componentes.
- [ ] Avaliação com conjunto de perguntas/respostas verificadas (golden set).
- [ ] Definir antes da implementação provedor, custo, privacidade e políticas para qualquer IA externa.

**Portão de aprovação:** respostas auditáveis, medição de acertos/erros e isolamento dos dados demonstrativos.

### Futuro condicional MV-12 — Integração corporativa autorizada
- [ ] Definir arquitetura interna: API, autenticação, autorização, segredos, auditoria e dados em repouso.
- [ ] Estudar leitura de inventários e fontes por mecanismo permitido no z/OS, em ambiente controlado.
- [ ] Substituir o IndexedDB como repositório de verdade por serviço interno com persistência central (PostgreSQL é candidato, sujeito a requisitos do banco).
- [ ] Aplicar classificação e escopo de acesso por biblioteca/componente.
- [ ] Proibir publicação de fontes e metadados sensíveis no GitHub Pages público.

**Condição:** arquitetura aprovada pelo responsável técnico e pela segurança; nenhuma conexão bancária implícita.

## 6. Ideias adicionais a priorizar depois da base

| Ideia | Benefício | Etapa sugerida |
| --- | --- | --- |
| Diff semântico de COBOL/JCL | Distinguir mudança de comentário de alteração funcional | 0.9C / 1.0 |
| Painel “o que mudou desde minha última visita?” | Facilitar rotina de análise | 1.0 |
| Indicador de confiança das relações | Evitar falsa certeza em dependências indiretas | 0.9C / 1.0 |
| Caderno de evidências de análise | Compartilhar decisão, linhas e versão analisada | 1.0 |
| Perguntas regressivas (golden set) | Detectar deterioração da análise ao atualizar parser/IA | 0.9C / 1.1 |
| Catálogo portável de dados **fictícios** | Reproduzir testes em outros navegadores/dispositivos | 0.9C |
| Ranking de impacto por criticidade | Ordenar dependências por risco, não só contagem | 1.0+ |
| PWA/offline para demonstração | Uso em apresentações sem conectividade | Futura, depois de medir armazenamento |

## 7. Modelo de gestão do plano (GitHub)

**Unidades:** Plano Diretor → Versão → Entrega/Epic (MV-09A etc.) → Issue executável → PR → validação → release.

**Campos sugeridos em GitHub Projects:** Versão, Entrega, Prioridade (P0/P1/P2), Status, Risco, Responsável, Dependência, Estimativa, Evidência de teste e Bloqueio de publicação.

**Fluxo de status:** Ideia → Especificado → Aprovado → Em desenvolvimento → Em revisão → Em validação → Aprovado para publicação → Publicado. Separar "Bloqueado" e "Rejeitado" quando cabível.

**Template mínimo de issue:**
- ID e versão / entrega
- Objetivo e problema de usuário
- Regra de negócio e exemplo de entrada/saída
- Escopo e não escopo
- Critérios de aceite observáveis
- Testes (unitário, integração e manual)
- Segurança/privacidade e risco de regressão
- Dependências e evidência de conclusão
- **Permissão de publicar?** somente aprovação expressa

**Regra de publicação:** feature branch + PR draft/revisão; \`main\` só após aprovação explícita. O Pages atual publica automaticamente em pushes para \`main\`, então merge equivale a acionar publicação. Não modificar o fluxo de promoção sem decisão explícita.

## 8. Ordem imediata sugerida

1. Homologar MV-09A sem merge.
2. Implementar MV-09B: inventário, classificação e operações de inclusão/alteração/exclusão.
3. Implementar MV-09C: snapshots e reversão com testes de carga.
4. Aprovar promoção da 0.9 para main somente com evidências.
5. Avançar para grafo visual 1.0, reaproveitando as relações já catalogadas.
6. Somente depois integrar IA generativa 1.1, com respostas fundamentadas.

**Princípio permanente:** cada nova entrega deve vir com demonstração, teste, métrica, limites conhecidos e decisão de promoção. Não assumir que implementar equivale a publicar.
