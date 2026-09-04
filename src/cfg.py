try:
    from src.transform_to_cfg import CNF
except ImportError:
    from transform_to_cfg import CNF

class CFG:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.reglas = self.analizar_gramatica(gramatica)
        self.tiene_vacia = any('' in v for v in self.reglas.values() if 'S' in self.reglas)
        self.es_cnf = self.comprobar_si_cnf()
        if not self.es_cnf:
            self.gramatica_cnf = CNF(self.reglas).convertir()
        else:
            self.gramatica_cnf = self.reglas

    def analizar_gramatica(self, grammar):
        rules = {}
        for rule in grammar:
            if '->' not in rule:
                continue
            lhs, rhs = rule.split("->")
            lhs = lhs.strip()
            rhs_alts = [r.strip().replace("ε", "") for r in rhs.split("|")]
            rules.setdefault(lhs, []).extend(rhs_alts)
        return rules

    def comprobar_si_cnf(self):
        for izquierda, lista_derecha in self.reglas.items():
            for derecha in lista_derecha:
                if derecha == '':
                    if izquierda != 'S':  # Solo se permite ε en S
                        return False
                    continue  # ε en S está permitido
                if len(derecha) == 1:
                    if not derecha.islower():  # Debe ser terminal
                        return False
                elif len(derecha) == 2:
                    if not (derecha[0].isupper() and derecha[1].isupper()):  # Dos no terminales
                        return False
                else:
                    return False
        return True

    def cky(self, palabra):
        reglas = self.gramatica_cnf
        n = len(palabra)

        # Caso especial: palabra vacía
        if n == 0:
            # Devuelve True si S -> '' está en la gramática
            return ['' in reglas.get('S', []), []]

        # Inicializar tabla triangular
        tabla = [[set() for _ in range(n)] for _ in range(n)]

        # Paso 1: Llenar diagonal con terminales
        for i in range(n):
            for nt, producciones in reglas.items():
                for prod in producciones:
                    if prod == palabra[i]:
                        tabla[i][i].add(nt)

        # Paso 2: Rellenar tabla con combinaciones binarias
        for l in range(2, n+1):
            for i in range(n-l+1):
                j = i + l - 1
                for k in range(i, j):
                    for nt, producciones in reglas.items():
                        for prod in producciones:
                            if len(prod) == 2:
                                B, C = prod[0], prod[1]
                                if B in tabla[i][k] and C in tabla[k+1][j]:
                                    tabla[i][j].add(nt)

        return ['S' in tabla[0][n-1], tabla]
