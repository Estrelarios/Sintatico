import string
import re

tipos = ["tuta", "reala", "karaktero", "bolea"]

reservados = ["se", "se ne", "al", "dum", "precipa", "reveno", "vere", "malvere", "eniro", "elijero"]

op_arit = ["+", "-", "*", "/"]
op_rel = ["==", "!=", ">", "<"]
op_log = ["e", "au", "ne"]
op_atrib = ["="]

par_esq = ["("]
par_dir = [")"]
chave_esq = ["{"]
chave_dir = ["}"]
virgula = [","]
ponto_virgula = [";"]

tokens = []

# regex de tokenização
padrao = r"\bse\s+ne\b|'[^']'|\d+\.\d+|\d+|==|!=|[a-zA-Z_]\w*|[+\-*/=<>(),;{}]"



f = open("Codigo.esp", "r")

for line in f:

    # remove comentarios
    if "//" in line:
        line = line.split("//")[0]

    encontrados = re.findall(padrao, line)

    i = 0
    while i < len(encontrados):

        token = encontrados[i]

        # tipos
        if token in tipos:
            tokens.append(["tipo", token])

        # reservados
        elif token in reservados:
            tokens.append(["reservado", token])

        # operadores
        elif token in op_arit:
            tokens.append(["op_arit", token])

        elif token in op_rel:
            tokens.append(["op_rel", token])

        elif token in op_log:
            tokens.append(["op_log", token])

        elif token in op_atrib:
            tokens.append(["op_atri", token])

        # delimitadores
        elif token in par_esq:
            tokens.append([token])

        elif token in par_dir:
            tokens.append([token])

        elif token in chave_esq:
            tokens.append([token])

        elif token in chave_dir:
            tokens.append([token])

        elif token in virgula:
            tokens.append([token])

        elif token in ponto_virgula:
            tokens.append([token])

        # numeros e caractere
        elif re.match(r'^\d+\.\d+$', token):
            tokens.append(["num_real", token])

        elif re.match(r"^'[^']'$", token):
            tokens.append(["caractere", token])

        elif token.isdigit():
            tokens.append(["num_int", token])

        # identificadores
        else:
            tokens.append(["id", token])

        i += 1

f.close()

for t in tokens:
    print(t)