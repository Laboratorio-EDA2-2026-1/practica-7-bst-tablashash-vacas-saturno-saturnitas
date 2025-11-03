# -*- coding: utf-8 -*-
"""
Práctica: BST y Tablas Hash (Criptoanálisis en campo)

Descripción:
 - Árbol Binario de Búsqueda (BST) para análisis de frecuencia
 - Funciones hash (multiplicación y módulo)
 - Búsqueda heurística de la constante A ≈ 0.61803
 - Descifrado combinado
 - Exportación de resultados (CSV y PDF)
"""

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from collections import Counter, defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import math, time, string, csv, os, zipfile

# ----------------------------------------------------------
# PARÁMETROS GLOBALES
# ----------------------------------------------------------
M = 31
A_SEED = 0.61803398875
CIPHERTEXT = "(/.-.-4%(+28.%#+2/($(6(#(3(8%.-/2(+(/(6.("
ALFABETO = " " + string.ascii_lowercase
SPANISH_PRIOR = " eaosrnidlctumpbgvyqhjzñxkw"

# ----------------------------------------------------------
# 1. ESTRUCTURA BST
# ----------------------------------------------------------
@dataclass
class NodoBST:
    clave: str
    freq: int = 1
    izq: Optional['NodoBST'] = None
    der: Optional['NodoBST'] = None

class BST:
    def __init__(self):
        self.raiz: Optional[NodoBST] = None

    def _insertar(self, nodo, clave):
        if nodo is None:
            return NodoBST(clave)
        if clave == nodo.clave:
            nodo.freq += 1
        elif clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave)
        else:
            nodo.der = self._insertar(nodo.der, clave)
        return nodo

    def insertar(self, clave):
        self.raiz = self._insertar(self.raiz, clave)

    def _inorden(self, nodo, acc):
        if nodo:
            self._inorden(nodo.izq, acc)
            acc.append((nodo.clave, nodo.freq))
            self._inorden(nodo.der, acc)

    def elementos(self):
        acc = []
        self._inorden(self.raiz, acc)
        return acc

# ----------------------------------------------------------
# 2. FUNCIONES HASH
# ----------------------------------------------------------
def hash_multiplicacion(k, A, M): return math.floor(M * ((k * A) % 1)) + 32
def hash_modulo(k, M): return (k % M) + 32

# ----------------------------------------------------------
# 3. MAPEOS Y UTILIDADES
# ----------------------------------------------------------
def construir_mapeos(A, M, alfabeto):
    mapA, mapM = {}, {}
    for ch in alfabeto:
        k = ord(ch)
        mapA[ch] = chr(hash_multiplicacion(k, A, M))
        mapM[ch] = chr(hash_modulo(k, M))
    return mapA, mapM

def invertir_mapeo(mapX):
    inv = defaultdict(list)
    for p, c in mapX.items():
        inv[c].append(p)
    return inv

# ----------------------------------------------------------
# 4. HEURÍSTICA PARA BUSCAR A
# ----------------------------------------------------------
def puntuar_A(A, M, alfabeto, vistos):
    mapA, mapM = construir_mapeos(A, M, alfabeto)
    posibles = set(mapA.values()) | set(mapM.values())
    cobertura = len(vistos & posibles) / max(1, len(vistos))
    colA = Counter(mapA.values())
    colM = Counter(mapM.values())
    colisiones = sum(1 for v in colA.values() if v > 1) + sum(1 for v in colM.values() if v > 1)
    return cobertura - 0.01 * colisiones

def buscar_A_mejor(M, alfabeto, cipher, semilla=A_SEED, radio=0.02, pasos=300):
    vistos = set(cipher)
    mejor_A, mejor_score = semilla, float("-inf")
    for i in range(pasos + 1):
        A = semilla - radio + (2 * radio) * (i / pasos)
        score = puntuar_A(A, M, alfabeto, vistos)
        if score > mejor_score:
            mejor_score, mejor_A = score, A
    return mejor_A

# ----------------------------------------------------------
# 5. DESCIFRADO
# ----------------------------------------------------------
def descifrar_con_mapa(cipher, invA, invM):
    out = []
    for ch in cipher:
        cands = set(invA.get(ch, [])) | set(invM.get(ch, []))
        if not cands:
            out.append('?'); continue
        if len(cands) == 1:
            out.append(next(iter(cands))); continue
        for p in SPANISH_PRIOR:
            if p in cands:
                out.append(p); break
    return ''.join(out)

