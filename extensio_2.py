class ProbabilisticCKY:
    """
    Implementació de l'algorisme CKY probabilístic (PCYK).

    Aquesta classe permet calcular la probabilitat que una paraula hagi estat generada per una gramàtica probabilística en CNF.
    """

    def __init__(self, grammar, start_symbol=None):
        """
        Inicialitza el reconeixedor CKY probabilístic.

        :param grammar: Llista de tuples de la forma ((no_terminal, [simbols_dreta]), probabilitat).
        :param start_symbol: Símbol inicial de la gramàtica (opcional, si no s'indica s'agafa el primer de la llista).
        """
        self.grammar = grammar
        self.rules_dict = self._build_rules_dict()
        if start_symbol is None:
            self.start_symbol, _ = self.grammar[0][0]
        else:
            self.start_symbol = start_symbol

    def _build_rules_dict(self):
        """
        Construeix un diccionari auxiliar per accedir ràpidament a la probabilitat de cada producció.

        :return: Diccionari de la forma {(no_terminal, tuple(simbols_dreta)): probabilitat}
        """
        rules_dict = {}
        for (head, body), prob in self.grammar:
            rules_dict[(head, tuple(body))] = prob
        return rules_dict

    def parse(self, word):
        """
        Aplica l'algorisme CKY probabilístic a una paraula per calcular la probabilitat que pertanyi al llenguatge de la gramàtica.

        :param word: Llista de símbols (caràcters) que formen la paraula d'entrada.
        :return: Probabilitat (float) si la paraula pertany al llenguatge, o False si la probabilitat és 0.
        """
        n = len(word)
        if n == 0:
            return 0.0

        table = [[dict() for _ in range(n + 1)] for _ in range(n)]

        # Omplim la diagonal (regles terminals)
        for i in range(n):
            for (A, body), prob in self.grammar:
                if len(body) == 1 and body[0] == word[i]:
                    table[i][i + 1][A] = max(table[i][i + 1].get(A, 0), prob)

        # Omplim la resta de la taula per subcadenes de longitud 2 a n
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l
                for k in range(i + 1, j):
                    for (A, body), prob in self.grammar:
                        if len(body) == 2:
                            B, C = body
                            prob_B = table[i][k].get(B, 0)
                            prob_C = table[k][j].get(C, 0)
                            if prob_B > 0 and prob_C > 0:
                                candidate = prob * prob_B * prob_C
                                table[i][j][A] = max(table[i][j].get(A, 0), candidate)

        probability = table[0][n].get(self.start_symbol, 0.0)
        return probability if probability > 0 else False
