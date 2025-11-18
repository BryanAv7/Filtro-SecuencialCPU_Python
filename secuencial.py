# ============================================================
# Practica 2: Procesamiento de convolución de imágenes con
# diferentes filtros utilizando Python.
# Autor: Bryan Avila
# Carrera: Ingeniería en Ciencias de la Computación
# ============================================================


# ============================================================
# Librerias por utilizar
# ============================================================

from PIL import Image
import numpy as np
import math
import time

# ============================================================
# Rutas de entrada y salida
# ============================================================
ruta_entrada = r"C:\Users\USUARIO\Desktop\UPS\computacionParalela\tarea_clases\imagenesPython\imagenprueba3.jpg"
ruta_salida_emboss = r"C:\Users\USUARIO\Desktop\UPS\computacionParalela\tarea_clases\imagenesPython\py_emboss_k49.jpg"
ruta_salida_sobel = r"C:\Users\USUARIO\Desktop\UPS\computacionParalela\tarea_clases\imagenesPython\py_sobel_k49.jpg"
ruta_salida_gauss = r"C:\Users\USUARIO\Desktop\UPS\computacionParalela\tarea_clases\imagenesPython\py_gauss_k49.jpg"
ruta_salida_sharp = r"C:\Users\USUARIO\Desktop\UPS\computacionParalela\tarea_clases\imagenesPython\py_sharp_k49.jpg"


# ============================================================
# Generadores de kernel
# ============================================================
def generar_kernel_emboss(size):
    mitad = size // 2
    k = np.zeros((size, size), dtype=np.float64)
    for y in range(size):
        for x in range(size):
            k[y, x] = (x - mitad) + (y - mitad)
    return k / (size * size)


def generar_kernel_sobel(size):
    mitad = size // 2
    kx = np.zeros((size, size), dtype=np.float64)
    ky = np.zeros((size, size), dtype=np.float64)
    for y in range(-mitad, mitad + 1):
        for x in range(-mitad, mitad + 1):
            kx[y + mitad, x + mitad] = x
            ky[y + mitad, x + mitad] = y
    kx /= np.sum(np.abs(kx)) if np.sum(np.abs(kx)) != 0 else 1
    ky /= np.sum(np.abs(ky)) if np.sum(np.abs(ky)) != 0 else 1
    return kx, ky


def generar_kernel_gaussiano(size, sigma):
    mitad = size // 2
    k = np.zeros((size, size), dtype=np.float64)
    suma = 0.0
    for y in range(-mitad, mitad + 1):
        for x in range(-mitad, mitad + 1):
            v = math.exp(-(x*x + y*y) / (2 * sigma * sigma))
            k[y + mitad, x + mitad] = v
            suma += v
    return k / suma if suma != 0 else k


def generar_kernel_sharpen(size):
    mitad = size // 2
    k = np.zeros((size, size), dtype=np.float64)
    for y in range(-mitad, mitad + 1):
        for x in range(-mitad, mitad + 1):
            if x == 0 and y == 0:
                k[y + mitad, x + mitad] = 5
            elif abs(x) + abs(y) == 1:
                k[y + mitad, x + mitad] = -1
    s = np.sum(np.abs(k))
    return k / s if s != 0 else k

# ============================================================
# Convolución secuencial
# ============================================================
def convolucion_general(img_arr, kernel, factor=1.0, offset_v=0.0):
    H, W, _ = img_arr.shape
    size = kernel.shape[0]
    mitad = size // 2

    salida = np.zeros((H, W, 3), dtype=np.uint8)

    padded = np.pad(img_arr, ((mitad, mitad), (mitad, mitad), (0, 0)), mode="edge")

    offsets = [(dy, dx) for dy in range(-mitad, mitad + 1) for dx in range(-mitad, mitad + 1)]
    kernel_flat = kernel.flatten()

    for y in range(H):
        for x in range(W):
            r = g = b = 0.0
            yp = y + mitad
            xp = x + mitad

            for (dy, dx), k in zip(offsets, kernel_flat):
                px = padded[yp + dy, xp + dx]
                r += px[0] * k
                g += px[1] * k
                b += px[2] * k

            salida[y, x] = (
                int(max(0, min(255, r * factor + offset_v))),
                int(max(0, min(255, g * factor + offset_v))),
                int(max(0, min(255, b * factor + offset_v)))
            )

    return salida


