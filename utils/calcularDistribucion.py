import numpy as np
from scipy.stats import skew, kurtosis

def describir_distribucion(data):
    data = np.array(data)

    media = np.mean(data)
    mediana = np.median(data)
    std = np.std(data)
    skewness = skew(data)
    kurt = kurtosis(data)

    descripcion = []

    if abs(skewness) < 0.5:
        descripcion.append("aproximadamente simétrica")
    elif skewness > 0:
        descripcion.append("asimétrica positiva (cola derecha)")
    else:
        descripcion.append("asimétrica negativa (cola izquierda)")

    if kurt > 0:
        descripcion.append("colas largas (leptocúrtica)")
    elif kurt < 0:
        descripcion.append("colas cortas (platicúrtica)")
    else:
        descripcion.append("colas normales")

    if std < (media * 0.1 if media != 0 else 1):
        descripcion.append("baja dispersión")
    elif std < (media * 0.3 if media != 0 else 3):
        descripcion.append("dispersión moderada")
    else:
        descripcion.append("alta dispersión")

    hist, _ = np.histogram(data, bins=10)
    peaks = np.sum(hist > np.mean(hist))

    if peaks <= 2:
        descripcion.insert(0, "unimodal")
    else:
        descripcion.insert(0, "multimodal")

    return "Distribución " + ", ".join(descripcion)


data1 = [266.02, 266.44, 266.42, 266.04, 267.59, 266.14, 271.79, 268.81, 272.11, 268.80, 270.98, 268.25, 270.00, 269.24, 270.39, 271.01, 269.99, 271.52, 266.42, 266.99, 263.56]
data2 = [783.11, 784.55, 784.00, 784.29, 786.36, 782.07, 788.12, 781.82, 788.41, 780.77, 787.62, 781.80, 785.96, 782.57, 785.07, 784.66, 783.37, 786.09, 781.05, 786.98, 774.38]
data3 = [401.65, 403.35, 401.67, 402.89, 401.83, 402.33, 402.55, 401.99, 402.74, 401.77, 403.05, 401.78, 403.27, 401.77, 403.18, 401.76, 402.77, 401.80, 402.09, 402.76, 401.19]
data4 = [537.97, 535.89, 538.51, 535.36, 538.61, 535.14, 538.88, 535.18, 538.14, 536.11, 537.38, 536.98, 536.49, 538.24, 535.45, 538.12, 535.38, 538.33, 535.77, 538.25, 536.23]
data5 = [173.18, 173.15, 173.42, 173.03, 173.78, 172.60, 174.16, 172.64, 174.10, 172.63, 173.84, 172.91, 173.46, 173.22, 173.22, 173.59, 172.98, 173.81, 172.65, 173.82, 171.45]
data6 = [165.84, 165.81, 166.09, 165.70, 166.48, 165.28, 166.80, 165.34, 166.71, 165.32, 166.52, 165.62, 166.13, 165.96, 165.90, 166.26, 165.63, 166.51, 165.30, 166.44, 164.26]
data7 = [29.59, 29.64, 29.63, 29.63, 29.76, 29.51, 30.32, 30.00, 30.38, 29.99, 30.35, 30.03, 30.27, 30.13, 30.21, 30.25, 30.18, 30.32, 30.06, 30.36, 29.75]
print(f"data1: {describir_distribucion(data1)}")
print(f"data2: {describir_distribucion(data2)}")
print(f"data3: {describir_distribucion(data3)}")
print(f"data4: {describir_distribucion(data4)}")
print(f"data5: {describir_distribucion(data5)}")
print(f"data6: {describir_distribucion(data6)}")
print(f"data7: {describir_distribucion(data7)}")