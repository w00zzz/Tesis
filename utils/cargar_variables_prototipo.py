import pandas as pd

def cargar_variables_prototipo():
    datos = [
        {
            "ID_Tecnico": "1GEV007CE",
            "Nombre_amigable": "potencia_activa",
            "Descripcion_funcional": "Nivel de exigencia operativa del sistema, influyendo directamente en los esfuerzos aplicados y en la probabilidad de fallo",
            "Unidad": "MW",
            "Tipo_dato": "float",
            "Rango_min": 263.56,
            "Rango_max": 272.11,
            "Distribucion_observada": "Distribución multimodal, aproximadamente simétrica, colas cortas (platicúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        },
        {
            "ID_Tecnico": "1FSRFTB504",
            "Nombre_amigable": "flujo_vapor_sobrecalentado_cuerpo_ap_turbina",
            "Descripcion_funcional": "Caudal de vapor que incide en la turbina, determinando los esfuerzos térmicos y mecánicos sobre sus componentes",
            "Unidad": "t/h",
            "Tipo_dato": "float",
            "Rango_min": 774.38,
            "Rango_max": 788.41,
            "Distribucion_observada": "Distribución multimodal, asimétrica negativa (cola izquierda), colas largas (leptocúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        },
        {
            "ID_Tecnico": "1FSRTE502C",
            "Nombre_amigable": "temp_vapor_sobrecalentado_despues_atemperador_izq",
            "Descripcion_funcional": "Nivel térmico del vapor, determinando los esfuerzos térmicos y el riesgo de degradación de los componentes",
            "Unidad": "°C",
            "Tipo_dato": "float",
            "Rango_min": 401.19,
            "Rango_max": 403.35,
            "Distribucion_observada": "Distribución multimodal, aproximadamente simétrica, colas cortas (platicúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        },
        {
            "ID_Tecnico": "1FRSTE503A",
            "Nombre_amigable": "temp_vapor_recalentado_salida_caldera",
            "Descripcion_funcional": "Nivel térmico del vapor recalentado, influyendo en los esfuerzos térmicos y en la probabilidad de fallo de los componentes",
            "Unidad": "°C",
            "Tipo_dato": "float",
            "Rango_min": 535.14,
            "Rango_max": 538.88,
            "Distribucion_observada": "Distribución multimodal, aproximadamente simétrica, colas cortas (platicúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        },
        {
            "ID_Tecnico": "1FSRPT501",
            "Nombre_amigable": "pres_domo",
            "Descripcion_funcional": "Nivel de presión del sistema, influyendo en los esfuerzos mecánicos y en la probabilidad de fallo de los componentes",
            "Unidad": "bar",
            "Tipo_dato": "float",
            "Rango_min": 171.45,
            "Rango_max": 174.16,
            "Distribucion_observada": "Distribución multimodal, asimétrica negativa (cola izquierda), colas largas (leptocúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        },
        {
            "ID_Tecnico": "1FSRPT504",
            "Nombre_amigable": "pres_vap_sobrecal_a_turbina",
            "Descripcion_funcional": "Presión del vapor de entrada, determinando los esfuerzos mecánicos y el riesgo de fallo en los componentes",
            "Unidad": "bar",
            "Tipo_dato": "float",
            "Rango_min": 164.26,
            "Rango_max": 166.80,
            "Distribucion_observada": "Distribución multimodal, asimétrica negativa (cola izquierda), colas largas (leptocúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        },
        {
            "ID_Tecnico": "1FRSPT526",
            "Nombre_amigable": "pres_vapor_entrada_recalentador",
            "Descripcion_funcional": "Presión del vapor antes del recalentamiento, influyendo en los esfuerzos mecánicos y en la probabilidad de fallo de los componentes",
            "Unidad": "bar",
            "Tipo_dato": "float",
            "Rango_min": 29.51,
            "Rango_max": 30.38,
            "Distribucion_observada": "Distribución multimodal, aproximadamente simétrica, colas cortas (platicúrtica), baja dispersión",
            "Pregunta_planta": "Frecuencia de muestreo?, Descripcion?"
        }
    ]

    return pd.DataFrame(datos)