# Multivacia — MVP 0.7

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
- Reconhecimento de voz quando suportado, com transcrição para conferência **antes do envio**
- Análise estrutural demonstrativa de quatro arquivos *fictícios*: JCL, PROC, COBOL e COPYBOOK
- Importação local opcional de arquivos de texto para experimentos autorizados

## Fora do escopo deste MVP

Sem IA generativa, sem integração z/OS, sem login, sem backend e sem publicação automática. O reconhecedor do navegador **pode enviar áudio a serviços externos**; por isso, use somente frases de teste e informações autorizadas. A importação de arquivos é local ao aplicativo e não é enviada por ele a servidor algum.

A interface não substitui revisão humana nem executa jobs. Não inclua código ou dados de clientes/BRQ neste repositório público.

**Próxima validação:** hospedar uma versão de demonstração em HTTPS e testar o microfone real no Android.
