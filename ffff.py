#!/usr/bin/env python3
import sys
import tempfile
import os

def limpiar_archivo(archivo_entrada):
    """
    Elimina líneas en blanco del archivo (como awk 'NF')
    y guarda el resultado en un archivo temporal.
    """
    temp = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
    
    with open(archivo_entrada, 'r') as f:
        for linea in f:
            if linea.strip():
                temp.write(linea)
    
    temp.close()
    return temp.name

def encontrar_patron_7_posiciones(numeros):
    """
    Encuentra el patrón de agrupación basado en los primeros 7 números.
    Retorna un diccionario con los números de inicio y sus correspondientes
    números 7 posiciones después.
    """
    print("\n--- Analizando patrón con primeros 7 números ---")
    
    # Mostrar los primeros 7 números
    primeros_7 = numeros[:7]
    for i, num in enumerate(primeros_7, 1):
        print(f"  {i}. {num}")
    
    patrones = {}
    
    # Para cada uno de los primeros 7 números
    for i, num_inicio in enumerate(primeros_7):
        indices = []
        valores = []
        indice_actual = i  # Comenzar desde la posición actual
        
        while indice_actual < len(numeros):
            indices.append(indice_actual + 1)  # +1 para mostrar posición humana
            valores.append(numeros[indice_actual])
            indice_actual += 7
        
        patrones[num_inicio] = {
            'posiciones': indices,
            'valores': valores,
            'total': len(valores)
        }
    
    return patrones

def agrupar_numeros_por_patron(archivo):
    """
    Lee números de un archivo y los agrupa según el patrón de 7 posiciones
    basado en los primeros 7 números.
    """
    # Leer todos los números del archivo
    with open(archivo, 'r') as f:
        numeros = [linea.strip() for linea in f if linea.strip()]
    
    print(f"\n📊 Total de números después de limpiar: {len(numeros)}")
    
    if len(numeros) < 7:
        print("⚠️  Advertencia: Hay menos de 7 números en el archivo")
        return {}
    
    # Encontrar patrones basados en los primeros 7 números
    patrones = encontrar_patron_7_posiciones(numeros)
    
    return patrones

def mostrar_resultados(patrones):
    """
    Muestra los resultados de forma organizada.
    """
    print("\n" + "="*60)
    print("RESULTADOS DE AGRUPACIÓN POR PATRÓN (cada 7 posiciones)")
    print("="*60)
    
    for i, (num_inicio, info) in enumerate(patrones.items(), 1):
        print(f"\n📌 GRUPO {i} - Comenzando con: {num_inicio}")
        print("-" * 40)
        print(f"📍 Posiciones: {info['posiciones']}")
        print(f"📊 Valores: {info['valores']}")
        print(f"📈 Total en este grupo: {info['total']}")
        
        # Mostrar en formato más legible
        print("\n   Detalle:")
        for j, (pos, val) in enumerate(zip(info['posiciones'], info['valores']), 1):
            print(f"     {j:2d}. Pos {pos:2d}: {val}")
    
    # Resumen ejecutivo
    print("\n" + "="*60)
    print("📋 RESUMEN EJECUTIVO (Arrays en Python):")
    print("="*60)
    for i, (num_inicio, info) in enumerate(patrones.items(), 1):
        print(f"grupo_{i} = {info['valores']}  # desde {num_inicio}")

def guardar_resultados(patrones, archivo_salida="resultados_agrupacion.txt"):
    """
    Guarda los resultados en un archivo de texto.
    """
    with open(archivo_salida, 'w') as f:
        f.write("RESULTADOS DE AGRUPACIÓN POR PATRÓN (cada 7 posiciones)\n")
        f.write("="*60 + "\n\n")
        
        for i, (num_inicio, info) in enumerate(patrones.items(), 1):
            f.write(f"GRUPO {i} - Inicio: {num_inicio}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Posiciones: {info['posiciones']}\n")
            f.write(f"Valores: {info['valores']}\n")
            f.write(f"Cantidad: {info['total']}\n\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("ARRAYS EN PYTHON:\n")
        f.write("="*60 + "\n")
        for i, (num_inicio, info) in enumerate(patrones.items(), 1):
            f.write(f"grupo_{i} = {info['valores']}  # desde {num_inicio}\n")
    
    print(f"\n💾 Resultados guardados en: {archivo_salida}")

def main():
    # Configuración
    ARCHIVO = "asdas"  # Cambia esto por tu archivo
    GUARDAR_RESULTADOS = True  # Si quieres guardar en archivo
    
    print("="*60)
    print("🔍 ANALIZADOR DE PATRONES DE 7 POSICIONES")
    print("="*60)
    
    # Verificar que el archivo existe
    if not os.path.exists(ARCHIVO):
        print(f"❌ Error: No se encuentra el archivo '{ARCHIVO}'")
        print("   Asegúrate de que el archivo existe en el directorio actual")
        return
    
    print(f"\n📁 Procesando archivo: {ARCHIVO}")
    
    # Limpiar el archivo (eliminar líneas en blanco)
    print("\n🧹 Limpiando líneas en blanco...")
    archivo_limpio = limpiar_archivo(ARCHIVO)
    print("✅ Archivo limpio creado")
    
    # Analizar patrones
    print("\n🔎 Analizando patrones con los primeros 7 números...")
    patrones = agrupar_numeros_por_patron(archivo_limpio)
    
    if patrones:
        # Mostrar resultados
        mostrar_resultados(patrones)
        
        # Guardar resultados si se solicita
        if GUARDAR_RESULTADOS:
            guardar_resultados(patrones)
    else:
        print("❌ No se pudieron generar patrones")
    
    # Limpiar archivo temporal
    os.unlink(archivo_limpio)
    print(f"\n🧹 Archivo temporal eliminado")

# Versión simplificada que solo muestra los arrays
def main_simple():
    """
    Versión minimalista que solo muestra los arrays resultantes
    """
    ARCHIVO = "asdas"
    
    # Limpiar y leer
    archivo_limpio = limpiar_archivo(ARCHIVO)
    with open(archivo_limpio, 'r') as f:
        numeros = [linea.strip() for linea in f if linea.strip()]
    
    # Generar arrays para cada uno de los primeros 7 números
    for i in range(min(7, len(numeros))):
        grupo = []
        idx = i
        while idx < len(numeros):
            grupo.append(numeros[idx])
            idx += 7
        print(f"grupo_{i+1} = {grupo}")
    
    os.unlink(archivo_limpio)

if __name__ == "__main__":
    # Elige qué versión usar:
    
    # Versión completa con detalles
    main()
    
    # Versión simple (solo arrays) - descomenta para usar
    # main_simple()