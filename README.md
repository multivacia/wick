# MultivacIA — 0.9 (prévia de arquitetura)

Interface retrô para facilitar o primeiro contato de profissionais de mainframe com IA.

## Executar localmente

Abra o projeto por um servidor HTTP local para testar a interface, a conversa, a síntese de voz **e os módulos do catálogo**. Abrir `index.html` diretamente como `file://` pode bloquear os módulos ES e o IndexedDB. Para testar o microfone, **use HTTPS ou localhost**; abrir o HTML pela pasta Downloads do Android não é suficiente.

Exemplo para computador, na pasta do repositório:

```bash
python3 -m http.server 8080
```

Depois abra `http://localhost:8080`. A versão pública atual permanece no GitHub Pages, hospedada a partir da `main`; esta prévia fica isolada na branch de desenvolvimento.

## Incluído

- Tela preta, rosto pixelado verde e modulador de três barras durante a fala
- Português Brasil (`pt-BR`), inglês EUA (`en-US`) e inglês Reino Unido (`en-GB`)
- Voz do navegador, seleção de vozes disponíveis, reprodução e interrupção
- Reconhecimento de voz quando suportado, com transcrição para conferência
- Envio **manual por padrão** ou **automático opcional** após o serviço retornar a transcrição final
- Indicadores animados de **ouvindo**, **analisando** e **falando**, e botão **PARAR** que interrompe a resposta
- Diagnóstico de eventos do reconhecimento de voz e teste local de sinal do microfone
- Análise estrutural demonstrativa de quatro arquivos *fictícios*: JCL, PROC, COBOL e COPYBOOK
- Importação local opcional de arquivos de texto para experimentos autorizados
- **Nova na 0.9:** aba CATÁLOGO com IndexedDB, índice invertido, hash SHA-256, Web Worker, busca textual e relações com linhas de evidência
- Indexação iniciada explicitamente pelo usuário; fonte inalterado não é reanalisado; limpeza do índice local

## Fora do escopo deste MVP

Sem IA generativa, sem integração z/OS, sem login, sem backend nem conexão de artefatos a z/OS. O reconhecedor do navegador **pode enviar áudio a serviços externos**; por isso, use somente frases de teste e informações autorizadas. A importação de arquivos é local ao aplicativo e não é enviada por ele a servidor algum.

A interface não substitui revisão humana nem executa jobs. Não inclua código ou dados de clientes/BRQ neste repositório público.

**Publicação atual:** https://multivacia.github.io/wick/ (branch `main`, versão 0.8.1). A prévia 0.9 não é publicada automaticamente: requer aprovação da PR e merge para `main`. A aplicação pública não contém os módulos desta branch enquanto a PR estiver aberta.

**Como testar a 0.8:** abra a página pelo HTTPS; habilite `AUTO ENVIO: ON` e, se desejar resposta falada, `FALA AUTOMÁTICA: ON`. Toque em OUVIR e diga "Qual programa executa o STEP050 do RFJ0001?". O envio automático só ocorre quando o navegador informa que a transcrição está finalizada. `PARAR` cancela a escuta ou interrompe a resposta. Mantenha AUTO ENVIO desligado se preferir revisar o texto antes de enviar.

## Plano Diretor de evolução

O roteiro das versões, o processo de inclusão/atualização/exclusão de componentes e os critérios de liberação estão em [Plano Diretor da MultivacIA](docs/plano-diretor-evolucao.md). A proposta é evolutiva; documentação não autoriza merge nem publicação.

## Arquitetura de dados 0.9

Consulte [Schema, fluxos e segurança do catálogo](docs/arquitetura-catalogo-09.md).

Na aba **CATÁLOGO**, clique em **INDEXAR ARTEFATOS CARREGADOS** para indexar os quatro exemplos. Busque `STEP050`, `RFP0001` ou `CLIPAG`; em seguida, abra as referências do resultado. Depois, execute a mesma indexação e verifique que `0` fontes foram reprocessados. Use **LIMPAR ÍNDICE LOCAL** para apagar os dados persistidos.

Os conteúdos importados que forem indexados ficam armazenados no navegador (por origem) até serem apagados. Não use fontes corporativos nesta demonstração pública.

Execute os testes de parser sem instalar dependências:

```bash
node --test tests/catalog.test.mjs
```
