from collections import defaultdict
from itertools import product

class CNF:
    def __init__(self, reglas):
        self.reglas = reglas
        self.no_terminales = set(reglas.keys())
        self.simbolo_inicial = 'S'
        self.nuevo_nt_counter = 0  

    def convertir(self):
        self.eliminar_producciones_vacias()
        self.eliminar_producciones_unitarias()
        self.eliminar_producciones_mixtas()
        self.dividir_producciones_largas()
        self.eliminar_no_generativos()  
        self.eliminar_no_alcanzables()  
        return self.obtener_reglas_finales()

    def eliminar_no_generativos(self):
        generativos = set()
        cambiado = True
        while cambiado:
            cambiado = False
            for nt, producciones in self.reglas.items():
                for prod in producciones:
                    if all(sim.islower() or sim in generativos for sim in prod):
                        if nt not in generativos:
                            generativos.add(nt)
                            cambiado = True
        
        nuevos_reglas = defaultdict(list)
        for nt in generativos:
            nuevos_reglas[nt] = [prod for prod in self.reglas[nt] 
                               if all(sim.islower() or sim in generativos for sim in prod)]
        self.reglas = nuevos_reglas
        self.no_terminales = generativos

    def eliminar_no_alcanzables(self):
        alcanzables = set()
        pila = [self.simbolo_inicial]
        while pila:
            nt = pila.pop()
            if nt not in alcanzables:
                alcanzables.add(nt)
            if nt in self.reglas:
                for prod in self.reglas[nt]:
                    for simbolo in prod:
                        if simbolo.isupper() and simbolo not in alcanzables:
                            pila.append(simbolo)
        
        nuevos_reglas = defaultdict(list)
        for nt in alcanzables:
            if nt in self.reglas:
                nuevos_reglas[nt] = self.reglas[nt]
        self.reglas = nuevos_reglas
        self.no_terminales = alcanzables

    def eliminar_producciones_vacias(self):
        anulables = set()
        cambiado = True
        while cambiado:
            cambiado = False
            for nt, producciones in self.reglas.items():
                if '' in producciones and nt not in anulables:
                    anulables.add(nt)
                    cambiado = True
                for prod in producciones:
                    if all(sim in anulables for sim in prod):
                        if nt not in anulables:
                            anulables.add(nt)
                            cambiado = True
        nuevas_reglas = defaultdict(list)
        for nt, producciones in self.reglas.items():
            for prod in producciones:
                if prod == '':
                    continue  
                self._agregar_combinaciones_sin_anulables(nt, prod, anulables, nuevas_reglas)
        self.reglas = nuevas_reglas

    def _agregar_combinaciones_sin_anulables(self, nt, prod, anulables, nuevas_reglas):
        simbolos = list(prod)
        indices_anulables = [i for i, simbolo in enumerate(simbolos) if simbolo in anulables]
        cantidad = len(indices_anulables)

        for seleccion in range(1 << cantidad):
            nueva_produccion = []
            for i, simbolo in enumerate(simbolos):
                if i in indices_anulables:
                    idx = indices_anulables.index(i)
                    if not (seleccion & (1 << idx)):
                        nueva_produccion.append(simbolo)
                else:
                    nueva_produccion.append(simbolo)
            nueva_produccion_str = ''.join(nueva_produccion)
            if nueva_produccion_str and nueva_produccion_str not in nuevas_reglas[nt]:
                nuevas_reglas[nt].append(nueva_produccion_str)

    def eliminar_producciones_unitarias(self):
        cambiado = True
        while cambiado:
            cambiado = False
            for nt in list(self.reglas.keys()):
                producciones = self.reglas[nt].copy()
                for prod in producciones:
                    if len(prod) == 1 and prod.isupper():  
                        if prod in self.reglas:
                            for prod_b in self.reglas[prod]:
                                if prod_b not in self.reglas[nt]:
                                    self.reglas[nt].append(prod_b)
                                    cambiado = True
                        if prod in self.reglas[nt]:
                            self.reglas[nt].remove(prod)

    def eliminar_producciones_mixtas(self):
        mapa_terminales = {}
        nuevas_reglas = defaultdict(list)
        for nt, producciones in self.reglas.items():
            for prod in producciones:
                if len(prod) == 1 and prod.islower():
                    nuevas_reglas[nt].append(prod)
                else:
                    nueva_prod = []
                    for sim in prod:
                        if sim.islower(): 
                            if sim not in mapa_terminales:
                                nuevo_nt = self.obtener_nuevo_no_terminal()
                                mapa_terminales[sim] = nuevo_nt
                                nuevas_reglas[nuevo_nt].append(sim)
                            nueva_prod.append(mapa_terminales[sim])
                        else:
                            nueva_prod.append(sim)
                    nuevas_reglas[nt].append(''.join(nueva_prod))
        self.reglas = nuevas_reglas

    def dividir_producciones_largas(self):
        nuevas_reglas = defaultdict(list)
        for nt, producciones in self.reglas.items():
            for prod in producciones:
                if len(prod) <= 2:
                    nuevas_reglas[nt].append(prod)
                else:
                    nt_actual = nt
                    restante = prod
                    while len(restante) > 2:
                        nuevo_nt = self.obtener_nuevo_no_terminal()
                        nuevas_reglas[nt_actual].append(restante[0] + nuevo_nt)
                        nt_actual = nuevo_nt
                        restante = restante[1:]
                    nuevas_reglas[nt_actual].append(restante)
        self.reglas = nuevas_reglas

    def obtener_nuevo_no_terminal(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for letra in letras:
            if letra not in self.no_terminales and letra != self.simbolo_inicial:
                self.no_terminales.add(letra)
                return letra

    def obtener_reglas_finales(self):
        reglas_finales = {}
        if self.simbolo_inicial in self.reglas:
            reglas_finales[self.simbolo_inicial] = self.reglas[self.simbolo_inicial]
        for nt in sorted(self.reglas.keys()):
            if nt != self.simbolo_inicial:
                reglas_finales[nt] = self.reglas[nt]
        return reglas_finales