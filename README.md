# Multivacia — MVP 0.8

Interface retrô para facilitar o primeiro contato de profissionais de mainframe com IA.

## Executar localmente

Abra o arquivo `index.html` em um navegador para testar a interface, a conversa local e a síntese de voz. Para testar o microfone, **use HTTPS ou localhost**; abrir o HTML pela pasta Downloads do Android não é suficiente.

Exemplo para computador, na pasta do repositório:

```bash
python3 -m http.server 8080
```

Depois abra `http://localhost:8080`. A publicação HTTPS será tratada em uma etapa separada.

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

## Fora do escopo deste MVP

Sem IA generativa, sem integração z/OS, sem login, sem backend e sem publicação automática. O reconhecedor do navegador **pode enviar áudio a serviços externos**; por isso, use somente frases de teste e informações autorizadas. A importação de arquivos é local ao aplicativo e não é enviada por ele a servidor algum.

A interface não substitui revisão humana nem executa jobs. Não inclua código ou dados de clientes/BRQ neste repositório público.

**Validação:** a página é publicada via GitHub Pages em https://multivacia.github.io/wick/ .
A captação e a reprodução de voz foram confirmadas em Android para a versão 0.7.1; a 0.8 ainda precisa de teste real após a atualização.

**Como testar a 0.8:** abra a página pelo HTTPS; habilite `AUTO ENVIO: ON` e, se desejar resposta falada, `FALA AUTOMÁTICA: ON`. Toque em OUVIR e diga "Qual programa executa o STEP050 do RFJ0001?". O envio automático só ocorre quando o navegador informa que a transcrição está finalizada. `PARAR` cancela a escuta ou interrompe a resposta. Mantenha AUTO ENVIO desligado se preferir revisar o texto antes de enviar.
