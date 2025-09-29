class CFGtoCNF:
    """
    Classe per convertir una gramàtica lliure de context (CFG) en Forma Normal de Chomsky (CNF).
    
    Aquesta classe implementa els passos clàssics: afegir nou símbol inicial, eliminar produccions lambda,
    eliminar unitàries, substituir terminals en produccions llargues i descompondre produccions llargues.
    """

    def __init__(self, rules, start='S'):
        """
        Inicialitza la gramàtica.

        :param rules: Llista de tuples, cada tupla és (no_terminal, [simbols_dreta]).
        :param start: Símbol inicial de la gramàtica (per defecte 'S').
        """
        self.cfg = list(rules)
        self.initial = start
        self.has_lambda_start = any(
            lhs == self.initial and rhs == [''] for lhs, rhs in self.cfg
        )

    def _is_cnf(self):
        """
        Comprova si la gramàtica actual està en forma normal de Chomsky (CNF).

        :return: True si està en CNF, False altrament.
        """
        for lhs, rhs in self.cfg:
            if lhs != self.initial and rhs == ['']:
                return False
            if len(rhs) == 1 and rhs[0].isupper():
                return False
            if len(rhs) == 2 and not all(s.isupper() for s in rhs):
                return False
            if len(rhs) > 2 or len(rhs) == 0:
                return False
        return True

    def add_new_start(self):
        """
        Garanteix que el símbol inicial no aparegui al cos de cap regla.
        Si cal, afegeix un nou símbol inicial que apunta a l'antic.
        """
        heads = {lhs for lhs, rhs in self.cfg}
        for lhs, rhs in self.cfg:
            if self.initial in rhs:
                new_start = self.initial + "_START"
                self.cfg = [(new_start, [self.initial])] + self.cfg
                self.initial = new_start
                break

    def remove_epsilon(self):
        """
        Elimina les produccions lambda (ε) i genera totes les combinacions correctes.
        Manté la possibilitat de lambda només per al símbol inicial si era possible a la gramàtica original.
        """
        nullable = set()
        # Troba no terminals que poden derivar ε
        for lhs, rhs in self.cfg:
            if rhs == [''] or rhs == []:
                nullable.add(lhs)

        # Propagació de nul·labilitat
        changed = True
        while changed:
            changed = False
            for lhs, rhs in self.cfg:
                if all(sym in nullable for sym in rhs) and lhs not in nullable:
                    nullable.add(lhs)
                    changed = True

        new_rules = []
        for lhs, rhs in self.cfg:
            if rhs == ['']:
                continue
            positions = [i for i, sym in enumerate(rhs) if sym in nullable]
            from itertools import product
            for bits in product([True, False], repeat=len(positions)):
                temp_rhs = rhs[:]
                for bit, pos in zip(bits, positions):
                    if bit:
                        temp_rhs[pos] = None
                new_rhs = [x for x in temp_rhs if x is not None]
                if new_rhs == []:
                    if lhs == self.initial and self.has_lambda_start:
                        new_rules.append((lhs, ['']))
                else:
                    if (lhs, new_rhs) not in self.cfg and (lhs, new_rhs) not in new_rules:
                        new_rules.append((lhs, new_rhs))
            if not positions and (lhs, rhs) not in new_rules:
                new_rules.append((lhs, rhs))

        self.cfg += new_rules
        # Elimina les regles λ (excepte si és l'inicial i la tenia originalment)
        self.cfg = [
            (lhs, rhs) for lhs, rhs in self.cfg
            if rhs != [''] or (lhs == self.initial and self.has_lambda_start)
        ]

    def eliminate_unary(self):
        """
        Elimina totes les produccions unitàries (del tipus A → B amb A, B no-terminals).
        Substitueix-les per produccions equivalents més llargues, si cal.
        """
        unit_pairs = set()
        for lhs, rhs in self.cfg:
            if len(rhs) == 1 and rhs[0].isupper():
                unit_pairs.add((lhs, rhs[0]))

        added = set()
        while unit_pairs:
            a, b = unit_pairs.pop()
            for lhs, rhs in self.cfg:
                if lhs == b and not (len(rhs) == 1 and rhs[0].isupper()):
                    if (a, tuple(rhs)) not in added and (a, rhs) not in self.cfg:
                        self.cfg.append((a, rhs))
                        added.add((a, tuple(rhs)))
                if lhs == b and len(rhs) == 1 and rhs[0].isupper():
                    if (a, rhs[0]) not in unit_pairs:
                        unit_pairs.add((a, rhs[0]))
        self.cfg = [
            (lhs, rhs) for lhs, rhs in self.cfg
            if not (len(rhs) == 1 and rhs[0].isupper())
        ]

    def split_terminals(self):
        """
        Substitueix terminals en produccions llargues (de 2 o més símbols)
        per no-terminals auxiliars, afegint les produccions corresponents.
        """
        aux_map = {}
        new_rules = []
        for i, (lhs, rhs) in enumerate(self.cfg):
            if len(rhs) >= 2:
                new_rhs = []
                for s in rhs:
                    if s.islower():
                        if s not in aux_map:
                            aux_sym = f"T_{s.upper()}"
                            aux_map[s] = aux_sym
                            new_rules.append((aux_sym, [s]))
                        new_rhs.append(aux_map[s])
                    else:
                        new_rhs.append(s)
                self.cfg[i] = (lhs, new_rhs)
        self.cfg += new_rules

    def break_long_productions(self):
        """
        Redueix totes les regles amb més de dos símbols en una cadena de regles binàries.
        """
        counter = 0
        new_cfg = []
        for lhs, rhs in self.cfg:
            if len(rhs) <= 2:
                new_cfg.append((lhs, rhs))
            else:
                prev_nt = lhs
                for i in range(len(rhs) - 2):
                    counter += 1
                    new_nt = f"Y{counter}"
                    new_cfg.append((prev_nt, [rhs[i], new_nt]))
                    prev_nt = new_nt
                new_cfg.append((prev_nt, rhs[-2:]))
        self.cfg = new_cfg

    def convert(self):
        """
        Executa tot el procés de conversió de CFG a CNF i retorna la nova llista de regles.

        :return: Llista de tuples (no_terminal, [simbols_dreta]) en Forma Normal de Chomsky.
        """
        self.add_new_start()
        self.remove_epsilon()
        self.eliminate_unary()
        self.split_terminals()
        self.break_long_productions()
        self.cfg = list(dict.fromkeys((lhs, tuple(rhs)) for lhs, rhs in self.cfg))
        self.cfg = [(lhs, list(rhs)) for lhs, rhs in self.cfg]

        return self.cfg

    def __str__(self):
        """
        Retorna la gramàtica en format llegible per consola o print.
        """
        return '\n'.join(f"{lhs} -> {' '.join(rhs)}" for lhs, rhs in self.cfg)
