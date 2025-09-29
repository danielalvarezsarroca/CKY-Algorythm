from extensio_base import CKY
from utils import llegir_gramatica, llegir_paraula
from extensio_1 import CFGtoCNF
from extensio_2 import ProbabilisticCKY
from generador_gramatiques import GrammarMaker
from generador_paraula import ParaulaAleatoria

def execucio_base():
    """
    Executa la comprovació de pertinença d'una paraula amb CKY sobre una gramàtica ja en CNF.
    Llegeix la gramàtica i la paraula dels fitxers corresponents, mostra les regles i informa
    si la paraula pertany al llenguatge.
    """
    print("\n--- Execució extensió base (CKY sobre CNF) ---")
    regles = llegir_gramatica("dades/gramatica2.txt")
    paraula = llegir_paraula("dades/paraula.txt")
    print("Regles:")
    for r in regles:
        print(r)
    cky = CKY(regles)
    resultat = cky.parse(paraula)
    print(f"\nParaula: {''.join(paraula)}")
    print("Pertany al llenguatge?", resultat)

def execucio_extensio1():
    """
    Executa la comprovació de pertinença de paraules a partir d'una gramàtica CFG,
    transformant-la prèviament a CNF i aplicant després CKY.
    Mostra la gramàtica original, la CNF obtinguda, i el resultat de la comprovació.
    """
    print("\n--- Execució extensió 1 (CFG → CNF → CKY) ---")
    regles_cfg = llegir_gramatica("dades/gramatica_cfg.txt")
    paraula = llegir_paraula("dades/paraula.txt")
    print("Gramàtica original (CFG):")
    for r in regles_cfg:
        print(r)
    convertidor = CFGtoCNF(regles_cfg)
    regles_cnf = convertidor.convert()
    print("\nGramàtica en CNF:")
    for r in regles_cnf:
        print(r)
    cky = CKY(regles_cnf)
    resultat = cky.parse(paraula)
    print(f"\nParaula: {''.join(paraula)}")
    print("Pertany al llenguatge?", resultat)

def execucio_extensio2():
    """
    Executa la comprovació probabilística (CKY probabilístic) d'una paraula sobre una
    gramàtica probabilística, llegida des de fitxer. Mostra la gramàtica i la probabilitat
    associada a la paraula generada.
    """
    print("\n--- Execució extensió 2 (CKY probabilístic) ---")
    regles = llegir_gramatica("dades/gramatica_probabilistica.txt", probabilistica=True)
    paraula = llegir_paraula("dades/paraula.txt")
    print("Gramàtica probabilística:")
    for r in regles:
        print(r)
    cky = ProbabilisticCKY(regles)
    resultat = cky.parse(paraula)
    if resultat is False:
        print(f"\nParaula: {''.join(paraula)}")
        print("La paraula **NO** pertany al llenguatge (probabilitat = 0)")
    else:
        print(f"\nParaula: {''.join(paraula)}")
        print(f"Probabilitat d'aquesta paraula segons la gramàtica: {resultat}")

