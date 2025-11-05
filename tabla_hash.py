# ===============================================
# Módulo: Tabla Hash con Encadenamiento
# ===============================================

class NodoHash:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None

class TablaHash:
    def __init__(self, tamaño=31):
        self.tamaño = tamaño
        self.tabla = [None] * tamaño

    def funcion_multiplicacion(self, clave_ascii, A=0.61803, M=31):
        """Función hash con desplazamiento ASCII +32"""
        return int(M * ((clave_ascii * A) % 1)) + 32

    def insertar(self, clave, valor, A=0.61803):
        """Inserta una clave con encadenamiento"""
        indice = self.funcion_multiplicacion(ord(clave), A, self.tamaño)
        nuevo = NodoHash(clave, valor)

        if self.tabla[indice] is None:
            self.tabla[indice] = nuevo
        else:
            actual = self.tabla[indice]
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def mostrar(self):
        """Muestra el contenido de las cubetas"""
        print("===== TABLA HASH =====")
        for i in range(self.tamaño):
            print(f"Cubeta {i}:", end=" ")
            actual = self.tabla[i]
            if actual is None:
                print("vacía")
            else:
                while actual:
                    print(f"({actual.clave}:{actual.valor}) -> ", end="")
                    actual = actual.siguiente
                print("None")
        print("======================\n")
