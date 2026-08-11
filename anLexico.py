import re
from collections import namedtuple

Token = namedtuple("Token", ["tipo", "lexema", "linha"])
Erro = namedtuple("Erro", ["linha", "erro", "tipo"])

TIPOS = ["tuta", "reala", "karaktero", "bolea"]
RESERVADAS = ["se", "se ne", "al", "dum", "precipa", "vere", "malvere", "eniro", "elijero"]
OP_ARIT = ["+", "-", "*", "/"]
OP_REL = ["==", "!=", ">", "<"]
OP_LOG = ["e", "au", "ne"]
OP_ATRIB = ["="]
DELIMITADORES = ["(", ")", "{", "}", ",", ";"]

# REGEX padrões
PADRAO = r"\bse\s+ne\b|'[^']'|\d+\.\d+|\d+|==|!=|[a-zA-Z_]\w*|[+\-*/=<>(),;{}]"
INCORRETO = r"\+\+|--"
CARACTERE = r"'[^']'"
REAL = r"\d+\.\d+"
ID = r"[a-zA-Z_]\w*"

def tokenizar(caminho):
    tokens = []
    erros = []

    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    linha_num = 0
    for linha_num, line in enumerate(linhas, start=1):

        # remove comentários
        if "//" in line:
            line = line.split("//")[0]
 
        # detectar operadores inválidos ++ e --
        for invalido in re.finditer(INCORRETO, line):
            erros.append(Erro(linha_num, invalido.group(0), "token_invalido"))

        # troca token invalido por espaco, para não atrapalhar outras detecções
        line = re.sub(INCORRETO, " ", line)

        encontrados = re.findall(PADRAO, line)

        # pegar tudo que não foi reconhecido
        resto = re.sub(PADRAO, " ", line)
        for erro in resto.split():
            erros.append(Erro(linha_num, erro, "token_invalido"))

        for lexema in encontrados:

            if lexema in TIPOS:
                tokens.append(Token("tipo", lexema, linha_num))

            elif lexema in RESERVADAS:
                tokens.append(Token("reservado", lexema, linha_num))

            elif lexema in OP_ARIT:
                tokens.append(Token("op_arit", lexema, linha_num))

            elif lexema in OP_REL:
                tokens.append(Token("op_rel", lexema, linha_num))

            elif lexema in OP_LOG:
                tokens.append(Token("op_log", lexema, linha_num))

            elif lexema in OP_ATRIB:
                tokens.append(Token("op_atrib", lexema, linha_num))

            elif lexema in DELIMITADORES:
                tokens.append(Token("delim", lexema, linha_num))

            elif re.match(REAL, lexema):
                tokens.append(Token("num_real", lexema, linha_num))

            elif lexema.isdigit():
                tokens.append(Token("num_int", lexema, linha_num))

            elif re.match(CARACTERE, lexema):
                tokens.append(Token("caractere", lexema, linha_num))

            elif re.match(ID, lexema):
                tokens.append(Token("id", lexema, linha_num))

            else:
                erros.append(Erro(linha_num, lexema, "desconhecido"))

    # adiciona token EOF no final
    tokens.append(Token("EOF", "$", linha_num + 1))
    return tokens, erros