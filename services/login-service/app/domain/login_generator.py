import re
import itertools

def validate_name(fullName: str) -> str:
    fullName = fullName.strip()
    if not fullName:
        raise ValueError("Nome completo é obrigatório!")

    if not re.fullmatch(r"[A-Za-z ]+", fullName):
        raise ValueError("Nome completo deve conter apenas letras de A-Z e espaços em branco(sem acentos/caracteres especiais)")

    fullName = re.sub(r"\s+", " ", fullName)
    return fullName.lower()


def generate_logins(fullName: str):
    name = validate_name(fullName)
    parts = [p for p in name.split(" ") if p]  
    first = parts[0]
    others = parts[1:] 

    all = "".join(parts)

    logins = []
    rep = set()

    def completa_login(cand):
        cand = cand[:7]                      
        fonte = itertools.cycle(all) 
        while len(cand) < 7:
            cand += next(fonte)             
        return cand

    def add(cand):
        cand = completa_login(cand)
        if cand not in rep:
            rep.add(cand)
            logins.append(cand)


    for other in others:
        add(first + other)

    add(first + "".join(p[0] for p in others))

    last = others[-1]

    for i in range(1, min(len(first), 6)):
        for name in others:
            add(first[:7 - i] + name[:i])
    

    add("".join(p[0] for p in parts[:-1]) + last)

    print(logins)

    return logins                                