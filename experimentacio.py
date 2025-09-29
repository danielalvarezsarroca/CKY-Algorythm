import sys
import io
from generador_gramatiques import GrammarMaker
from generador_paraula import ParaulaAleatoria
from extensio_base import CKY
from extensio_1 import CFGtoCNF
from extensio_2 import ProbabilisticCKY
import random
import numpy as np

RANDOM_SEED = 1234

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

RESULTS_FILE = "jocs_de_proves3.txt"

def run_experiment(probabilistica, cnf, pertany, experiment_num):
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    print(f"\nEXPERIMENT {experiment_num}:")
    print(f"Probabilística: {probabilistica}")
    print(f"CNF: {cnf}")
    print(f"Paraula pertany: {pertany}")

    gm = GrammarMaker()
    gramatica = None
    simbol_inicial = "S"
    gramatica_transformada = None

    if probabilistica:
        # Gramàtica probabilística (sempre en CNF)
        gramatica = gm.crea_gramatica(en_cnf=True, probabilistica=True)
        print("\nGramàtica probabilística generada (CNF):")
        for (head, body), prob in gramatica:
            print(f"({head}, {body}) -> {prob:.4f}")
        # Trobar símbol inicial
        simbol_inicial = "S"
        for (head, body), prob in gramatica:
            if head == "S_START":
                simbol_inicial = head
                break
        if simbol_inicial == "S":
            for (head, body), prob in gramatica:
                if head in ["ST", "S"]:
                    simbol_inicial = head
                    break
        cky = ProbabilisticCKY(gramatica, start_symbol=simbol_inicial)
        generador = ParaulaAleatoria([x[0] for x in gramatica], simbol_inicial=simbol_inicial, max_len=8)
    else:
        # Gramàtica no probabilística
        gramatica = gm.crea_gramatica(en_cnf=cnf)
        print("\nGramàtica original generada:")
        for head, body in gramatica:
            print(f"({head}, {body})")
        if not cnf:
            convertidor = CFGtoCNF(gramatica)
            gramatica_transformada = convertidor.convert()
            print("\n--- S'ha convertit a CNF ---")
            print("Gramàtica transformada a CNF:")
            for head, body in gramatica_transformada:
                print(f"({head}, {body})")
            gramatica_cnf = gramatica_transformada
        else:
            gramatica_cnf = gramatica

        # Trobar símbol inicial
        simbol_inicial = "S"
        for r in gramatica_cnf:
            if r[0] == "S_START":
                simbol_inicial = r[0]
                break
        if simbol_inicial == "S":
            for r in gramatica_cnf:
                if r[0] in ["ST", "S"]:
                    simbol_inicial = r[0]
                    break
        cky = CKY(gramatica_cnf, start_symbol=simbol_inicial)
        generador = ParaulaAleatoria(gramatica_cnf, simbol_inicial=simbol_inicial, max_len=8)

    # Generar la paraula
    paraula = ""
    intents = 0
    if pertany:
        while paraula == "" and intents < 30:
            paraula = generador.crea_paraula(True, min_len=2)
            intents += 1
        if paraula == "":
            while paraula == "" and intents < 50:
                paraula = generador.crea_paraula(True, min_len=1)
                intents += 1
        if paraula == "":
            print("No s'ha pogut generar cap paraula vàlida.")
            sys.stdout = old_stdout
            return mystdout.getvalue()
    else:
        while paraula == "" and intents < 20:
            paraula = generador.crea_paraula(False)
            intents += 1
        if paraula == "":
            print("No s'ha pogut generar cap paraula invàlida.")
            sys.stdout = old_stdout
            return mystdout.getvalue()

    print(f"\nParaula generada: {paraula}")
    if probabilistica:
        resultat = cky.parse(list(paraula))
        if resultat is False or resultat == 0:
            print(f"La paraula **NO** pertany al llenguatge (probabilitat = 0)")
        else:
            print(f"Probabilitat d'aquesta paraula segons la gramàtica: {resultat}")
    else:
        resultat = cky.parse_quiet(list(paraula))
        print(f"La paraula pertany al llenguatge de la gramàtica: {resultat}")

    sys.stdout = old_stdout
    return mystdout.getvalue()

def main():
    from itertools import product
    combinacions = list(product([False, True], repeat=3))
    combinacions = [c for c in combinacions if not (c[0] and not c[1])]
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        for idx, (prob, cnf, pertany) in enumerate(combinacions, 1):
            result = run_experiment(prob, cnf, pertany, idx)
            f.write(result)
            f.write("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
