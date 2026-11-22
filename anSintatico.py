from anLexico import tokenizar, Token
from tabela import TABELA_PARSING, FOLLOWS

class No:
    """Nó da árvore de derivação (parse tree).

    simbolo: nome do não-terminal ou do terminal esperado
    filhos:  lista de No (vazia para terminais e produções ε)
    token:   Token casado (somente para terminais)
    """
    def __init__(self, simbolo, token=None):
        self.simbolo = simbolo
        self.filhos = []
        self.token = token

    def __repr__(self):
        return f"No({self.simbolo})"

def eh_terminal(simbolo):
    return simbolo not in TABELA_PARSING

def get_chave(token):
    if token.tipo == "EOF": return "$"
    if token.tipo in ["id", "num_int", "num_real", "caractere"]: return token.tipo

    return token.lexema

def analisador_sintatico(caminho_fonte):
    tokens, erros_lex = tokenizar(caminho_fonte)

    # Printa todos os tokens recebidos do léxico

    # print("\nTokens:")
    # for token in tokens:
    #     print(f"  {token.tipo}: {token.lexema}")
    
    if erros_lex:
        print("Erros Léxicos:")
        for err in erros_lex: print(f"  Linha {err.linha}: {err.erro}")
    
    raiz = No("PROGRAMA")
    # a pilha guarda pares (simbolo, no) para montar a árvore durante a análise
    pilha = [("$", None), ("PROGRAMA", raiz)]
    index = 0
    erros_sintaticos = []
    primitivas_encontradas = set() 
    
    while len(pilha) > 0:
        topo, no_topo = pilha[-1]
        token_atual = tokens[index]
        chave = get_chave(token_atual)

        # controle das primitivas encontradas no código compilado, utilizado posteriormente para verificaçaõ
        if not eh_terminal(topo): 
            primitivas_encontradas.add(topo) 
        
        # 1. Sucesso
        if topo == chave:
            pilha.pop()
            if no_topo is not None:
                no_topo.token = token_atual
            index += 1
            
        # 2. Erro
        elif eh_terminal(topo):
            # Encontrei um terminal não esperado (não combina com o topo da pilha)
            erros_sintaticos.append(f"Linha {token_atual.linha}: Esperado '{topo}', encontrado '{token_atual.lexema}'")
            pilha.pop()
            
        # 3. Não-Terminal
        else:
            if chave in TABELA_PARSING.get(topo, {}):
                producao = TABELA_PARSING[topo][chave]
                pilha.pop()
                # a produção está invertida na tabela: filhos na ordem correta = reversed
                no_topo.filhos = [No(simbolo) for simbolo in reversed(producao)]
                for filho in reversed(no_topo.filhos):
                    pilha.append((filho.simbolo, filho))
            
            # 4. Modo pânico
            else:
                erros_sintaticos.append(f"Linha {token_atual.linha}: Inesperado '{token_atual.lexema}' lendo regra '{topo}'")
                
                follow_topo = FOLLOWS.get(topo, [";", "}"])
                print(f"   -> Modo Pânico: Ignorando tokens até encontrar {follow_topo}")
                
                while chave not in follow_topo and chave != "$":
                    index += 1
                    if index >= len(tokens): break
                    token_atual = tokens[index]
                    chave = get_chave(token_atual)
                
                pilha.pop()

    if not erros_sintaticos:
        print("\nSUCESSO: Nenhum erro sintático encontrado!")
    else:
        print(f"\nFALHA: {len(erros_sintaticos)} erro(s) sintático(s):")
        for err in erros_sintaticos:
            print("  -", err)

    # Testa se todas as primitivas foram encontradas no código compilado

    # todas_primitivas = set(TABELA_PARSING.keys())
    # primitivas_ausentes = todas_primitivas - primitivas_encontradas

    # if not primitivas_ausentes:
    #     print(f"\nTodas as {len(todas_primitivas)} primitivas foram encontradas no código.")
    #     print("Primitivas encontradas:")
    #     for p in primitivas_encontradas:
    #         print("  -", p)
    # else:
    #     print(f"\n{len(primitivas_ausentes)} de {len(todas_primitivas)} primitiva(s) não foram encontradas:")
    #     for p in primitivas_ausentes:
    #         print("  -", p)

    return raiz, erros_lex, erros_sintaticos

if __name__ == "__main__":
    # Crie um arquivo de teste "codigo_teste.txt" para rodar
    analisador_sintatico("teste_valido.esp")