# Documentação da Análise Semântica — Linguagem Esperanta

Esta documentação descreve os aspectos semânticos da linguagem **Esperanta** e como o analisador semântico os verifica.

## 1. Visão geral

O analisador semântico é a terceira fase do front end:

```
código-fonte (.esp)
      │
 anLexico.py      → tokens
      │
 anSintatico.py   → árvore de derivação (parse tree, classe `No`)
      │
 anAST.py         → AST (descarta não-terminais auxiliares)
      │
 anSemantico.py   → erros e avisos semânticos  (usa tabelaSimbolos.py)
```

- A análise semântica **só é executada se não houver erros léxicos nem sintáticos**.
- A abordagem escolhida é a **travessia de uma AST** com uma **tabela de símbolos** (em vez de ações semânticas embutidas no parser LL(1)). Cada método `_tipo` devolve o tipo sintetizado de uma expressão (atributo sintetizado), e a tabela de símbolos funciona como ambiente herdado.
- Mensagens seguem o formato `Linha N: mensagem`.

### Arquivos

| Arquivo | Papel |
|---|---|
| `anAST.py` | Nós da AST (`Programa`, `Bloco`, `Declaracao`, `Atribuicao`, `Se`, `Dum`, `Al`, `Eniro`, `Elijero`, `BinOp`, `UnOp`, `Literal`, `Var`), `construir_ast` e `imprimir_ast`. Todo nó guarda `linha`. |
| `tabelaSimbolos.py` | `Simbolo` e `TabelaSimbolos` (pilha de escopos). |
| `anSemantico.py` | `AnalisadorSemantico` e `analisar_arquivo`. |
| `teste_semantico.esp` | Programa sintaticamente válido com 13 erros semânticos propositais. |
| `teste_valido.esp` | Programa válido; gera apenas 1 aviso (`r` nunca usada). |

### Execução

```
python anSemantico.py arquivo.esp          # análise
python anSemantico.py arquivo.esp --ast    # imprime também a AST
```

No Windows, use `PYTHONIOENCODING=utf-8` para exibir acentos corretamente.

## 2. Tabela de símbolos

Implementada como **pilha de dicionários** (um por escopo ativo).

Cada `Simbolo` possui:

| Campo | Descrição |
|---|---|
| `nome` | identificador |
| `tipo` | `tuta`, `reala`, `karaktero` ou `bolea` |
| `linha` | linha da declaração |
| `escopo` | nível de aninhamento (0 = bloco de `precipa`) |
| `inicializada` | `True` se declarada com valor, atribuída ou lida por `eniro` |
| `usada` | `True` se referenciada em alguma expressão, atribuição ou `eniro`/`elijero` |

Operações:

- `entrar_escopo()` / `sair_escopo()` — empilha/desempilha; `sair_escopo` devolve os símbolos do escopo para a verificação de "nunca usada".
- `declarar(nome, tipo, linha, inicializada)` — insere no escopo **atual**; devolve `None` se o nome já existe nele (redeclaração).
- `buscar(nome)` — procura do escopo mais interno ao mais externo (permite sombreamento).
- `historico` — todos os símbolos declarados, na ordem, usado para imprimir a tabela ao final.

## 3. Escopos

- O corpo de `precipa` é o escopo de nível 0.
- Cada **bloco** `{ ... }` (de `se`, `se ne`, `dum`, `al`) abre um novo escopo.
- O comando `al` abre um escopo extra para o comando de inicialização: a variável declarada em `al (tuta t = 0; ...)` existe só dentro do `al` (condição, atualização e bloco).
- Uma variável pode ser **redeclarada em escopo interno** (sombreamento) — não é erro. Redeclarar no **mesmo** escopo é erro.
- Numa declaração, a expressão de inicialização é avaliada **antes** de declarar o nome; assim `tuta x = x;` refere-se a um `x` externo.

## 4. Sistema de tipos

Tipos: `tuta` (inteiro), `reala` (real), `karaktero` (caractere), `bolea` (booleano). Não há funções, vetores nem outros tipos.

Tipos dos literais: `num_int` → `tuta`; `num_real` → `reala`; `caractere` → `karaktero`; `vere`/`malvere` → `bolea`.

### 4.1 Compatibilidade de atribuição (`destino ← origem`)

| Destino \ Origem | tuta | reala | karaktero | bolea |
|---|:-:|:-:|:-:|:-:|
| `tuta` | ✔ | ✘ | ✘ | ✘ |
| `reala` | ✔ (conversão implícita) | ✔ | ✘ | ✘ |
| `karaktero` | ✘ | ✘ | ✔ | ✘ |
| `bolea` | ✘ | ✘ | ✘ | ✔ |

Única conversão implícita: `tuta → reala` (alargamento). Aplica-se a declaração com inicialização e a atribuição.

### 4.2 Operadores

