"""Tabela de símbolos com escopos aninhados (pilha de dicionários)."""
from dataclasses import dataclass


@dataclass
class Simbolo:
    nome: str
    tipo: str
    linha: int
    escopo: int                 # nível de aninhamento (0 = bloco de precipa)
    inicializada: bool = False
    usada: bool = False


class TabelaSimbolos:
    def __init__(self):
        self._escopos = []      # pilha de {nome: Simbolo}
        self.historico = []     # todos os símbolos já declarados, na ordem (para relatório)

    @property
    def nivel(self):
        return len(self._escopos) - 1

    def entrar_escopo(self):
        self._escopos.append({})

    def sair_escopo(self):
        """Fecha o escopo e devolve os símbolos que ele continha."""
        return list(self._escopos.pop().values())

    def declarar(self, nome, tipo, linha, inicializada=False):
        """Retorna o Simbolo criado, ou None se já existe no escopo atual."""
        if nome in self._escopos[-1]:
            return None
        simbolo = Simbolo(nome, tipo, linha, self.nivel, inicializada)
        self._escopos[-1][nome] = simbolo
        self.historico.append(simbolo)
        return simbolo

    def buscar(self, nome):
        """Procura do escopo mais interno para o mais externo."""
        for escopo in reversed(self._escopos):
            if nome in escopo:
                return escopo[nome]
        return None

    def imprimir(self):
        print("\nTabela de símbolos:")
        print(f"  {'nome':<12}{'tipo':<12}{'linha':<7}{'escopo':<8}{'init':<6}usada")
        for s in self.historico:
            print(f"  {s.nome:<12}{s.tipo:<12}{s.linha:<7}{s.escopo:<8}"
                  f"{'sim' if s.inicializada else 'não':<6}{'sim' if s.usada else 'não'}")