# ----------------------------------------------------------
# 6. EXPORTACIONES (CSV / PDF)
# ----------------------------------------------------------
def exportar_csv(nombre, encabezados, filas):
    with open(nombre, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(encabezados)
        for fila in filas:
            writer.writerow(fila)

def exportar_pdf(A_mejor, tiempo, dec_comb, freq_list, mapeo_final):
    doc = SimpleDocTemplate("Reporte_Criptoanalisis.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Práctica: Estructuras BST y Tablas Hash (Criptoanálisis en campo)</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>1. Justificación del valor A</b>", styles["Heading2"]))
    story.append(Paragraph(f"Mediante un barrido heurístico en el rango [0.598, 0.638] se determinó que la constante de dispersión óptima es A ≈ {A_mejor:.8f}. Este valor maximiza la cobertura de símbolos del mensaje cifrado y minimiza las colisiones dentro de las funciones hash de multiplicación y módulo.", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>2. Tiempo de ejecución</b>", styles["Heading2"]))
    story.append(Paragraph(f"Tiempo medido para la función analizar_frecuencia(): {tiempo:.6f} segundos.", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>3. Resultado del descifrado final</b>", styles["Heading2"]))
    story.append(Paragraph(f"Mensaje descifrado reconstruido:<br/><b>{dec_comb}</b>", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>4. Frecuencias de caracteres cifrados</b>", styles["Heading2"]))
    tabla_freq = Table([["Carácter", "Frecuencia"]] + [[c, str(f)] for c, f in freq_list])
    tabla_freq.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.grey),
                                    ("GRID", (0,0), (-1,-1), 0.5, colors.black)]))
    story.append(tabla_freq)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>5. Mapeo cifrado → original</b>", styles["Heading2"]))
    tabla_m = Table([["Cifrado", "Original"]] + [[c, p] for c, p in mapeo_final.items()])
    tabla_m.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.black)]))
    story.append(tabla_m)

    doc.build(story)
    print("[PDF generado: Reporte_Criptoanalisis.pdf]")

# ----------------------------------------------------------
# 7. COMPRESIÓN FINAL
# ----------------------------------------------------------
def crear_zip():
    with zipfile.ZipFile("Entrega_Criptoanalisis.zip", "w") as z:
        for fname in ["frecuencias_BST.csv", "mapeo_final.csv", "Reporte_Criptoanalisis.pdf", __file__]:
            if os.path.exists(fname):
                z.write(fname)
    print("\n[ZIP creado: Entrega_Criptoanalisis.zip] ✅")

# ----------------------------------------------------------
# 8. PIPELINE PRINCIPAL
# ----------------------------------------------------------
def main():
    print("=== Fase 1: Análisis de Frecuencia con BST ===")
    bst = BST()
    t0 = time.perf_counter()
    for ch in CIPHERTEXT:
        bst.insertar(ch)
    t1 = time.perf_counter()
    tiempo_total = t1 - t0

    freq_list = sorted(bst.elementos(), key=lambda x: -x[1])
    exportar_csv("frecuencias_BST.csv", ["Carácter cifrado", "Frecuencia"], freq_list)

    print(f"[Tiempo analizar_frecuencia] {tiempo_total:.6f} s")

    print("\n=== Fase 2: Determinación de A ===")
    A_mejor = buscar_A_mejor(M, ALFABETO, CIPHERTEXT)
    print(f"A óptima encontrada: {A_mejor:.8f}")

    mapA, mapM = construir_mapeos(A_mejor, M, ALFABETO)
    invA, invM = invertir_mapeo(mapA), invertir_mapeo(mapM)

    print("\n=== Fase 3: Descifrado ===")
    dec_comb = descifrar_con_mapa(CIPHERTEXT, invA, invM)
    print(f"Mensaje descifrado: {dec_comb}")

    # Mapeo final para CSV
    mapeo_final = {}
    for c in sorted(set(CIPHERTEXT)):
        posibles = set(invA.get(c, [])) | set(invM.get(c, []))
        if not posibles:
            mapeo_final[c] = '?'
        else:
            for p in SPANISH_PRIOR:
                if p in posibles:
                    mapeo_final[c] = p
                    break

    exportar_csv("mapeo_final.csv", ["Carácter cifrado", "Carácter original"], list(mapeo_final.items()))
    exportar_pdf(A_mejor, tiempo_total, dec_comb, freq_list, mapeo_final)
    crear_zip()

    print("\nListo  Archivos generados:")
    print("1️ frecuencias_BST.csv")
    print("2️ mapeo_final.csv")
    print("3️ Reporte_Criptoanalisis.pdf")
    print("4️ Entrega_Criptoanalisis.zip")

if __name__ == "__main__":
    main()
