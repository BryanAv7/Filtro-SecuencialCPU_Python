# 📌 Práctica 2: Procesamiento de Convolución de Imágenes en Python

**Autor:** Bryan Avila\
**Carrera:** Ingeniería en Ciencias de la Computación

Esta práctica implementa diferentes filtros de convolución aplicados a
imágenes utilizando Python. Se desarrollan filtros como **Emboss**,
**Sobel**, **Gaussiano** y **Sharpen**, empleando operaciones de
convolución mediante bucles.

------------------------------------------------------------------------

## 🧩 Características principales

-   Carga una imagen de entrada en formato RGB.\
-   Genera kernels dinámicos según el filtro seleccionado.\
-   Aplica convolución secuencial pixel por pixel.\
-   Permite elegir el tamaño del kernel (9, 21 o 49).\
-   Guarda las imágenes resultantes.\
-   Mide el tiempo de ejecución de la convolución generada.

------------------------------------------------------------------------

## 📚 Librerías utilizadas

-   **PIL (Pillow)** -- manejo de imágenes\
-   **NumPy** -- generación de matrices\
-   **Math** -- funciones matemáticas\
-   **Time** -- medición de tiempos

------------------------------------------------------------------------

## 🛠️ Filtros implementados

### 🔹 Emboss

Resalta bordes generando un efecto de relieve.\
Se utiliza un kernel generado a partir de posiciones relativas dentro de
la matriz.

------------------------------------------------------------------------

### 🔹 Sobel

Detecta bordes en direcciones X e Y.\
Se generan dos kernels: uno para gradiente horizontal (**kx**) y otro
vertical (**ky**).\
Los gradientes se combinan para obtener la magnitud total del borde.

------------------------------------------------------------------------

### 🔹 Gaussiano

Desenfoque suave basado en la función gaussiana.\
El usuario define el parámetro **sigma**, que controla la difusión del
filtro.

------------------------------------------------------------------------

### 🔹 Sharpen

Aumenta nitidez realzando diferencias locales.\
Se utiliza un kernel centrado que resalta el píxel actual y resta
vecinos.

------------------------------------------------------------------------

## ⏱️ Medición de tiempo

Después de aplicar el filtro, se muestra:

-   Tiempo en **milisegundos**
-   Tiempo en **segundos**
-   Tiempo en **minutos**

------------------------------------------------------------------------

## ▶️ Ejecución del programa

Al iniciar, el programa:

1.  Carga la imagen especificada.

2.  Pregunta qué filtro aplicar:

        1. Emboss
        2. Sobel
        3. Gaussiano
        4. Sharpen
        0. Salir

3.  Solicita el tamaño del kernel: **9, 21 o 49**

4.  Dependiendo del filtro:

    -   Para Gauss: solicita **sigma**
    -   Para Sharpen: solicita **intensidad**
    -   Para los demás filtros, ya vienen preconfiguradas.

5.  Genera la imagen procesada y la guarda en la ruta definida.

------------------------------------------------------------------------

## 📂 Estructura del código

El programa se compone de:

-   **Funciones de generación de kernels**
-   **Funciones de convolución general y Sobel**
-   **Main con menú interactivo**
-   **Guardado de resultados**

------------------------------------------------------------------------

## 📸 Entrada y salida

-   **Entrada:** Imagen JPG o PNG\
-   **Salida:** Versiones filtradas guardadas como:
    -   `py_emboss_kXX.jpg`\
    -   `py_sobel_kXX.jpg`\
    -   `py_gauss_kXX.jpg`\
    -   `py_sharp_kXX.jpg`

(XX corresponde al tamaño del kernel)

------------------------------------------------------------------------

## ✔️ Ejemplo de ejecución

    Imagen cargada: (1080, 1920, 3)

    Seleccione filtro:
    1. Emboss
    2. Sobel
    3. Gaussiano
    4. Sharpen
    > 3

    Seleccione tamaño de kernel (9, 21, 49):
    > 21

    Sigma:
    > 2.0

    Guardado en: py_gauss_k21.jpg

    Tiempo de ejecución:
    ------- ms
    ------- s
    ------- m
    0.150 s
    0.002 min
