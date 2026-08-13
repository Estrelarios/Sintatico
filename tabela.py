TABELA_PARSING = {
    "PROGRAMA": {
        "precipa": ["}", "LISTACOMANDOS", "{", ")", "(", "precipa"]
    },
    "LISTACOMANDOS": {
        "tuta": ["LISTACOMANDOS", "COMANDO"],
        "reala": ["LISTACOMANDOS", "COMANDO"],
        "karaktero": ["LISTACOMANDOS", "COMANDO"],
        "bolea": ["LISTACOMANDOS", "COMANDO"],
        "id": ["LISTACOMANDOS", "COMANDO"],
        "se": ["LISTACOMANDOS", "COMANDO"],
        "dum": ["LISTACOMANDOS", "COMANDO"],
        "al": ["LISTACOMANDOS", "COMANDO"],
        "eniro": ["LISTACOMANDOS", "COMANDO"],
        "elijero": ["LISTACOMANDOS", "COMANDO"],
        "}": [] # Produção ε (vazia)
    },
    "COMANDO": {
        "tuta": ["DECLARACAO"], "reala": ["DECLARACAO"], "karaktero": ["DECLARACAO"], "bolea": ["DECLARACAO"],
        "id": ["ATRIBUICAO"],
        "se": ["COM_SE"],
        "dum": ["COM_DUM"],
        "al": ["COM_AL"],
        "eniro": ["COM_ENIRO"],
        "elijero": ["COM_ELIJERO"]
    },
    "BLOCO": {
        "{": ["}", "LISTACOMANDOS", "{"]
    },
    "DECLARACAO": {
        "tuta": ["RESTODECLARACAO", "id", "TIPO"],
        "reala": ["RESTODECLARACAO", "id", "TIPO"],
        "karaktero": ["RESTODECLARACAO", "id", "TIPO"],
        "bolea": ["RESTODECLARACAO", "id", "TIPO"]
    },
    "RESTODECLARACAO": {
        "=": [";", "EXPRESSAO", "="],
        ";": [";"]
    },
    "TIPO": {
        "tuta": ["tuta"], "reala": ["reala"], "karaktero": ["karaktero"], "bolea": ["bolea"]
    },
    "ATRIBUICAO": {
        "id": [";", "EXPRESSAO", "=", "id"]
    },
    "COM_SE": {
        "se": ["COM_SENE", "BLOCO", ")", "EXPRESSAO", "(", "se"]
    },
    "COM_SENE": {
        "se ne": ["BLOCO", "se ne"],
        "tuta": [], "reala": [], "karaktero": [], "bolea": [], "id": [], "se": [], "dum": [], "al": [], "eniro": [], "elijero": [], "}": [] # ε
    },
    "COM_DUM": {
        "dum": ["BLOCO", ")", "EXPRESSAO", "(", "dum"]
    },
    "COM_AL": {
        "al": ["BLOCO", ")", "ALATUALIZA", ";", "EXPRESSAO", ";", "ALINIT", "(", "al"]
    },
    "ALINIT": {
        "tuta": ["EXPRESSAO", "=", "id", "TIPO"], "reala": ["EXPRESSAO", "=", "id", "TIPO"],
        "karaktero": ["EXPRESSAO", "=", "id", "TIPO"], "bolea": ["EXPRESSAO", "=", "id", "TIPO"],
        "id": ["EXPRESSAO", "=", "id"]
    },
    "ALATUALIZA": {
        "id": ["EXPRESSAO", "=", "id"]
    },
    "COM_ENIRO": {
        "eniro": [";", ")", "id", "(", "eniro"]
    },
    "COM_ELIJERO": {
        "elijero": [";", ")", "id", "(", "elijero"]
    },

    "EXPRESSAO": {
        "id": ["EXPRESSAOLOGICA"], "num_int": ["EXPRESSAOLOGICA"], "num_real": ["EXPRESSAOLOGICA"], "caractere": ["EXPRESSAOLOGICA"],
        "vere": ["EXPRESSAOLOGICA"], "malvere": ["EXPRESSAOLOGICA"], "-": ["EXPRESSAOLOGICA"], "ne": ["EXPRESSAOLOGICA"], "(": ["EXPRESSAOLOGICA"]
    },
    "EXPRESSAOLOGICA": {
         "id": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"], "num_int": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"], 
         "num_real": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"], "caractere": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"],
         "vere": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"], "malvere": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"],
         "-": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"], "ne": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"], 
         "(": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL"]
    },
    "EXPRESSAOLOGICALINHA": {
        "e": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL", "OPLOGICO"], "au": ["EXPRESSAOLOGICALINHA", "EXPRESSAORELACIONAL", "OPLOGICO"],
        ";": [], ")": [] # ε
    },
    "OPLOGICO": { "e": ["e"], "au": ["au"] },
    
    "EXPRESSAORELACIONAL": {
         "id": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"], "num_int": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"],
         "num_real": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"], "caractere": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"],
         "vere": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"], "malvere": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"],
         "-": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"], "ne": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"], 
         "(": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA"]
    },
    "EXPRESSAORELACIONALLINHA": {
        "==": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA", "OPRELACIONAL"], "!=": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA", "OPRELACIONAL"],
        "<": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA", "OPRELACIONAL"], ">": ["EXPRESSAORELACIONALLINHA", "EXPRESSAOARITMETICA", "OPRELACIONAL"],
        ";": [], ")": [], "e": [], "au": [] # ε
    },
    "OPRELACIONAL": { "==": ["=="], "!=": ["!="], "<": ["<"], ">": [">"] },
    
    "EXPRESSAOARITMETICA": {
         "id": ["EXPRESSAOARITMETICALINHA", "TERMO"], "num_int": ["EXPRESSAOARITMETICALINHA", "TERMO"],
         "num_real": ["EXPRESSAOARITMETICALINHA", "TERMO"], "caractere": ["EXPRESSAOARITMETICALINHA", "TERMO"],
         "vere": ["EXPRESSAOARITMETICALINHA", "TERMO"], "malvere": ["EXPRESSAOARITMETICALINHA", "TERMO"],
         "-": ["EXPRESSAOARITMETICALINHA", "TERMO"], "ne": ["EXPRESSAOARITMETICALINHA", "TERMO"], 
         "(": ["EXPRESSAOARITMETICALINHA", "TERMO"]
    },
    "EXPRESSAOARITMETICALINHA": {
        "+": ["EXPRESSAOARITMETICALINHA", "TERMO", "+"], "-": ["EXPRESSAOARITMETICALINHA", "TERMO", "-"],
        ";": [], ")": [], "==": [], "!=": [], "<": [], ">": [], "e": [], "au": [] # ε
    },
    "TERMO": {
         "id": ["TERMOLINHA", "FATOR"], "num_int": ["TERMOLINHA", "FATOR"], "num_real": ["TERMOLINHA", "FATOR"],
         "caractere": ["TERMOLINHA", "FATOR"], "vere": ["TERMOLINHA", "FATOR"], "malvere": ["TERMOLINHA", "FATOR"],
         "-": ["TERMOLINHA", "FATOR"], "ne": ["TERMOLINHA", "FATOR"], "(": ["TERMOLINHA", "FATOR"]
    },
    "TERMOLINHA": {
        "*": ["TERMOLINHA", "FATOR", "*"], "/": ["TERMOLINHA", "FATOR", "/"],
        ";": [], ")": [], "+": [], "-": [], "==": [], "!=": [], "<": [], ">": [], "e": [], "au": [] # ε
    },
    "FATOR": {
        "id": ["id"], "num_int": ["num_int"], "num_real": ["num_real"], "caractere": ["caractere"],
        "vere": ["vere"], "malvere": ["malvere"], 
        "-": ["FATOR", "-"], "ne": ["FATOR", "ne"],
        "(": [")", "EXPRESSAO", "("]
    }
}

FOLLOWS = {
    "PROGRAMA": ["$"],
    "LISTACOMANDOS": ["}"],
    "COMANDO": ["tuta", "reala", "karaktero", "bolea", "id", "se", "dum", "al", "eniro", "elijero", "}"],
    "BLOCO": ["tuta", "reala", "karaktero", "bolea", "id", "se", "dum", "al", "eniro", "elijero", "se ne", "}"],
    "DECLARACAO": ["tuta", "reala", "karaktero", "bolea", "id", "se", "dum", "al", "eniro", "elijero", "}"],
    "EXPRESSAO": [";", ")"],
}