# Gramática Livre de Contexto — Linguagem "Esperanta"

Notação: literais entre aspas simples são terminais (lexemas exatos); nomes em
`<angulos>` são classes de token devolvidas pelo analisador léxico
(`anLexico.py`); `ε` é a cadeia vazia.

## Terminais (classes de token do léxico)

| Classe          | Lexemas / exemplos                                   |
|-----------------|-------------------------------------------------------|
| `<tipo>`        | tuta, reala, karaktero, bolea                          |
| `<id>`          | identificadores (`[a-zA-Z_]\w*`)                       |
| `<num_int>`     | inteiros (`\d+`)                                       |
| `<num_real>`    | reais (`\d+\.\d+`)                                     |
| `<caractere>`   | caractere entre aspas simples (`'c'`)                  |
| palavras reservadas | precipa, se, se ne, dum, al, eniro, elijero, vere, malvere |
| operadores      | `+ - * / == != > < = e au ne`                          |
| delimitadores   | `( ) { } ;`                                          |

## Produções

```
PROGRAMA -> 'precipa' '(' ')' '{' LISTACOMANDOS '}'

LISTACOMANDOS -> COMANDO LISTACOMANDOS | ε

COMANDO -> DECLARACAO | ATRIBUICAO | COMANDOSE | COMANDODUM | COMANDOAL | COMANDOENIRO | COMANDOELIJERO

BLOCO -> '{' LISTACOMANDOS '}'

DECLARACAO -> TIPO <id> RESTODECLARACAO

RESTODECLARACAO -> '=' EXPRESSAO ';' | ';'

TIPO -> 'tuta' | 'reala' | 'karaktero' | 'bolea'

ATRIBUICAO -> <id> '=' EXPRESSAO ';'

COMANDOSE -> 'se' '(' EXPRESSAO ')' BLOCO COMANDOSENE

COMANDOSENE -> 'se ne' BLOCO | ε

COMANDODUM -> 'dum' '(' EXPRESSAO ')' BLOCO

COMANDOAL -> 'al' '(' ALINIT ';' EXPRESSAO ';' ALATUALIZA ')' BLOCO

ALINIT -> TIPO <id> '=' EXPRESSAO | <id> '=' EXPRESSAO

ALATUALIZA -> <id> '=' EXPRESSAO

COMANDOENIRO -> 'eniro' '(' <id> ')' ';'

COMANDOELIJERO -> 'elijero' '(' <id> ')' ';'

EXPRESSAO -> EXPRESSAOLOGICA

EXPRESSAOLOGICA -> EXPRESSAORELACIONAL EXPRESSAOLOGICALINHA
EXPRESSAOLOGICALINHA -> OPLOGICO EXPRESSAORELACIONAL EXPRESSAOLOGICALINHA | ε
OPLOGICO -> 'e' | 'au'

EXPRESSAORELACIONAL -> EXPRESSAOARITMETICA EXPRESSAORELACIONALLINHA
EXPRESSAORELACIONALLINHA -> OPRELACIONAL EXPRESSAOARITMETICA | ε
OPRELACIONAL -> '==' | '!=' | '>' | '<'

EXPRESSAOARITMETICA -> TERMO EXPRESSAOARITMETICALINHA
EXPRESSAOARITMETICALINHA -> '+' TERMO EXPRESSAOARITMETICALINHA | '-' TERMO EXPRESSAOARITMETICALINHA | ε

TERMO -> FATOR TERMOLINHA
TERMOLINHA -> '*' FATOR TERMOLINHA | '/' FATOR TERMOLINHA | ε

FATOR -> '-' FATOR | 'ne' FATOR | '(' EXPRESSAO ')' | <id> | <num_int> | <num_real> | <caractere> | 'vere' | 'malvere'
```