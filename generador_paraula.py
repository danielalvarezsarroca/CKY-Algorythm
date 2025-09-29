import random

class ParaulaAleatoria:
    """
    Classe per a la generació de paraules (cadenes) a partir d'una gramàtica.
    Pot generar paraules que pertanyen o no pertanyen al llenguatge de la gramàtica donada.
    """

    def __init__(self, regles, probabilistica=False, simbol_inicial="S", profunditat_max=15, max_len=8):
        """
        Inicialitza el generador de paraules.

        :param regles: Llista de regles de la gramàtica (tuples del tipus (capçalera, [cos])).
        :param probabilistica: Booleà, indica si la gramàtica és probabilística (no es fa servir directament aquí).
        :param simbol_inicial: Símbol inicial per començar la generació (per defecte "S").
        :param profunditat_max: Profunditat màxima de recursió per evitar bucles infinits.
        :param max_len: Longitud màxima de la paraula generada.
        """
        self.regles = regles
        self.es_prob = probabilistica
        self.inici = simbol_inicial
        self.profunditat_max = profunditat_max
        self.max_len = max_len

    def crea_paraula(self, ha_de_pertanye=True, min_len=2):
        """
        Genera una paraula segons la gramàtica. Pot ser que pertanyi o no al llenguatge.

        :param ha_de_pertanye: Si True, genera una paraula vàlida segons la gramàtica. Si False, una invàlida.
        :param min_len: Longitud mínima preferida de la paraula.
        :return: Cadena amb la paraula generada, o "" si no se n'ha pogut generar cap.
        """
        if ha_de_pertanye:
            # Intentar generar paraules més llargues primer
            for target_len in [3, 4, 2, 5]:
                for _ in range(50):
                    paraula = self._construeix_amb_preferencia(self.inici, 0, target_len)
                    if paraula and min_len <= len(paraula) <= self.max_len:
                        return paraula

            # Si no funciona, provar qualsevol longitud vàlida
            for _ in range(100):
                paraula = self._construeix(self.inici, 0)
                if paraula and min_len <= len(paraula) <= self.max_len:
                    return paraula
            return ""
        else:
            # Genera una paraula vàlida i la modifica per fer-la invàlida
            base = ""
            for _ in range(100):
                base = self._construeix(self.inici, 0)
                if base and min_len <= len(base) <= self.max_len:
                    break

            if not base:
                return ''
            return self._modificar_paraula(base)

    def _construeix_amb_preferencia(self, simbol, profunditat, target_len):
        """
        Construeix una paraula intentant aconseguir una longitud objectiu.

        :param simbol: Símbol des d'on expandir.
        :param profunditat: Profunditat actual de la recursió.
        :param target_len: Longitud objectiu de la paraula.
        :return: Paraula generada (string), o '' si no s'ha pogut generar.
        """
        if profunditat > self.profunditat_max:
            return ''

        matches = [r for r in self.regles if r[0] == simbol]
        if not matches:
            return ''

        # Estratègia per llargada objectiu i profunditat
        if target_len > 2 and profunditat < 3:
            # Prioritzar regles binàries
            binary_rules = [r for r in matches if len(r[1]) == 2 and all(s.isupper() for s in r[1])]
            if binary_rules:
                matches = binary_rules
        elif target_len <= 2 or profunditat >= 3:
            # Prioritzar regles terminals
            terminal_rules = [r for r in matches if len(r[1]) == 1 and r[1][0].islower()]
            if terminal_rules:
                matches = terminal_rules

        cos = random.choice(matches)[1]
        return self._expandir_cos(cos, profunditat, target_len)

    def _construeix(self, simbol, profunditat):
        """
        Construcció normal sense preferència de longitud.

        :param simbol: Símbol d'expansió.
        :param profunditat: Profunditat actual de la recursió.
        :return: Paraula generada (string) o '' si no es pot.
        """
        if profunditat > self.profunditat_max:
            return ''

        matches = [r for r in self.regles if r[0] == simbol]
        if not matches:
            return ''
        # Liger biaix a regles binàries a profunditat baixa
        if profunditat < 2 and random.random() < 0.6:
            binary_rules = [r for r in matches if len(r[1]) == 2]
            if binary_rules:
                matches = binary_rules

        cos = random.choice(matches)[1]
        return self._expandir_cos(cos, profunditat)

    def _expandir_cos(self, cos, profunditat, target_len=None):
        """
        Expandeix el cos d'una regla recursivament.

        :param cos: Llista de símbols a expandir.
        :param profunditat: Profunditat actual.
        :param target_len: Longitud objectiu (opcional).
        :return: Paraula generada (string), o '' si no és vàlid.
        """
        paraula = ''
        for part in cos:
            if part == '':
                continue
            elif part.islower():
                paraula += part
            else:
                if target_len is not None:
                    sub_paraula = self._construeix_amb_preferencia(part, profunditat + 1, target_len)
                else:
                    sub_paraula = self._construeix(part, profunditat + 1)
                if sub_paraula is None:
                    return ''
                paraula += sub_paraula
                if len(paraula) > self.max_len:
                    return ''
        return paraula

    def _modificar_paraula(self, base):
        """
        Modifica una paraula vàlida per convertir-la en invàlida.

        :param base: Paraula vàlida.
        :return: Paraula invàlida (string).
        """
        if not base:
            return 'xyz'  # Paraula clarament invàlida
        # Canviar un caràcter
        if base:
            pos = random.randrange(len(base))
            all_letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
            available_chars = [c for c in all_letters if c != base[pos]]
            if available_chars:
                paraula_llista = list(base)
                paraula_llista[pos] = random.choice(available_chars)
                return ''.join(paraula_llista)
        # Altres modificacions si no ha funcionat
        modifications = [
            lambda w: w + random.choice(['x', 'y', 'z', 'q', 'w']),
            lambda w: random.choice(['x', 'y', 'z', 'q', 'w']) + w,
        ]
        mod = random.choice(modifications)
        return mod(base)
