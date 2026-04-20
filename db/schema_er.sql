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
('1GEV007CE', 'potencia_activa', 'MW', 'float', 'Carga', 'Potencia', 'Vibraciones_mecanicas,HCF (High Cycle Fatigue)', 'G(X) = C - D (estado limite, Nachlas 1995)', 'Potencia de salida que induce esfuerzos mecanicos sobre el rotor. Participa en funcion de estado limite G(X) = Capacidad - Demanda. Referencia: Perez (2024), Nachlas (1995)', 263.56, 272.11, 'Multimodal, simetrica, colas cortas', '¿Ubicacion del sensor? ¿Medicion directa o calculada? ¿Frecuencia de muestreo? ¿Precision? ¿Ultima calibracion? ¿Retrasos?'),
('1FSRFTB504', 'flujo_vapor_sobrecalentado', 't/h', 'float', 'Carga', 'Flujo', 'SPE (Solid Particle Erosion)', 'sigma_y = 1.14e-7 * rho_ox * d_ox^3 * (F_v/S)^2 - Ecs (2.1),(2.11),(2.15),(2.16),(2.17)', 'F_v en energia cinetica para erosion SPE. rho_ox=5.08 g/cm³, d_ox via oxidacion parabolica. Constantes: A=6.22e20 µm²/h, Eox=-326kJ/mol. Referencia: Perez (2024), Reshetnyak (1995)', 774.38, 788.41, 'Multimodal, asimetrica negativa, colas largas', '¿Ubicacion? ¿Directa o calculada? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Retrasos de transporte?'),
('1FSRTE502C', 'temp_vapor_sobrecalentado_atemperador', '°C', 'float', 'Carga', 'Temperatura', 'Choque_termico,Fatiga_termica', 'Nu = 0.023 * Re^0.8 * Pr^n (Dittus-Boelter) - Ecs (2.25),(2.27),(2.28)', 'T entrada para coeficiente de pelicula y numero de Nusselt. n=0.4 calentamiento, n=0.02 real. Referencia: Perez (2024), Leyzerovich (2008)', 401.19, 403.35, 'Multimodal, simetrica, colas cortas', '¿Ubicacion? ¿Contacto directo? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Retraso termico?'),
('1FRSTE503A', 'temp_vapor_recalentado_salida', '°C', 'float', 'Carga', 'Temperatura', 'Creep (Fluencia lenta),Fatiga_termica', 'LMP = T*(C + log10(t_r)) - Ecs (2.8),(2.9),(2.12),(2.32)', 'T absoluta para parametro Larson-Miller, C=20, en vida remanente por creep. Influye en oxidacion parabolica. Referencia: Perez (2024), Mendelson (1965)', 535.14, 538.88, 'Multimodal, simetrica, colas cortas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Influencia de radiacion?'),
('1FSRPT501', 'presion_domo', 'bar', 'float', 'Carga', 'Presion', 'Creep,SCC (Stress Corrosion Cracking)', 'sigma_theta = P*r/t (esfuerzo circunferencial)', 'P genera esfuerzos de membrana en paredes del domo para analisis de creep y SCC. sigma_theta = P*r/t. Referencia: Perez (2024)', 171.45, 174.16, 'Multimodal, asimetrica negativa, colas largas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Pulsaciones?'),
('1FSRPT504', 'presion_vapor_sobrecalentado_turbina', 'bar', 'float', 'Carga', 'Presion', 'SPE,Creep', 'V = F_v/S, rho_corregida = f(P,T) - Ecs (2.14),(2.19)', 'P_tr entrada para correccion de densidad del vapor y calculo de velocidad V = F_v/S. Influye en energia cinetica de SPE. Referencia: Perez (2024)', 164.26, 166.80, 'Multimodal, asimetrica negativa, colas largas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Vibraciones?'),
('1FRSPT526', 'presion_vapor_entrada_recalentador', 'bar', 'float', 'Carga', 'Presion', 'Creep,Oxidacion', 'd_ox^2 = 2*A*exp(-Eox/(R*T))*dt - Ecs (2.10),(2.36),(2.37),(2.38)', 'P_T entrada para calculo de oxido d_ox via oxidacion parabolica. Constantes: A=6.22e20 µm²/h, Eox=-326kJ/mol. Influye en sigma_y para SPE. Referencia: Sabau (2014), Perez (2024)', 29.51, 30.38, 'Multimodal, simetrica, colas cortas', '¿Ubicacion? ¿Directa? ¿Frecuencia? ¿Precision? ¿Calibracion? ¿Humedad?');