# ============================================================
# Convolución Sobel secuencial
# ============================================================
def sobel_convolucion(img_arr, kx, ky):
    H, W, _ = img_arr.shape
    size = kx.shape[0]
    mitad = size // 2

    salida = np.zeros((H, W, 3), dtype=np.uint8)

    padded = np.pad(img_arr, ((mitad, mitad), (mitad, mitad), (0, 0)), mode="edge")

    offsets = [(dy, dx) for dy in range(-mitad, mitad + 1) for dx in range(-mitad, mitad + 1)]
    kxf = kx.flatten()
    kyf = ky.flatten()

    for y in range(H):
        for x in range(W):
            gx = [0.0, 0.0, 0.0]
            gy = [0.0, 0.0, 0.0]
            yp = y + mitad
            xp = x + mitad

            for (dy, dx), kxv, kyv in zip(offsets, kxf, kyf):
                px = padded[yp + dy, xp + dx]
                for c in range(3):
                    gx[c] += px[c] * kxv
                    gy[c] += px[c] * kyv

            salida[y, x] = (
                int(min(255, math.sqrt(gx[0]**2 + gy[0]**2) * 2)),
                int(min(255, math.sqrt(gx[1]**2 + gy[1]**2) * 2)),
                int(min(255, math.sqrt(gx[2]**2 + gy[2]**2) * 2)),
            )

    return salida


# ============================================================
# Main
# ============================================================
def main():
    img = Image.open(ruta_entrada).convert("RGB")
    img_arr = np.array(img, dtype=np.uint8)

    print("\nImagen cargada:", img_arr.shape)

    print("\nSeleccione filtro:")
    print("1. Emboss")
    print("2. Sobel")
    print("3. Gaussiano")
    print("4. Sharpen")
    print("0. Salir")
    opcion = int(input("> "))

    if opcion == 0:
        return

    print("\nSeleccione tamaño de kernel (9, 21, 49):")
    tam = int(input("> "))
    if tam not in (9, 21, 49):
        tam = 9

    inicio = time.time()

    if opcion == 1:
        kernel = generar_kernel_emboss(tam)
        salida = convolucion_general(img_arr, kernel, factor=2.0, offset_v=128.0)
        Image.fromarray(salida).save(ruta_salida_emboss)
        print("Guardado en:", ruta_salida_emboss)

    elif opcion == 2:
        kx, ky = generar_kernel_sobel(tam)
        salida = sobel_convolucion(img_arr, kx, ky)
        Image.fromarray(salida).save(ruta_salida_sobel)
        print("Guardado en:", ruta_salida_sobel)

    elif opcion == 3:
        sigma = float(input("Sigma: "))
        kernel = generar_kernel_gaussiano(tam, sigma)
        salida = convolucion_general(img_arr, kernel)
        Image.fromarray(salida).save(ruta_salida_gauss)
        print("Guardado en:", ruta_salida_gauss)

    elif opcion == 4:
        intensidad = float(input("Intensidad: "))
        kernel = generar_kernel_sharpen(tam)
        salida = convolucion_general(img_arr, kernel, factor=intensidad)
        Image.fromarray(salida).save(ruta_salida_sharp)
        print("Guardado en:", ruta_salida_sharp)

    tiempo = time.time() - inicio
    
    # Medir y mostrar tiempo de ejecución(convolución)
    print("\nTiempo de ejecución:")
    print(f"{tiempo*1000:.3f} ms")
    print(f"{tiempo:.3f} s")
    print(f"{tiempo/60:.3f} min")


if __name__ == "__main__":
    main()
