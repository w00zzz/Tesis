-- Schema: Simulador de Turbina de Vapor
-- Modelo Entidad-Relacion normalizado

CREATE TABLE Variable (
    id_variable         SERIAL PRIMARY KEY,
    id_tecnico          VARCHAR(50)     NOT NULL UNIQUE,
    nombre_amigable     VARCHAR(100)    NOT NULL,
    unidad              VARCHAR(20)     NOT NULL,
    tipo_dato           VARCHAR(20)     NOT NULL CHECK (tipo_dato IN ('float', 'int')),
    tipo_en_modelo      VARCHAR(20)     NOT NULL CHECK (tipo_en_modelo IN ('Carga', 'Resistencia', 'Auxiliar')),
    tipo_variable       VARCHAR(50),
    mecanismos_asociados VARCHAR(200),
    ecuacion            VARCHAR(100),
    rol_en_ecuacion     TEXT,
    rango_min           FLOAT,
    rango_max           FLOAT,
    distribucion_observada VARCHAR(200),
    pregunta_planta     TEXT,
    fecha_creacion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_variable_id_tecnico ON Variable(id_tecnico);
CREATE INDEX idx_variable_tipo_modelo ON Variable(tipo_en_modelo);
CREATE INDEX idx_variable_mecanismos ON Variable(mecanismos_asociados);

CREATE TABLE ParametroEstadistico (
    id_parametro        SERIAL PRIMARY KEY,
    id_variable         INTEGER         NOT NULL,
    distribucion        VARCHAR(50)     NOT NULL CHECK (distribucion IN ('Normal', 'LogNormal', 'Weibull', 'Gamma', 'Exponencial')),
    param1              FLOAT           NOT NULL,
    param2              FLOAT           NOT NULL,
    param3              FLOAT,
    gof_metric          VARCHAR(50),
    gof_value           FLOAT,
    fecha_actualizacion DATE            NOT NULL DEFAULT CURRENT_DATE,
    notas               TEXT,

    CONSTRAINT fk_parametro_variable
        FOREIGN KEY (id_variable)
        REFERENCES Variable(id_variable)
        ON DELETE CASCADE
);

CREATE INDEX idx_parametro_id_variable ON ParametroEstadistico(id_variable);

CREATE TABLE Simulacion (
    id_simulacion       SERIAL PRIMARY KEY,
    fecha_generacion    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion         VARCHAR(200),
    n_dias              INTEGER,
    freq_minutos        INTEGER         DEFAULT 60,
    modelo_temporal     VARCHAR(20)     DEFAULT 'AR(1)',
    phi                 FLOAT           DEFAULT 0.7,
    usuario             VARCHAR(100),
    estado              VARCHAR(20)     DEFAULT 'completada' CHECK (estado IN ('en_progreso', 'completada', 'fallida'))
);

CREATE TABLE RegistroSimulado (
    id_registro         SERIAL PRIMARY KEY,
    id_simulacion       INTEGER         NOT NULL,
    timestamp_simulado  TIMESTAMP       NOT NULL,
    id_variable         INTEGER         NOT NULL,
    valor               FLOAT           NOT NULL,

    CONSTRAINT fk_registro_simulacion
        FOREIGN KEY (id_simulacion)
        REFERENCES Simulacion(id_simulacion)
        ON DELETE CASCADE,

    CONSTRAINT fk_registro_variable
        FOREIGN KEY (id_variable)
        REFERENCES Variable(id_variable)
        ON DELETE CASCADE
);

CREATE INDEX idx_registro_id_simulacion ON RegistroSimulado(id_simulacion);
CREATE INDEX idx_registro_id_variable ON RegistroSimulado(id_variable);
CREATE INDEX idx_registro_timestamp ON RegistroSimulado(timestamp_simulado);

CREATE VIEW VW_VariableConParametros AS
SELECT
    v.id_variable,
    v.id_tecnico,
    v.nombre_amigable,
    v.unidad,
    v.tipo_en_modelo,
    v.tipo_variable,
    v.mecanismos_asociados,
    v.ecuacion,
    v.rango_min,
    v.rango_max,
    p.distribucion,
    p.param1,
    p.param2,
    p.param3,
    p.gof_value
FROM Variable v
LEFT JOIN ParametroEstadistico p ON v.id_variable = p.id_variable
WHERE p.fecha_actualizacion = (
    SELECT MAX(fecha_actualizacion)
    FROM ParametroEstadistico
    WHERE id_variable = v.id_variable
);

-- Datos iniciales: variables SCADA del Anexo 1
INSERT INTO Variable (id_tecnico, nombre_amigable, unidad, tipo_dato, tipo_en_modelo, tipo_variable, mecanismos_asociados, ecuacion, rol_en_ecuacion, rango_min, rango_max, distribucion_observada, pregunta_planta) VALUES
('1GEV007CE', 'potencia_activa', 'MW', 'float', 'Carga', 'Potencia', 'Vibraciones_mecanicas', 'Cap.2', 'Potencia de salida que induce esfuerzos mecanicos y vibraciones en el rotor', 263.56, 272.11, 'Multimodal, simetrica, colas cortas', '¿Ubicacion del sensor? ¿Medicion directa o calculada? ¿Frecuencia de muestreo? ¿Precision? ¿Ultima calibracion? ¿Retrasos?'),
('1FSRFTB504', 'flujo_vapor_sobrecalentado', 't/h', 'float', 'Carga', 'Flujo', 'SPE,Choque_termico,Fatiga_termica', '(2.1),(2.11),(2.16),(2.17)', 'F_v en energia cinetica y velocidad del vapor', 774.38, 788.41, 'Multimodal, asimetrica negativa, colas largas', '¿Ubicacion? ¿Directa o calculada? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Retrasos de transporte?'),
('1FSRTE502C', 'temp_vapor_sobrecalentado_atemperador', '°C', 'float', 'Carga', 'Temperatura', 'Choque_termico,Fatiga_termica', 'Cap.2 - Transferencia de calor', 'T determina esfuerzos termicos y numero de Nusselt', 401.19, 403.35, 'Multimodal, simetrica, colas cortas', '¿Ubicacion? ¿Contacto directo? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Retraso termico?'),
('1FRSTE503A', 'temp_vapor_recalentado_salida', '°C', 'float', 'Carga', 'Temperatura', 'Creep,Fatiga_termica,SPE', '(2.8),(2.9),(2.12)', 'T afecta espesor de oxido y parametro de Larson-Miller', 535.14, 538.88, 'Multimodal, simetrica, colas cortas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Influencia de radiacion?'),
('1FSRPT501', 'presion_domo', 'bar', 'float', 'Carga', 'Presion', 'Creep,SCC', 'Cap.2 - Esfuerzo circunferencial', 'P genera esfuerzos de membrana en paredes del domo', 171.45, 174.16, 'Multimodal, asimetrica negativa, colas largas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Pulsaciones?'),
('1FSRPT504', 'presion_vapor_sobrecalentado_turbina', 'bar', 'float', 'Carga', 'Presion', 'SPE,Creep', '(2.14),(2.19)', 'P_tr para correccion de densidad y velocidad', 165.28, 166.80, 'Multimodal, asimetrica negativa, colas largas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Vibraciones?'),
('1FRSPT526', 'presion_vapor_entrada_recalentador', 'bar', 'float', 'Carga', 'Presion', 'Creep,Fatiga', '(2.10)', 'P_T en calculo de espesor de oxido', 29.51, 30.38, 'Multimodal, simetrica, colas cortas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Humedad?');

-- Propiedades de materiales (Resistencia)
INSERT INTO Variable (id_tecnico, nombre_amigable, unidad, tipo_dato, tipo_en_modelo, tipo_variable, mecanismos_asociados, ecuacion, rol_en_ecuacion, rango_min, rango_max, distribucion_observada, pregunta_planta) VALUES
('Acero_CrMoV_LimFluencia', 'limite_fluencia_acero_rotor', 'MPa', 'float', 'Resistencia', 'Propiedad_mecanica', 'SPE,Creep,Fatiga_termica,SCC', '(2.6),(2.11),(2.12)', 'sigma_y resistencia superficial contra erosion', 350.0, 450.0, 'Normal', '¿Composicion exacta? ¿Tratamiento termico? ¿Certificados? ¿Ensayos? ¿Precision de ensayos? ¿Calibracion de equipos? ¿Ubicacion de probetas?'),
('Acero_CrMoV_ResFatiga', 'resistencia_fatiga_acero', 'MPa', 'float', 'Resistencia', 'Propiedad_mecanica', 'Fatiga_termica,Vibraciones_mecanicas', 'sigma_n = Ca·Cb·Cc·Cd·Ce·sigma_n', 'Resistencia a fatiga corregida por coeficientes', 150.0, 230.0, 'Normal', '¿Valores de coeficientes? ¿Curvas S-N? ¿Temp. operacion? ¿Precision de ensayos? ¿Calibracion? ¿Ubicacion de probetas?'),
('Acero_CrMoV_ModElasticidad', 'modulo_elasticidad_acero', 'GPa', 'float', 'Resistencia', 'Propiedad_mecanica', 'Vibraciones_mecanicas,Fatiga_termica', 'sigma = E·epsilon', 'Modulo de Young para deformaciones elasticas', 190.0, 210.0, 'Normal', '¿Valor de E a temp. operacion? ¿Curva E vs T? ¿Ensayo a temp. elevada? ¿Tipo acero? ¿Precision? ¿Calibracion? ¿Ubicacion?');
