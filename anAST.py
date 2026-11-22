"""AST da linguagem Esperanta e conversão da árvore de derivação (anSintatico.No) em AST.

A árvore de derivação contém todos os não-terminais auxiliares (LISTACOMANDOS,
EXPRESSAOLOGICALINHA, ...). A AST descarta esse ruído e deixa só a estrutura
relevante para o analisador semântico. Todo nó guarda `linha` para mensagens de erro.
"""
from dataclasses import dataclass, field
from typing import List, Optional


# ---------- nós ----------
@dataclass
class Programa:
    comandos: List["object"]
    linha: int = 0

@dataclass
class Bloco:
    comandos: List["object"]
    linha: int = 0

@dataclass
class Declaracao:
    tipo: str
    nome: str
    init: Optional["object"]
    linha: int = 0

@dataclass
class Atribuicao:
    nome: str
    expr: "object"
    linha: int = 0

@dataclass
class Se:
    cond: "object"
    bloco: Bloco
    senao: Optional[Bloco]
    linha: int = 0

@dataclass
class Dum:
    cond: "object"
    bloco: Bloco
    linha: int = 0

@dataclass
class Al:
    init: "object"          # Declaracao ou Atribuicao
    cond: "object"
    atualiza: "object"      # Atribuicao
    bloco: Bloco
    linha: int = 0

@dataclass
class Eniro:
    nome: str
    linha: int = 0

@dataclass
class Elijero:
    nome: str
    linha: int = 0

@dataclass
class BinOp:
    op: str
    esq: "object"
    dir: "object"
    linha: int = 0

@dataclass
class UnOp:
    op: str                 # '-' ou 'ne'
    operando: "object"
    linha: int = 0

@dataclass
class Literal:
    tipo: str               # tuta | reala | karaktero | bolea
    valor: str
    linha: int = 0

@dataclass
class Var:
    nome: str
    linha: int = 0


# ---------- conversão ----------
_TIPO_LITERAL = {"num_int": "tuta", "num_real": "reala", "caractere": "karaktero"}


def _f(no, simbolo):
    """Primeiro filho com o símbolo dado."""
    for filho in no.filhos:
        if filho.simbolo == simbolo:
            return filho
    raise KeyError(simbolo)


def _linha(no):
    """Linha do primeiro token folha dentro do nó."""
    if no.token is not None:
        return no.token.linha
    for filho in no.filhos:
        l = _linha(filho)
        if l:
            return l
    return 0


def construir_ast(raiz):
    return _programa(raiz)


def _programa(no):
    return Programa(_lista(_f(no, "LISTACOMANDOS")), _linha(no))


def _lista(no):
    """LISTACOMANDOS -> COMANDO LISTACOMANDOS | ε (iterativo)."""
    comandos = []
    while no.filhos:
        comandos.append(_comando(no.filhos[0]))
        no = no.filhos[1]
    return comandos


def _bloco(no):
    return Bloco(_lista(_f(no, "LISTACOMANDOS")), _linha(no))


def _comando(no):
    filho = no.filhos[0]
    return {
        "DECLARACAO": _declaracao,
        "ATRIBUICAO": _atribuicao,
        "COM_SE": _se,
        "COM_DUM": _dum,
        "COM_AL": _al,
        "COM_ENIRO": lambda n: Eniro(_f(n, "id").token.lexema, _linha(n)),
        "COM_ELIJERO": lambda n: Elijero(_f(n, "id").token.lexema, _linha(n)),
    }[filho.simbolo](filho)


def _tipo(no):
    return _f(no, "TIPO").filhos[0].token.lexema


def _declaracao(no):
    resto = _f(no, "RESTODECLARACAO")
    init = _expr(_f(resto, "EXPRESSAO")) if any(f.simbolo == "EXPRESSAO" for f in resto.filhos) else None
    id_tok = _f(no, "id").token
    return Declaracao(_tipo(no), id_tok.lexema, init, id_tok.linha)


def _atribuicao(no):
    id_tok = _f(no, "id").token
    return Atribuicao(id_tok.lexema, _expr(_f(no, "EXPRESSAO")), id_tok.linha)


