#Este es un modelo híbirido y el que consideramos se hacer más a una frase coherente.

import math
import time

# ==============================================================
#                       CLASE BST
# ==============================================================
class BSTNode:
    def __init__(self, char, frequency=1):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, char):
        if self.root is None:
            self.root = BSTNode(char)
            return
        
        current = self.root
        while True:
            if char == current.char:
                current.frequency += 1
                return
            elif char < current.char:
                if current.left is None:
                    current.left = BSTNode(char)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(char)
                    return
                current = current.right
    
    def inorder_traversal(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is None:
            return result
        
        if node.left:
            self.inorder_traversal(node.left, result)
        result.append((node.char, node.frequency))
        if node.right:
            self.inorder_traversal(node.right, result)
        
        return result


# ==============================================================
#                   FUNCIONES HASH
# ==============================================================
def hash_multiplicacion(k, A, M=27):
    """Función hash por multiplicación"""
    return int(M * ((k * A) % 1))

def hash_division(k, M=27):
    """Función hash por división"""
    return k % M


# ==============================================================
#                   FRECUENCIAS ESPAÑOL (sin espacios)
# ==============================================================
# Orden aproximado de frecuencia en español sin espacios:
frecuencia_esp = ['e','a','o','s','n','r','i','d','l','c','t','u','m','p','b','g','v','y','q','h','f','z','j','ñ','x','k','w']


# ==============================================================
#                   ANÁLISIS DE FRECUENCIA
# ==============================================================
def analizar_frecuencia(mensaje):
    bst = BST()
    start_time = time.time()
    for char in mensaje:
        bst.insert(char)
    end_time = time.time()
    
    frecuencias = bst.inorder_traversal()
    frecuencias_ordenadas = sorted(frecuencias, key=lambda x: x[1], reverse=True)
    return frecuencias_ordenadas, end_time - start_time


# ==============================================================
#               MAPEADO COMBINADO DE HASHES
# ==============================================================
def generar_tabla_hash_combinada(A=0.61803, M=27):
    """Genera una tabla combinada de índices hash (mult + div)"""
    alfabeto = "abcdefghijklmnñopqrstuvwxyz"
    tabla = {}
    for i, letra in enumerate(alfabeto):
        h_mult = hash_multiplicacion(i, A, M)
        h_div  = hash_division(i, M)
        tabla[letra] = (h_mult, h_div)
    return tabla


# ==============================================================
#                DESCIFRADO BASADO EN FRECUENCIAS
# ==============================================================
def descifrar_por_frecuencia(mensaje_cifrado, tabla_hash, frecuencias_cifrado):
    """Compara frecuencias y genera mapeo probable"""
    
    # Ordenamos los símbolos del cifrado por frecuencia
    simbolos_ordenados = [c for c, _ in frecuencias_cifrado]
    
    # Mapear letras comunes (más frecuentes en español)
    mapeo_aproximado = {}
    for i, simbolo in enumerate(simbolos_ordenados):
        if i < len(frecuencia_esp):
            mapeo_aproximado[simbolo] = frecuencia_esp[i]
    
    # Reconstruir texto aproximado
    texto_descifrado = "".join([mapeo_aproximado.get(c, '?') for c in mensaje_cifrado])
    
    return texto_descifrado, mapeo_aproximado


# ==============================================================
#                         MAIN
# ==============================================================
mensaje_cifrado = "(/-.-4%(+28.%#+2/($(6(#(3(8%.-/2(+(/(6.("

# 1Analizar frecuencias con BST
frecuencias_cifrado, tiempo_bst = analizar_frecuencia(mensaje_cifrado)
print("=== FRECUENCIAS EN MENSAJE CIFRADO ===")
for char, freq in frecuencias_cifrado:
    print(f"'{char}': {freq}")
print(f"Tiempo BST: {tiempo_bst:.6f}s")

# 2Generar tabla combinada (multiplicación + división)
phi = (math.sqrt(5) - 1) / 2
tabla_hash = generar_tabla_hash_combinada(phi)

# 3Descifrar por frecuencia
mensaje_descifrado, mapeo = descifrar_por_frecuencia(mensaje_cifrado, tabla_hash, frecuencias_cifrado)

# 4Mostrar resultados
print("\n=== POSIBLE MAPEADO (POR FRECUENCIAS) ===")
for simb, letra in mapeo.items():
    print(f"'{simb}' → '{letra}'")

print("\n=== MENSAJE DESCIFRADO APROXIMADO ===")
print(mensaje_descifrado)

# 5Mostrar tabla combinada (solo para análisis)
print("\n=== TABLA HASH (MULT + DIV) ===")
for letra, (h1, h2) in tabla_hash.items():
    print(f"{letra}: mult={h1}, div={h2}")
