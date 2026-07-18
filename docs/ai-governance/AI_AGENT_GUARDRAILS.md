# Guardrails para Agentes de IA

## 1. Escopo

Estas regras se aplicam a qualquer IA que atue no Wick, independentemente da ferramenta.

## 2. Princípios obrigatórios

### 2.1 Leitura antes de escrita

Antes de alterar arquivos, o agente deve:

- identificar a branch e o commit-base;
- ler os documentos relevantes;
- entender o estado oficial do projeto;
- listar restrições e itens fora de escopo;
- confirmar que não está trabalhando diretamente na `main`.

### 2.2 Branch dedicada

Toda alteração deve ocorrer em branch dedicada.

Formato recomendado:

```text
feature/<escopo>
fix/<escopo>
docs/<escopo>
agent/<escopo>
```

É proibido trabalhar diretamente na `main`.

### 2.3 Mudanças pequenas e rastreáveis

O agente deve:

- limitar cada tarefa a um objetivo;
- evitar refatorações não solicitadas;
- evitar alterações cosméticas fora do escopo;
- manter commits coesos;
- registrar todos os arquivos alterados.

### 2.4 Evidência antes de conclusão

Nenhum agente pode declarar uma tarefa concluída apenas porque o código foi gerado.

A conclusão exige evidência, como:

- testes executados;
- resultado dos testes;
- análise do diff;
- documentação atualizada;
- riscos remanescentes;
- confirmação de que itens proibidos não foram executados.

### 2.5 Sem suposições silenciosas

Quando houver ambiguidade relevante, o agente deve:

- registrar a suposição;
- escolher a opção mais conservadora;
- bloquear a ação se a suposição puder alterar estado científico, dados ou produção.

## 3. Ações proibidas sem autorização humana explícita

```text
PROHIBITED_WITHOUT_EXPLICIT_HUMAN_AUTHORIZATION:
- merge de pull request
- push direto em main
- force-push
- exclusão de branch remota
- alteração de histórico Git
- execução de validate científico
- consulta de métricas de efeito antes do gate
- alteração de cutoff
- alteração de freeze
- alteração de thresholds congelados
- alteração de critérios de aprovação após observar resultados
- liberação de interpretação econômica
- alteração de R3E_GATE, R4_STATUS ou R5_STATUS
- acesso ou modificação de dados de produção
- exclusão ou sobrescrita de datasets
- rotação ou remoção de segredos
- mudança em permissões de repositório
```

## 4. Ações destrutivas

Ações destrutivas exigem:

1. descrição exata do impacto;
2. plano de rollback;
3. autorização humana;
4. registro posterior do resultado.

## 5. Proteção contra alucinação

O agente deve tratar como não confirmado qualquer item que não tenha sido verificado em:

- código;
- testes;
- documentação oficial;
- estado do GitHub;
- saída real de comando.

Frases como “provavelmente”, “deve estar” ou “parece” não podem ser usadas como evidência de conclusão.

## 6. Separação de funções

O agente que implementa não deve ser a única fonte de aprovação.

Fluxo mínimo:

```text
Especificação → Implementação → Revisão independente → Autorização humana
```

## 7. Estado padrão

Na dúvida:

```text
MERGE_STATUS = BLOCKED
REVIEW_STATUS = PENDING
SCIENTIFIC_ACTIONS_ALLOWED = false
```