| Operador | Operandos | Resultado |
|---|---|---|
| `+ - * /` | ambos numéricos (`tuta`/`reala`) | `reala` se algum operando for `reala`; senão `tuta` |
| `-` unário | numérico | mesmo tipo do operando |
| `==` `!=` | ambos numéricos, **ou** ambos do mesmo tipo | `bolea` |
| `>` `<` | ambos numéricos, **ou** ambos `karaktero` | `bolea` |
| `e` `au` | ambos `bolea` | `bolea` |
| `ne` (unário) | `bolea` | `bolea` |

Observações:

- `bolea` não pode ser comparado com `>`/`<`; `bolea == bolea` é permitido.
- `tuta` e `reala` podem ser misturados em operações e comparações.
- **Divisão por zero**: erro quando o divisor é um literal numérico igual a zero (`x / 0`, `x / 0.0`). Divisores não literais não são avaliados.

### 4.3 Condições

A expressão de `se`, `dum` e da condição central de `al` deve ter tipo `bolea`.

### 4.4 Propagação de erro (evitar cascata)

Existe um tipo interno especial `erro`. Quando uma subexpressão já gerou erro, ela devolve `erro` e as expressões que a contêm **não reportam novos erros** por causa dela. Assim, cada problema real é reportado uma única vez.

## 5. Comandos e regras verificadas

| Comando | Verificações |
|---|---|
| `tipo id [= expr];` | nome não declarado no escopo atual; tipo da expressão compatível com o tipo declarado |
| `id = expr;` | `id` declarado (em qualquer escopo visível); tipo compatível; marca `id` como inicializada |
| `se (c) {…} [se ne {…}]` | `c` é `bolea`; blocos em escopos próprios |
| `dum (c) {…}` | `c` é `bolea`; bloco em escopo próprio |
| `al (init; c; atualiza) {…}` | escopo próprio para `init`; `c` é `bolea`; `atualiza` é atribuição válida |
| `eniro(id);` | `id` declarado; marca como **inicializada** e usada |
| `elijero(id);` | `id` declarado; aviso se ainda não inicializada |

## 6. Erros semânticos

| # | Erro | Mensagem (resumo) |
|---|---|---|
| 1 | Redeclaração no mesmo escopo | `variável 'x' já declarada neste escopo (linha N)` |
| 2 | Variável não declarada | `variável 'x' não declarada` |
| 3 | Inicialização incompatível | `não é possível inicializar 'x' (tipo) com valor tipo2` |
| 4 | Atribuição incompatível | `não é possível atribuir tipo2 a 'x' (tipo)` |
| 5 | Operador aritmético com tipo inválido | `operador '+' exige operandos numéricos, encontrado A e B` |
| 6 | Operador lógico (`e`/`au`) inválido | `operador 'e' exige operandos bolea, encontrado A e B` |
| 7 | `ne` fora de bolea | `operador 'ne' exige bolea, encontrado T` |
| 8 | `-` unário fora de numérico | `operador '-' unário exige tuta ou reala, encontrado T` |
| 9 | Relacional inválido | `operador '<' não se aplica a A e B` |
| 10 | Condição não booleana | `condição de 'se' deve ser bolea, encontrado T` |
| 11 | Divisão por zero literal | `divisão por zero` |

## 7. Avisos (não impedem a compilação)

- `variável 'x' usada sem ter sido inicializada` — leitura de variável declarada sem valor e ainda não atribuída/lida por `eniro` (a análise é linear, não considera fluxo de controle).
- `variável 'x' declarada mas nunca usada` — emitido ao sair do escopo.

## 8. Exemplo

Trecho de `teste_semantico.esp`:

```
tuta x = 0;
tuta x = 1;      // erro 1: redeclaração
bolea b = 5;     // erro 3: tuta → bolea
y = 3;           // erro 2: y não declarada
b = x + c;       // erro 5: tuta + karaktero
r = x / 0;       // erro 11: divisão por zero
se (x) { ... }   // erro 10: condição tuta
dum (x + 1) {
    tuta x = 3;  // ok: sombreamento em escopo interno
}
al (tuta t = 0; t < 10; t = t + 1) { elijero(t); }
elijero(t);      // erro 2: t fora do escopo do al
```

O arquivo completo produz 13 erros e 3 avisos (`nao_init` sem inicialização; `i` e o `x` interno do `dum` nunca usados).

## 9. Limitações e trabalhos futuros

- Sem análise de fluxo: o aviso de não inicialização é aproximado (não distingue ramos de `se`).
- Divisão por zero só é detectada para divisor literal.
- Não há avaliação de constantes (`x / (1 - 1)` não é detectado).
- Sem testes automatizados (a validação é feita por `teste_semantico.esp` e `teste_valido.esp`).
- A geração de código intermediário poderá reaproveitar a AST e os tipos já inferidos.
