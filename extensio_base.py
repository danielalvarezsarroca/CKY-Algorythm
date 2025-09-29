class CKY:
    """
    Implementació de l'algorisme CKY per reconeixement de llenguatges amb gramàtiques en Forma Normal de Chomsky (CNF).
    
    Aquesta classe permet comprovar si una paraula pertany al llenguatge generat per una gramàtica donada.
    """

    def __init__(self, rules, start_symbol='S'):
        '''
        Inicialitza el reconeixedor CKY.

        :param rules: Llista de tuples (no_terminal, [simbols_dreta]) que representen les regles de la gramàtica en CNF.
        :param start_symbol: Símbol inicial de la gramàtica (per defecte 'S').
        '''
        self.rules = rules
        self.start_symbol = start_symbol
        
        # Verificar si el símbol inicial pot generar epsilon
        self.start_generates_epsilon = any(
            lhs == start_symbol and rhs == [''] 
            for lhs, rhs in rules
        )

    def parse(self, paraula):
        '''
        Comprova si la paraula proporcionada pertany al llenguatge de la gramàtica.

        Aquesta versió crida internament `parse_quiet`. Mantinguda per compatibilitat i debug.

        :param paraula: Llista de símbols (caràcters) que formen la paraula a comprovar.
        :return: True si la paraula pertany al llenguatge, False altrament.
        '''
        return self.parse_quiet(paraula)

    def parse_quiet(self, paraula):
        '''
        Algorisme CKY sense missatges de debug.

        Omple la taula de programació dinàmica per a la paraula donada i comprova si el símbol inicial pot derivar-la.

        :param paraula: Llista de símbols (caràcters) de la paraula d'entrada.
        :return: True si la paraula pertany al llenguatge de la gramàtica, False en cas contrari.
        '''
        # Cas especial: paraula buida
        if len(paraula) == 0:
            return self.start_generates_epsilon
        
        n = len(paraula)
        table = [[set() for _ in range(n)] for _ in range(n)]

        # Omplir la diagonal (subcadenes de longitud 1)
        for i in range(n):
            simbol = paraula[i]
            for lhs, rhs in self.rules:
                if len(rhs) == 1 and rhs[0] == simbol and rhs[0].islower():
                    table[i][i].add(lhs)

        # Omplir la resta de la taula (subcadenes de longitud 2 a n)
        for longitud in range(2, n + 1):
            for i in range(n - longitud + 1):
                j = i + longitud - 1
                for k in range(i, j):
                    for lhs, rhs in self.rules:
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].add(lhs)

        return self.start_symbol in table[0][n-1]
