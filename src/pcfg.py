from collections import defaultdict

class PCFG:
    def __init__(self, reglas_gramatica):
        self.reglas, self.probabilidades = self.analizar_gramatica(reglas_gramatica)
        self.simbolo_inicial = 'S'
        self.es_cnf = self.es_cnf()

    def analizar_gramatica(self, lineas_gramatica):
        reglas = defaultdict(list)
        probabilidades = defaultdict(list)
        
        for linea in lineas_gramatica:
            if '->' not in linea:
                continue
                
            izquierda, derecha = linea.split('->')
            izquierda = izquierda.strip()
            
            producciones = [p.strip() for p in derecha.split('|') if p.strip()]
            
            for produccion in producciones:
                indice_abre = produccion.find('[')
                indice_cierra = produccion.find(']')
                
                if indice_abre != -1 and indice_cierra != -1 and indice_cierra > indice_abre:
                    prod = produccion[:indice_abre].strip()
                    prob_str = produccion[indice_abre+1:indice_cierra].strip()
                    if prob_str.replace('.', '', 1).isdigit():
                        prob = float(prob_str)
                    else:
                        prob = 1.0
                else:
                    prod = produccion
                    prob = 1.0
                
                reglas[izquierda].append(prod)
                probabilidades[izquierda].append(prob)
        
        return reglas, probabilidades

    def es_cnf(self):
        for izquierda, producciones in self.reglas.items():
            for prod in producciones:
                if prod == '':
                    continue
                if len(prod) == 1:
                    if not prod.islower():
                        return False
                elif len(prod) == 2:
                    if not (prod[0].isupper() and prod[1].isupper()):
                        return False
                else:
                    return False
        return True

    def cky(self, palabra):
        n = len(palabra)
        if n == 0:
            vacio_prob = next((prob for prod, prob in zip(
                self.reglas.get(self.simbolo_inicial, []),
                self.probabilidades.get(self.simbolo_inicial, []))
                if prod == ''), 0.0)
            return [vacio_prob > 0, vacio_prob]

        tabla = [[defaultdict(float) for _ in range(n)] for _ in range(n)]

        for i in range(n):
            char = palabra[i]
            for nt in self.reglas:
                for prod, prob in zip(self.reglas[nt], self.probabilidades[nt]):
                    if prod == char:
                        if prob > tabla[i][i][nt]:
                            tabla[i][i][nt] = prob

        for length in range(2, n+1):
            for i in range(n-length+1):
                j = i + length - 1
                for k in range(i, j):
                    for nt in self.reglas:
                        for prod, prob in zip(self.reglas[nt], self.probabilidades[nt]):
                            if len(prod) == 2:
                                B, C = prod[0], prod[1]
                                prob_actual = tabla[i][k].get(B, 0.0) * tabla[k+1][j].get(C, 0.0) * prob
                                if prob_actual > tabla[i][j][nt]:
                                    tabla[i][j][nt] = prob_actual

        prob_final = tabla[0][n-1].get(self.simbolo_inicial, 0.0)
        return [prob_final > 0, prob_final]