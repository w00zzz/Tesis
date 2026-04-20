import pandas as pd
import json
import os
import operator


def cargar_reglas(ruta_json):
    """Carga las reglas desde el archivo JSON."""
    if not os.path.exists(ruta_json):
        return {"reglas_validez": [], "reglas_consistencia": []}
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)


OPERADORES = {
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}


def _parsear_condicion(condicion_str):
    """Parsea una condicion tipo '>= 0' en (operador, valor)."""
    condicion_str = condicion_str.strip()
    for op_str, op_func in OPERADORES.items():
        if condicion_str.startswith(op_str):
            try:
                valor = float(condicion_str[len(op_str):].strip())
                return op_func, valor
            except ValueError:
                raise ValueError(f"Valor no numerico en condicion: '{condicion_str}'")
    raise ValueError(f"Operador no reconocido en condicion: '{condicion_str}'")


def _verificar_condicion(valor, condicion_str):
    """Verifica si un valor cumple una condicion usando operadores seguros."""
    op_func, umbral = _parsear_condicion(condicion_str)
    return op_func(valor, umbral)


def validar_reglas_dinamicas(df_datos, ruta_reglas):
    """Aplica reglas de validez y consistencia sobre un DataFrame."""
    reglas = cargar_reglas(ruta_reglas)
    resultados = []

    for regla in reglas.get("reglas_validez", []):
        nombre_regla = regla.get("nombre", "Sin nombre")
        condicion = regla.get("condicion", "")
        mensaje = regla.get("mensaje", "")
        columnas_afectadas = regla.get("columnas", [])

        for col in columnas_afectadas:
            if col not in df_datos['ID_Tecnico'].values:
                resultados.append({
                    "Regla": nombre_regla,
                    "Variable": col,
                    "Estado": "Variable no encontrada",
                    "Detalle": f"La variable '{col}' no esta en los datos"
                })
                continue

            stats = df_datos[df_datos['ID_Tecnico'] == col].iloc[0]
            min_muestra = stats['Min_Muestra']
            max_muestra = stats['Max_Muestra']

            try:
                valido_min = _verificar_condicion(min_muestra, condicion)
                valido_max = _verificar_condicion(max_muestra, condicion)
            except ValueError as e:
                resultados.append({
                    "Regla": nombre_regla,
                    "Variable": col,
                    "Estado": "Error de configuracion",
                    "Detalle": str(e)
                })
                continue

            if not valido_min or not valido_max:
                detalles = []
                if not valido_min:
                    detalles.append(f"Minimo ({min_muestra}) viola {condicion}")
                if not valido_max:
                    detalles.append(f"Maximo ({max_muestra}) viola {condicion}")
                resultados.append({
                    "Regla": nombre_regla,
                    "Variable": col,
                    "Estado": "Error de Validez",
                    "Detalle": f"{mensaje} - {'; '.join(detalles)}"
                })
            else:
                resultados.append({
                    "Regla": nombre_regla,
                    "Variable": col,
                    "Estado": "Valido",
                    "Detalle": f"Cumple condicion {condicion}"
                })

    for regla in reglas.get("reglas_consistencia", []):
        nombre_regla = regla.get("nombre", "Sin nombre")
        descripcion = regla.get("descripcion", "")
        mensaje = regla.get("mensaje", "")
        logica = regla.get("logica", "")

        try:
            cumple = _evaluar_regla_consistencia(df_datos, logica)
            if cumple:
                resultados.append({
                    "Regla": nombre_regla,
                    "Variable": "Multiples",
                    "Estado": "Consistente",
                    "Detalle": descripcion
                })
            else:
                resultados.append({
                    "Regla": nombre_regla,
                    "Variable": "Multiples",
                    "Estado": "Inconsistencia",
                    "Detalle": f"{mensaje} - {descripcion}"
                })
        except Exception as e:
            resultados.append({
                "Regla": nombre_regla,
                "Variable": "Multiples",
                "Estado": "Error de evaluacion",
                "Detalle": str(e)
            })

    return pd.DataFrame(resultados)


def _evaluar_regla_consistencia(df_datos, logica_str):
    """Evalua una regla de consistencia tipo 'var1 < val => var2 < val'."""
    if "=>" not in logica_str:
        raise ValueError(f"Formato invalido, debe contener '=>': '{logica_str}'")

    condicion_str, consecuencia_str = logica_str.split("=>", 1)
    condicion_str = condicion_str.strip()
    consecuencia_str = consecuencia_str.strip()

    cond_var, cond_op_str, cond_val = _parsear_expresion(condicion_str)
    if cond_var not in df_datos['ID_Tecnico'].values:
        raise ValueError(f"Variable '{cond_var}' no encontrada")

    valor_cond = df_datos[df_datos['ID_Tecnico'] == cond_var].iloc[0]['Max_Muestra']
    op_cond = OPERADORES.get(cond_op_str)
    if not op_cond(valor_cond, cond_val):
        return True

    cons_var, cons_op_str, cons_val = _parsear_expresion(consecuencia_str)
    if cons_var not in df_datos['ID_Tecnico'].values:
        raise ValueError(f"Variable '{cons_var}' no encontrada")

    valor_cons = df_datos[df_datos['ID_Tecnico'] == cons_var].iloc[0]['Max_Muestra']
    op_cons = OPERADORES.get(cons_op_str)
    return op_cons(valor_cons, cons_val)


def _parsear_expresion(expresion):
    """Parsea 'variable < 10' en (variable, operador, valor)."""
    for op_str in OPERADORES.keys():
        if op_str in expresion:
            partes = expresion.split(op_str, 1)
            variable = partes[0].strip()
            try:
                valor = float(partes[1].strip())
                return variable, op_str, valor
            except ValueError:
                raise ValueError(f"Valor no numerico en: '{expresion}'")
    raise ValueError(f"No se encontro operador en: '{expresion}'")
