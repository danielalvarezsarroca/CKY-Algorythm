import random
from collections import defaultdict

class GrammarMaker:
    """
    Classe per a la generació automàtica de gramàtiques (CFG o CNF), 
    incloent la possibilitat d'assignar probabilitats.
    Permet controlar la recursivitat i la complexitat de les regles.
    """

    def __init__(self):
        """
        Inicialitza la instància de GrammarMaker. Prepara les estructures
        per guardar no-terminals, regles i terminals utilitzats.
        """
        self.nonterminals = set()
        self.regles = []
        self.terminals_used = set()

    def _nou_no_terminal(self):
        """
        Genera i retorna un nou símbol no-terminal del tipus X1, X2, ..., Xn.
        """
        for i in range(1, 100):
            nt = f"X{i}"
            if nt not in self.nonterminals:
                return nt
        return "X" + str(random.randint(100, 999))

    def _nou_terminal(self):
        """
        Retorna un nou símbol terminal aleatori entre les 26 lletres minúscules.
        """
        available = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        return random.choice(available)

    def _regla_cnf_recursiva(self, head):
        """
        Genera una regla de tipus CNF recursiva o terminal per al no-terminal especificat.

        :param head: Símbol no-terminal del cap de la regla.
        :return: Tuple (head, [cos])
        """
        if random.random() < 0.3:  # 30% terminals
            return (head, [self._nou_terminal()])
        else:
            existing_nts = list(self.nonterminals - {head})
            if len(existing_nts) >= 1 and random.random() < 0.8:
                if len(existing_nts) >= 2:
                    nt1, nt2 = random.sample(existing_nts, 2)
                else:
                    nt1 = random.choice(existing_nts)
                    nt2 = self._nou_no_terminal()
                    self.nonterminals.add(nt2)
            else:
                nt1 = self._nou_no_terminal()
                nt2 = self._nou_no_terminal()
                self.nonterminals.add(nt1)
                self.nonterminals.add(nt2)
            return (head, [nt1, nt2])

    def _regla_cfg_recursiva(self, head):
        """
        Genera una regla CFG recursiva per al no-terminal indicat, afavorint
        produccions més llargues i paraules més llargues.

        :param head: Símbol no-terminal del cap de la regla.
        :return: Tuple (head, [cos])
        """
        opciones = []
        if random.random() < 0.2:
            opciones.append([self._nou_terminal()])
        longitud = random.randint(2, 4)
        cos = []
        existing_nts = list(self.nonterminals - {head})
        for _ in range(longitud):
            if random.random() < 0.4:
                cos.append(self._nou_terminal())
            else:
                if existing_nts and random.random() < 0.7:
                    nt = random.choice(existing_nts)
                else:
                    nt = self._nou_no_terminal()
                    self.nonterminals.add(nt)
                cos.append(nt)
        opciones.append(cos)
        return (head, random.choice(opciones))

    def crea_gramatica_recursiva(self, en_cnf=True, num_regles=None, probabilistica=False):
        """
        Genera una gramàtica recursiva, en CNF o CFG, i opcionalment probabilística.

        :param en_cnf: Booleà, si True la gramàtica és en CNF, sinó en CFG.
        :param num_regles: Nombre de regles a generar (si None, aleatori dins d’un rang).
        :param probabilistica: Si True, assigna probabilitats a cada producció.
        :return: Llista de tuples (head, [cos]) o [ ((head, [cos]), prob), ... ]
        """
        if num_regles is None:
            num_regles = random.randint(4, 8)  

        self.nonterminals = set()
        self.regles = []
        self.terminals_used = set()
        self.nonterminals.add('S')

        # Regles inicials que afavoreixen recursivitat
        if en_cnf:
            nt1 = self._nou_no_terminal()
            nt2 = self._nou_no_terminal()
            self.nonterminals.add(nt1)
            self.nonterminals.add(nt2)
            self.regles.append(('S', [nt1, nt2]))
            self.regles.append(('S', [self._nou_terminal()]))
        else:
            self.regles.append(('S', [self._nou_terminal(), self._nou_terminal()]))
            nt1 = self._nou_no_terminal()
            self.nonterminals.add(nt1)
            self.regles.append(('S', [nt1, self._nou_terminal(), nt1]))

        regles_agregades = len(self.regles)
        while regles_agregades < num_regles:
            cap = random.choice(list(self.nonterminals))
            if en_cnf:
                regla = self._regla_cnf_recursiva(cap)
            else:
                regla = self._regla_cfg_recursiva(cap)
            if regla not in self.regles:
                self.regles.append(regla)
                regles_agregades += 1
                for simbol in regla[1]:
                    if simbol.isupper() and simbol != '':
                        self.nonterminals.add(simbol)

        # Garantir regla terminal per cada no-terminal
        for cap in list(self.nonterminals):
            has_terminal_rule = any(
                r[0] == cap and len(r[1]) == 1 and r[1][0].islower() 
                for r in self.regles
            )
            if not has_terminal_rule:
                terminal_rule = (cap, [self._nou_terminal()])
                if terminal_rule not in self.regles:
                    self.regles.append(terminal_rule)

        # Afegir recursives extra
        for _ in range(2):
            cap = random.choice(list(self.nonterminals))
            other_nt = random.choice(list(self.nonterminals - {cap}))
            if en_cnf:
                recursive_rule = (cap, [cap, other_nt])
            else:
                recursive_rule = (cap, [cap, self._nou_terminal(), other_nt])
            if recursive_rule not in self.regles:
                self.regles.append(recursive_rule)

        if not probabilistica:
            return self.regles
        else:
            # Assignar probabilitats
            cap_a_regles = defaultdict(list)
            for head, body in self.regles:
                cap_a_regles[head].append(body)
            regles_prob = []
            for head, bodys in cap_a_regles.items():
                probs = [random.random() for _ in bodys]
                total = sum(probs)
                probs = [p / total for p in probs]
                for body, prob in zip(bodys, probs):
                    regles_prob.append(((head, body), round(prob, 2)))
            return regles_prob

    def crea_gramatica(self, en_cnf=True, num_regles=None, probabilistica=False):
        """
        Genera una gramàtica amb la configuració desitjada.
        Aquest mètode només crida a crea_gramatica_recursiva.

        :param en_cnf: Si True, gramàtica en CNF.
        :param num_regles: Nombre de regles a generar.
        :param probabilistica: Si True, assigna probabilitats.
        :return: Llista de regles (veure crea_gramatica_recursiva).
        """
        return self.crea_gramatica_recursiva(en_cnf, num_regles, probabilistica)
