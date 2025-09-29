def llegir_gramatica(path, probabilistica=False):
    """
    Llegeix una gramàtica (amb o sense probabilitats) d'un fitxer.
    - Si probabilistica=True, retorna: [ ((head, [body]), prob), ... ]
    - Si probabilistica=False, retorna: [ (head, [body]), ... ]
    """
    regles = []
    with open(path, 'r', encoding='utf-8') as f:
        for linia in f:
            linia = linia.strip()
            if not linia or linia.startswith('#'):
                continue
            if '→' in linia:
                esquerra, dreta = linia.split('→')
            elif '->' in linia:
                esquerra, dreta = linia.split('->')
            else:
                continue
            esquerra = esquerra.strip()
            dretes = dreta.split('|')
            for produccio in dretes:
                parts = produccio.strip().split()
                if probabilistica:
                    if len(parts) < 2:
                        continue  # línia mal formada
                    *simbols, prob = parts
                    if simbols == [] or simbols == ['ε']:
                        simbols = ['']
                    regles.append( ((esquerra, simbols), float(prob)) )
                else:
                    if parts == [] or parts == ['ε']:
                        simbols = ['']
                    else:
                        simbols = parts
                    regles.append( (esquerra, simbols) )
    return regles




def llegir_paraula(path):
    with open(path, 'r', encoding='utf-8') as f:
        paraula = list(f.read().strip())
    return paraula


