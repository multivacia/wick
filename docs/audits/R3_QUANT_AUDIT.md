# Auditoria Quantitativa R3

Tente reprovar a metodologia e a implementação.

## Temporalidade

- Sinal sem confirmação entra em t+1?
- Confirmado entra em t+2?
- Saída usa N correto?
- Alguma feature usa futuro?
- Split é temporal?
- Holdout foi tocado durante calibração?

## Custos

- entrada e saída?
- slippage nos dois lados?
- cenários?
- short implícito?
- bearish rotulado corretamente?

## Estatística

- baseline pareado?
- seed fixa?
- block bootstrap?
- FDR?
- amostra pequena destacada?
- sobreposição analisada?
- resultado concentrado?

## Reprodutibilidade

- experiment_id?
- parâmetros congelados?
- versões?
- operações exportáveis?
- cálculo manual bate?
- motor próprio bate com validação complementar?

## Comunicação

- relatório mostra negativos?
- inconclusivo é permitido?
- linguagem executiva é compreensível?
- promoção para R4 é automática indevidamente?