-- Propiedades de materiales (Resistencia) - Pagina 103 tesis
INSERT INTO Variable (id_tecnico, nombre_amigable, unidad, tipo_dato, tipo_en_modelo, tipo_variable, mecanismos_asociados, ecuacion, rol_en_ecuacion, rango_min, rango_max, distribucion_observada, pregunta_planta) VALUES
('Acero_1CrMoV_LimFluencia', 'limite_fluencia_acero_rotor', 'MPa', 'float', 'Resistencia', 'Propiedad_mecanica', 'SPE,Creep,Fatiga_termica,SCC', 'sigma_y_resistencia = sigma_y (Perez 2024)', 'sigma_y=240 MPa resistencia superficial SPE. Composicion: C=0.28-0.35%, Cr=0.90-1.20%, Mo=0.20-0.35%, V=0.05-0.15%. Trat: Austeniz 850-900C + Revenido 540-680C. Referencia: Perez (2024), ASM Handbook', 240.0, 240.0, 'Normal', 'Composicion: C=0.28-0.35%, Cr=0.90-1.20%, Mo=0.20-0.35%, V=0.05-0.15%. Trat: Austeniz 850-900C + Revenido 540-680C. Certificados: ASTM A470, ASME Section II. Ubicacion probetas: zona rotor, eje'),
('Acero_1CrMoV_ResFatiga', 'resistencia_fatiga_acero', 'MPa', 'float', 'Resistencia', 'Propiedad_mecanica', 'Fatiga_termica,Vibraciones_mecanicas', 'sigma_n = Ca*Cb*Cc*Cd*Ce*sigma_n_prim - Anexo 6', 'Fatiga corregida: Ca=0.75, Cb=0.85, Cc=0.82, Cd=0.42, Ce=0.99. sigma_n_prim=835 MPa. Resultado: 190 MPa. Curva S-N: sigma = 1315 - 0.563*N. Referencia: Anexo 6 tesis', 190.0, 190.0, 'Normal', 'Coeficientes: Ca=0.75, Cb=0.85, Cc=0.82, Cd=0.42, Ce=0.99. Curva S-N: sigma=1315-0.563N. Temp. operacion: 530C (800K). Zona probetas: rotor, eje. Norma: ASTM E466'),
('Acero_1CrMoV_ModElasticidad', 'modulo_elasticidad_acero', 'GPa', 'float', 'Resistencia', 'Propiedad_mecanica', 'Vibraciones_mecanicas,Fatiga_termica', 'sigma = E*epsilon (Ley elastica de Hooke)', 'Modulo de Young E=160 GPa. Degrada >450C. Referencia: Perez (2024), Pagina 103 tesis, ASM Handbook', 160.0, 160.0, 'Normal', 'E=160 GPa a temp. ambiente. Curva E vs T: degradacion >450C. Ensayo a temp. elevada necesario. Tipo: 1CrMoV. Precision: segun ASTM A470'),
('Acero_1CrMoV_DilTermica', 'coef_dilatacion_termica', '1/°C', 'float', 'Resistencia', 'Propiedad_termica', 'Choque_termico,Fatiga_termica', 'delta_L = alpha * L0 * delta_T', 'Coeficiente alpha=1.2e-5 1/°C para deformaciones termicas. Referencia: Pagina 103 tesis', 1.2e-5, 1.2e-5, 'Normal', 'Alpha=1.2e-5 1/°C. Ensayo a temp. elevada requerido (>450C). Tipo: 1CrMoV. Precision: segun ASTM A470'),
('Acero_1CrMoV_Densidad', 'densidad_acero', 'g/cm³', 'float', 'Resistencia', 'Propiedad_masica', 'SPE,Vibraciones_mecanicas', 'masa = densidad * volumen', 'Densidad=7.8 g/cm³ para calculo de masa y esfuerzos inerciales. Referencia: Pagina 103 tesis, ASM Handbook', 7.8, 7.8, 'Normal', 'Densidad=7.8 g/cm³ segun ASM Handbook. Ensayo: metodo hidrostatico. Muestra: representativa del rotor. Homogeneidad verificada por certificados ASTM A470'),
('Acero_1CrMoV_Cp', 'capacidad_calorifica', 'J/kg°C', 'float', 'Resistencia', 'Propiedad_termica', 'Choque_termico,Fatiga_termica,Creep', 'Q = Cp * masa * delta_T', 'Capacidad calorifica Cp=680 J/kg°C. Degrada >500C. Referencia: Pagina 103 tesis', 680.0, 680.0, 'Normal', 'Cp=680 J/kg°C a temp. ambiente. Curva Cp vs T: degradacion >500C. Ensayo: calorimeria diferencial. Norma: ASTM E1269'),
('Oxido_Fe3O4_Densidad', 'densidad_oxido_magnetita', 'g/cm³', 'float', 'Resistencia', 'Propiedad_oxido', 'SPE', 'sigma_y = 1.14e-7 * rho_ox * d_ox^3 * (F_v/S)^2', 'Densidad oxidos rho_ox=5.08 g/cm³ para erosion SPE. Transforma a hematites >600C. Constantes: A=6.22e20 µm²/h, Eox=-326kJ/mol. Referencia: Sabau (2014), Dooley (2019)', 5.08, 5.08, 'Normal', 'Densidad=5.08 g/cm³ (magnetita). Transicion a hematites >600C. Espesor escama medido por UT. Composicion: Fe3O4. Norma: ASTM E570');
