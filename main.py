import os
import sys

# Support importing from src directory
try:
    from src.cfg import CFG
    from src.pcfg import PCFG
except ImportError:
    from cfg import CFG
    from pcfg import PCFG

usar_pcky = True   # Cambiar a False para utilizar CFG estándar sin probabilidades


def leer_input(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        gramatica, palabras = [], []
        for linea in f:
            linea = linea.strip()
            if not linea:
                if gramatica and palabras:
                    data.append((gramatica, palabras))
                    gramatica, palabras = [], []
            elif '->' in linea:
                gramatica.append(linea)
            else:
                palabras.append('' if linea == 'ε' else linea)

        if gramatica and palabras:
            data.append((gramatica, palabras))
    return data


def formatear_reglas(reglas, es_pcfg=False, probabilidades=None):
    resultado = []
    for lhs, prods in reglas.items():
        producciones = []
        for i, prod in enumerate(prods):
            if es_pcfg and probabilidades:
                producciones.append(f"{prod} {probabilidades[lhs][i]}")
            else:
                producciones.append(prod)
        resultado.append(f"{lhs} -> {' | '.join(producciones)}")
    return resultado


def escribir_salida(output_path, resultados, es_pcfg=False):
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for gramatica, cnf_info, word_results in resultados:        
            if es_pcfg:
                if cnf_info['es_cnf']:
                    f.write("La gramatica ya esta en CNF\n\n")
                else:
                    f.write("La gramatica PCFG fue convertida a CNF\n\n")
                    f.write('\n'.join(cnf_info['reglas_cnf']) + '\n\n')
            else:
                if cnf_info:
                    f.write("Gramatica no esta en CNF\n")
                    f.write("Gramatica convertida a CNF:\n")
                    f.write('\n'.join(cnf_info) + '\n\n')
                else:
                    f.write("La gramatica ya esta en CNF\n")

            f.write("Resultados\n")
            for word, (aceptada, prob) in word_results:
                estado = "True" if aceptada else "False"
                if es_pcfg:
                    f.write(f"'{word}': {estado} (Probabilidad: {prob:.4f})\n")
                else:
                    visible = "ε" if word == '' else word
                    f.write(f"'{visible}': {estado}\n")

            f.write("\n")


def resolver_ruta(rel_folder, filename):
    """Resuelve la ruta buscando en la carpeta organizada o en el directorio raíz."""
    path_en_carpeta = os.path.join(rel_folder, filename)
    if os.path.exists(path_en_carpeta):
        return path_en_carpeta
    return filename


def main():
    if usar_pcky:
        input_path = resolver_ruta('data', 'input_PCKY.txt')
        output_path = os.path.join('output', 'output_PCKY.txt')
    else:   
        input_path = resolver_ruta('data', 'input.txt')
        output_path = os.path.join('output', 'output.txt')
    
    entradas = leer_input(input_path)
    resultados = []

    for gramatica, palabras in entradas:
        if usar_pcky:
            pcfg = PCFG(gramatica)
            cnf_info = {
                'es_cnf': pcfg.es_cnf,
                'reglas_cnf': formatear_reglas(pcfg.reglas, pcfg.probabilidades)
            }
            # cky devuelve (aceptada, probabilidad)
            resultados_palabras = [(w, pcfg.cky(w)) for w in palabras]
            resultados.append((gramatica, cnf_info, resultados_palabras))
        else:
            cfg = CFG(gramatica)
            reglas_formateadas = None
            if not cfg.es_cnf:
                reglas_formateadas = [
                    f"{lhs} -> {' | '.join(rhs)}" 
                    for lhs, rhs in cfg.gramatica_cnf.items()
                ]
            # Para CFG normal, mantenemos solo aceptación (probabilidad es 1 o 0)
            resultados_palabras = [(w, (cfg.cky(w)[0], 1.0 if cfg.cky(w)[0] else 0.0)) 
                                 for w in palabras]
            resultados.append((gramatica, reglas_formateadas, resultados_palabras))

    escribir_salida(output_path, resultados, usar_pcky)


if __name__ == "__main__":
    main()