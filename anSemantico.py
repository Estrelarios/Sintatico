"""Analisador semântico da linguagem Esperanta.

Percorre a AST (anAST) com uma TabelaSimbolos e verifica:
  - declaração antes do uso e redeclaração no mesmo escopo;
  - compatibilidade de tipos em declaração/atribuição (tuta -> reala é permitido);
  - tipos dos operandos de operadores aritméticos, relacionais e lógicos;
  - condições de se/dum/al devem ser bolea;
  - eniro/elijero exigem variável declarada;
  - divisão por zero literal;
Avisos (não impedem a compilação): variável usada sem inicialização, variável nunca usada.
"""
import sys

from anSintatico import analisador_sintatico
from anAST import (construir_ast, imprimir_ast, Programa, Bloco, Declaracao, Atribuicao,
                   Se, Dum, Al, Eniro, Elijero, BinOp, UnOp, Literal, Var)
from tabelaSimbolos import TabelaSimbolos

NUMERICOS = ("tuta", "reala")
ERRO = "erro"   # tipo especial: já houve erro na subexpressão, evita erros em cascata


class AnalisadorSemantico:
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.erros = []
        self.avisos = []

    # ---- utilidades ----
    def erro(self, linha, msg):
        self.erros.append(f"Linha {linha}: {msg}")

    def aviso(self, linha, msg):
        self.avisos.append(f"Linha {linha}: {msg}")

    def _sair_escopo(self):
        for s in self.tabela.sair_escopo():
            if not s.usada:
                self.aviso(s.linha, f"variável '{s.nome}' declarada mas nunca usada")

    @staticmethod
    def compativel(destino, origem):
        """Atribuição origem -> destino."""
        return destino == origem or (destino == "reala" and origem == "tuta")

    # ---- comandos ----
    def analisar(self, programa):
        self.tabela.entrar_escopo()
        self._comandos(programa.comandos)
        self._sair_escopo()
        return not self.erros

    def _comandos(self, comandos):
        for c in comandos:
            self._comando(c)

    def _bloco(self, bloco):
        self.tabela.entrar_escopo()
        self._comandos(bloco.comandos)
        self._sair_escopo()

    def _comando(self, c):
        if isinstance(c, Declaracao):
            self._declaracao(c)
        elif isinstance(c, Atribuicao):
            self._atribuicao(c)
        elif isinstance(c, Se):
            self._condicao(c.cond, "se")
            self._bloco(c.bloco)
            if c.senao:
                self._bloco(c.senao)
        elif isinstance(c, Dum):
            self._condicao(c.cond, "dum")
            self._bloco(c.bloco)
        elif isinstance(c, Al):
            self.tabela.entrar_escopo()          # escopo da variável do init
            self._comando(c.init)
            self._condicao(c.cond, "al")
            self._atribuicao(c.atualiza)
            self._bloco(c.bloco)
            self._sair_escopo()
        elif isinstance(c, Eniro):
            s = self._usar(c.nome, c.linha, leitura=False)
            if s:
                s.inicializada = True            # o valor lido inicializa a variável
        elif isinstance(c, Elijero):
            self._usar(c.nome, c.linha, leitura=True)

    def _declaracao(self, d):
        # a expressão é avaliada antes de declarar: `tuta x = x;` usa um x externo
        tipo_init = self._tipo(d.init) if d.init is not None else None
        if self.tabela.declarar(d.nome, d.tipo, d.linha, inicializada=d.init is not None) is None:
            ant = self.tabela.buscar(d.nome)
            self.erro(d.linha, f"variável '{d.nome}' já declarada neste escopo (linha {ant.linha})")
            return
        if tipo_init is not None and tipo_init != ERRO and not self.compativel(d.tipo, tipo_init):
            self.erro(d.linha, f"não é possível inicializar '{d.nome}' ({d.tipo}) com valor {tipo_init}")

    def _atribuicao(self, a):
        tipo_expr = self._tipo(a.expr)
        s = self._usar(a.nome, a.linha, leitura=False)
        if s is None:
            return
        s.inicializada = True
        if tipo_expr != ERRO and not self.compativel(s.tipo, tipo_expr):
            self.erro(a.linha, f"não é possível atribuir {tipo_expr} a '{a.nome}' ({s.tipo})")

    def _condicao(self, expr, nome):
        t = self._tipo(expr)
        if t not in (ERRO, "bolea"):
            self.erro(expr.linha, f"condição de '{nome}' deve ser bolea, encontrado {t}")

    def _usar(self, nome, linha, leitura):
        s = self.tabela.buscar(nome)
        if s is None:
            self.erro(linha, f"variável '{nome}' não declarada")
            return None
        s.usada = True
        if leitura and not s.inicializada:
            self.aviso(linha, f"variável '{nome}' usada sem ter sido inicializada")
        return s

    # ---- expressões: devolvem o tipo (ou ERRO) ----
    def _tipo(self, e):
        if isinstance(e, Literal):
            return e.tipo
        if isinstance(e, Var):
            s = self._usar(e.nome, e.linha, leitura=True)
            return s.tipo if s else ERRO
        if isinstance(e, UnOp):
            t = self._tipo(e.operando)
            if t == ERRO:
                return ERRO
            if e.op == "-":
                if t in NUMERICOS:
                    return t
                self.erro(e.linha, f"operador '-' unário exige tuta ou reala, encontrado {t}")
            else:  # ne
                if t == "bolea":
                    return "bolea"
                self.erro(e.linha, f"operador 'ne' exige bolea, encontrado {t}")
            return ERRO
        if isinstance(e, BinOp):
            return self._binop(e)
        return ERRO

    def _binop(self, e):
        te, td = self._tipo(e.esq), self._tipo(e.dir)
        if ERRO in (te, td):
            return ERRO
        op = e.op
        if op in ("+", "-", "*", "/"):
            if te in NUMERICOS and td in NUMERICOS:
                if op == "/" and isinstance(e.dir, Literal) and e.dir.tipo in NUMERICOS \
                        and float(e.dir.valor) == 0:
                    self.erro(e.linha, "divisão por zero")
                    return ERRO
                return "reala" if "reala" in (te, td) else "tuta"
            self.erro(e.linha, f"operador '{op}' exige operandos numéricos, encontrado {te} e {td}")
            return ERRO
        if op in ("e", "au"):
            if te == td == "bolea":
                return "bolea"
            self.erro(e.linha, f"operador '{op}' exige operandos bolea, encontrado {te} e {td}")
            return ERRO
        # relacionais
        if op in ("==", "!="):
            ok = (te in NUMERICOS and td in NUMERICOS) or te == td
        else:  # > <
            ok = (te in NUMERICOS and td in NUMERICOS) or te == td == "karaktero"
        if ok:
            return "bolea"
        self.erro(e.linha, f"operador '{op}' não se aplica a {te} e {td}")
        return ERRO


def analisar_arquivo(caminho, mostrar_ast=False):
    raiz, erros_lex, erros_sint = analisador_sintatico(caminho)
    if erros_lex or erros_sint:
        print("\nAnálise semântica não executada: corrija os erros léxicos/sintáticos.")
        return False

    ast = construir_ast(raiz)
    if mostrar_ast:
        print("\nAST:")
        imprimir_ast(ast)

    sem = AnalisadorSemantico()
    ok = sem.analisar(ast)

    sem.tabela.imprimir()
    if sem.avisos:
        print(f"\n{len(sem.avisos)} aviso(s):")
        for a in sem.avisos:
            print("  -", a)
    if ok:
        print("\nSUCESSO: Nenhum erro semântico encontrado!")
    else:
        print(f"\nFALHA: {len(sem.erros)} erro(s) semântico(s):")
        for e in sem.erros:
            print("  -", e)
    return ok


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    analisar_arquivo(args[0] if args else "teste_valido.esp", "--ast" in sys.argv)
