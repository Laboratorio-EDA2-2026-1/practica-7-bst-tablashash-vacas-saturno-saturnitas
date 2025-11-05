# ===============================================
# PRÁCTICA: CRIPTOANÁLISIS EN CAMPO
# Estructuras: Árbol Binario de Búsqueda (BST) y Tabla Hash
# Alumno: [Tu nombre]
# Profesor: Luis Ricardo López Villafañán
# Materia: EDA II
# ===============================================

import time
import math

# ===============================================
# CLASE NODO Y BST
# ===============================================
class NodoBST:
    def __init__(self, clave):
        self.clave = clave          # carácter cifrado
        self.frecuencia = 1         # número de repeticiones
        self.izq = None
        self.der = None

class BST:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave):
        """Inserta un carácter en el BST o aumenta su frecuencia"""
        self.raiz = self._insertar_recursivo(self.raiz, clave)

    def _insertar_recursivo(self, nodo, clave):
        if nodo is None:
            return NodoBST(clave)
        if clave == nodo.clave:
            nodo.frecuencia += 1
        elif clave < nodo.clave:
            nodo.izq = self._insertar_recursivo(nodo.izq, clave)
        else:
            nodo.der = self._insertar_recursivo(nodo.der, clave)
        return nodo

    def recorrido_inorden(self):
        """Devuelve lista [(clave, frecuencia)] ordenada alfabéticamente"""
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izq, resultado)
            resultado.append((nodo.clave, nodo.frecuencia))
            self._inorden(nodo.der, resultado)


# ===============================================
# FASE 1: ANÁLISIS DE FRECUENCIA
# ===============================================
def analizar_frecuencia(mensaje):
    """
    Inserta cada carácter cifrado en un BST y calcula las frecuencias.
    Devuelve lista ordenada por frecuencia descendente.
    """
    bst = BST()
    inicio = time.time()

    for c in mensaje:
        bst.insertar(c)

    fin = time.time()
    tiempo = fin - inicio

    lista = bst.recorrido_inorden()
    lista.sort(key=lambda x: x[1], reverse=True)

    print("\n📊 Frecuencias encontradas:")
    for c, f in lista:
        print(f"  {c}: {f}")

    print(f"\n⏱ Tiempo de ejecución (BST): {tiempo:.6f} s\n")
    return lista, tiempo


# ===============================================
# FASE 2: INGENIERÍA INVERSA (CONSTANTE A)
# ===============================================
def funcion_multiplicacion(k_ascii, A, M=31):
    """Función hash de multiplicación con desplazamiento ASCII +32"""
    return int(M * ((k_ascii * A) % 1)) + 32

def buscar_constante_A(par_clave, A_inicial=0.6, M=31):
    """
    Busca heurísticamente una constante A cercana a la proporción áurea
    que mantenga un patrón estable.
    """
    k_ascii = ord(par_clave)
    mejor_A = A_inicial
    mejor_valor = funcion_multiplicacion(k_ascii, mejor_A, M)

    for i in range(10000):
        A_prueba = 0.5 + i * 0.00001
        valor = funcion_multiplicacion(k_ascii, A_prueba, M)
        if valor == mejor_valor:
            mejor_A = A_prueba
            break
    return mejor_A


# ===============================================
# FASE 3: DESCIFRADO FINAL
# ===============================================
def descifrar_mensaje(mensaje, mapeo):
    """
    Sustituye cada carácter cifrado por su correspondiente carácter original.
    """
    texto = ""
    for c in mensaje:
        if c in mapeo:
            texto += mapeo[c]
        else:
            texto += "?"  # si no se encontró mapeo
    return texto


# ===============================================
# PROGRAMA PRINCIPAL
# ===============================================
if __name__ == "__main__":
    mensaje_cifrado = "(/.-.-4%(+28.%#+2/($(6#(3(8%.-/2(+(/6.("

    print("========== FASE 1: ANALISIS DE FRECUENCIA ==========")
    frecuencias, tiempo = analizar_frecuencia(mensaje_cifrado)

    print("========== FASE 2: BUSQUEDA DE CONSTANTE A ==========")
    par_postulado = frecuencias[0][0]   # carácter más frecuente
    A = buscar_constante_A(par_postulado)
    print(f"Constante A encontrada ≈ {A:.5f}\n")

    # Frecuencias reales del mensaje original (del profe)
    frecuencias_reales = ['e', 't', 'a', 'o', 'u', 'r', 's', 'c', 'n', 'd', 'l', 'q', 'b', 'j']

    print("========== MAPEOS SUGERIDOS ==========")
    for i, (caracter, _) in enumerate(frecuencias):
        if i < len(frecuencias_reales):
            print(f"'{caracter}' → '{frecuencias_reales[i]}'")

    print("\n========== FASE 3: DESCIFRADO FINAL ==========")
    # Mapeo hipotético generado a partir de las frecuencias
    mapeo = {frecuencias[i][0]: frecuencias_reales[i] for i in range(min(len(frecuencias), len(frecuencias_reales)))}

    mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, mapeo)
    print("\nMensaje descifrado tentativo:\n", mensaje_descifrado)