def execucio_random():
    """
    Experimenta amb gramàtiques i paraules generades aleatòriament, preguntant a l'usuari
    si vol CFG/CNF o probabilística, i si vol una paraula que pertanyi o no al llenguatge.
    Mostra la gramàtica generada, la paraula i el resultat de la comprovació.
    """
    print("\n--- Experiment aleatori (gramàtica i paraula generades random) ---")
    gm = GrammarMaker()
    probabilistic = input("Vols gramàtica probabilística? (y/n): ").strip().lower() == "y"

    if probabilistic:
        # Genera directament CNF amb probabilitats
        gramatica_prob = gm.crea_gramatica(en_cnf=True, probabilistica=True)
        print("\nAquesta és la gramàtica probabilística:")
        for (head, body), prob in gramatica_prob:
            print(f"({head}, {body}) -> {prob:.4f}")

        # Detecta símbol inicial
        simbol_inicial = "S"
        for (head, body), prob in gramatica_prob:
            if head == "S_START":
                simbol_inicial = head
                break
        if simbol_inicial == "S":
            for (head, body), prob in gramatica_prob:
                if head in ["ST", "S"]:
                    simbol_inicial = head
                    break

        cky = ProbabilisticCKY(gramatica_prob, start_symbol=simbol_inicial)

        print("\nQuin tipus de paraula vols generar?")
        print("1. Que pertanyi al llenguatge")
        print("2. Que NO pertanyi")
        tipus = input("Selecciona 1 o 2: ").strip()

        generador = ParaulaAleatoria([x[0] for x in gramatica_prob], simbol_inicial=simbol_inicial, max_len=8)
        paraula = ""

        if tipus == "1":
            intents = 0
            while paraula == "" and intents < 30:
                paraula = generador.crea_paraula(True, min_len=2)
                intents += 1
            if paraula == "":
                print("Generant qualsevol paraula vàlida...")
                intents = 0
                while paraula == "" and intents < 20:
                    paraula = generador.crea_paraula(True, min_len=1)
                    intents += 1
            if paraula == "":
                print("No s'ha pogut generar cap paraula vàlida.")
                return

        elif tipus == "2":
            intents = 0
            while paraula == "" and intents < 20:
                paraula = generador.crea_paraula(False)
                intents += 1
            if paraula == "":
                print("No s'ha pogut generar cap paraula invàlida.")
                return

        else:
            print("Opció no vàlida. Sortint.")
            return

        resultat = cky.parse(list(paraula))
        if resultat is False or resultat == 0:
            print(f"\nAquesta és la paraula que es comprova: {paraula}")
            print("La paraula **NO** pertany al llenguatge (probabilitat = 0)")
        else:
            print(f"\nAquesta és la paraula que es comprova: {paraula}")
            print(f"Probabilitat d'aquesta paraula segons la gramàtica: {resultat}")

    else:
        # Procés clàssic: genera CFG/CNF segons li demanis a l’usuari (com abans)
        resposta = input("Vols la gramàtica en CNF? (y/n): ").strip().lower()
        cnf = resposta == "y"
        gramatica = gm.crea_gramatica(en_cnf=cnf)

        print("\nAquesta és la gramàtica original:")
        for head, body in gramatica:
            print(f"({head}, {body})")

        if not cnf:
            convertidor = CFGtoCNF(gramatica)
            gramatica_cnf = convertidor.convert()
            print("S'ha convertit a CNF amb èxit!")
            print("Aquesta és la gramàtica transformada:")
            for head, body in gramatica_cnf:
                print(f"({head}, {body})")
            gramatica = gramatica_cnf

        simbol_inicial = "S"
        for r in gramatica:
            if r[0] == "S_START":
                simbol_inicial = r[0]
                break
        if simbol_inicial == "S":
            for r in gramatica:
                if r[0] in ["ST", "S"]:
                    simbol_inicial = r[0]
                    break

        cky = CKY(gramatica, start_symbol=simbol_inicial)

        print("\nQuin tipus de paraula vols generar?")
        print("1. Que pertanyi al llenguatge")
        print("2. Que NO pertanyi")
        tipus = input("Selecciona 1 o 2: ").strip()

        generador = ParaulaAleatoria(gramatica, simbol_inicial=simbol_inicial, max_len=8)
        paraula = ""

        if tipus == "1":
            intents = 0
            while paraula == "" and intents < 30:
                paraula = generador.crea_paraula(True, min_len=2)
                intents += 1
            if paraula == "":
                print("Generant qualsevol paraula vàlida...")
                intents = 0
                while paraula == "" and intents < 20:
                    paraula = generador.crea_paraula(True, min_len=1)
                    intents += 1
            if paraula == "":
                print("No s'ha pogut generar cap paraula vàlida.")
                return

        elif tipus == "2":
            intents = 0
            while paraula == "" and intents < 20:
                paraula = generador.crea_paraula(False)
                intents += 1
            if paraula == "":
                print("No s'ha pogut generar cap paraula invàlida.")
                return

        else:
            print("Opció no vàlida. Sortint.")
            return

        resultat = cky.parse_quiet(list(paraula))

        print(f"Aquesta és la paraula que es comprova: {paraula}")
        print(f"La paraula pertany al llenguatge de la gramàtica:  {resultat}")

def mostra_exemples_pertanyents():
    """
    Mostra exemples de paraules generades que pertanyen al llenguatge, donada una gramàtica.
    Permet a l'usuari triar entre dues gramàtiques i generar tants exemples com vulgui.
    """
    print("\n--- EXEMPLES de paraules que pertanyen al llenguatge ---")
    print("Escull la gramàtica sobre la qual vols veure exemples:")
    print("1. dades/gramatica2.txt (CNF ja preparada)")
    print("2. dades/gramatica_cfg.txt (es transformarà a CNF primer)")
    opcio = input("Selecciona 1 o 2: ").strip()

    if opcio == "1":
        regles = llegir_gramatica("dades/gramatica2.txt")
        simbol_inicial = "S"
        for r in regles:
            if r[0] in ["S", "ST"]:
                simbol_inicial = r[0]
                break
    elif opcio == "2":
        regles_cfg = llegir_gramatica("dades/gramatica_cfg2.txt")
        convertidor = CFGtoCNF(regles_cfg)
        regles = convertidor.convert()
        simbol_inicial = "S"
        for r in regles:
            if r[0] in ["S", "ST"]:
                simbol_inicial = r[0]
                break
    else:
        print("Opció no vàlida.")
        return

    generador = ParaulaAleatoria(regles, simbol_inicial=simbol_inicial)
    num = input("Quants exemples vols veure? [default=5]: ").strip()
    try:
        n = int(num)
    except:
        n = 5

    print(f"\n{n} paraules generades que PERTANYEN al llenguatge:")
    paraules = set()
    intents = 0
    while len(paraules) < n and intents < 5 * n:
        p = generador.crea_paraula(True)
        if p != "":
            paraules.add(p)
        intents += 1
    for idx, p in enumerate(paraules, 1):
        print(f"{idx}. {p}")
    if not paraules:
        print("No s'ha pogut generar cap paraula. Potser la gramàtica només genera lambda.")

def main():
    """
    Menú principal d'execució de l'aplicació. Permet triar quina extensió o experiment executar.
    """
    print("Quina extensió vols executar?")
    print("1. Extensió base (CKY amb gramàtica CNF ja preparada)")
    print("2. Extensió 1 (Transformació CFG → CNF i CKY)")
    print("3. Extensió 2 (CKY probabilístic)")
    print("4. Experiment aleatori (generador de gramàtiques i paraules)")

    opcio = input("Selecciona 1, 2, 3 o 4: ").strip()
    if opcio == "1":
        execucio_base()
    elif opcio == "2":
        execucio_extensio1()
    elif opcio == "3":
        execucio_extensio2()
    elif opcio == "4":
        execucio_random()
    else:
        print("Opció no vàlida.")

if __name__ == "__main__":
    main()