def _se(no):
    sene = _f(no, "COM_SENE")
    senao = _bloco(_f(sene, "BLOCO")) if sene.filhos else None
    return Se(_expr(_f(no, "EXPRESSAO")), _bloco(_f(no, "BLOCO")), senao, _linha(no))


def _dum(no):
    return Dum(_expr(_f(no, "EXPRESSAO")), _bloco(_f(no, "BLOCO")), _linha(no))


def _alinit(no):
    id_tok = _f(no, "id").token
    expr = _expr(_f(no, "EXPRESSAO"))
    if any(f.simbolo == "TIPO" for f in no.filhos):
        return Declaracao(_tipo(no), id_tok.lexema, expr, id_tok.linha)
    return Atribuicao(id_tok.lexema, expr, id_tok.linha)


def _al(no):
    # filhos: al ( ALINIT ; EXPRESSAO ; ALATUALIZA ) BLOCO
    return Al(
        _alinit(_f(no, "ALINIT")),
        _expr(_f(no, "EXPRESSAO")),
        _atribuicao(_f(no, "ALATUALIZA")),
        _bloco(_f(no, "BLOCO")),
        _linha(no),
    )


# ---------- expressões ----------
def _expr(no):
    """Despacha pelos níveis EXPRESSAO > LOGICA > RELACIONAL > ARITMETICA > TERMO > FATOR."""
    s = no.simbolo
    if s == "EXPRESSAO":
        return _expr(no.filhos[0])
    if s == "EXPRESSAOLOGICA":
        return _cadeia(no.filhos[0], no.filhos[1], _expr)
    if s == "EXPRESSAORELACIONAL":
        esq = _expr(no.filhos[0])
        linha = no.filhos[1]
        if not linha.filhos:
            return esq
        op = linha.filhos[0].filhos[0].token
        return BinOp(op.lexema, esq, _expr(linha.filhos[1]), op.linha)
    if s == "EXPRESSAOARITMETICA":
        return _cadeia(no.filhos[0], no.filhos[1], _expr)
    if s == "TERMO":
        return _cadeia(no.filhos[0], no.filhos[1], _expr)
    if s == "FATOR":
        return _fator(no)
    raise ValueError(s)


def _cadeia(primeiro, resto, conv):
    """Dobra à esquerda: X -> A X' ; X' -> op A X' | ε  (associatividade à esquerda)."""
    esq = conv(primeiro)
    while resto.filhos:
        op_no, operando, resto = resto.filhos
        op = op_no.token if op_no.token is not None else op_no.filhos[0].token
        esq = BinOp(op.lexema, esq, conv(operando), op.linha)
    return esq


def _fator(no):
    f = no.filhos
    if len(f) == 1:
        t = f[0].token
        if t.tipo == "id":
            return Var(t.lexema, t.linha)
        if t.tipo in _TIPO_LITERAL:
            return Literal(_TIPO_LITERAL[t.tipo], t.lexema, t.linha)
        return Literal("bolea", t.lexema, t.linha)   # vere / malvere
    if f[0].simbolo == "(":
        return _expr(f[1])
    # '-' FATOR  |  'ne' FATOR
    return UnOp(f[0].token.lexema, _fator(f[1]), f[0].token.linha)


# ---------- impressão (depuração) ----------
def imprimir_ast(n, recuo=0):
    pad = "  " * recuo
    if isinstance(n, list):
        for x in n:
            imprimir_ast(x, recuo)
    elif hasattr(n, "__dataclass_fields__"):
        simples = {k: v for k, v in vars(n).items()
                   if k != "linha" and not (isinstance(v, list) or hasattr(v, "__dataclass_fields__"))}
        print(f"{pad}{type(n).__name__} {simples if simples else ''}")
        for k, v in vars(n).items():
            if isinstance(v, list) or hasattr(v, "__dataclass_fields__"):
                print(f"{pad}  .{k}:")
                imprimir_ast(v, recuo + 2)
    elif n is None:
        pass
