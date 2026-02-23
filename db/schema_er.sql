CREATE TABLE simulacion (
    id_simulacion SERIAL PRIMARY KEY,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT
);

CREATE TABLE RegistroSimulado (
    id_registro SERIAL PRIMARY KEY,
    id_simulacion INTEGER NOT NULL,
    timestamp_simulado TIMESTAMP NOT NULL,
    
    potencia_activa DOUBLE PRECISION,
    flujo_vapor_sobrecalentado_cuerpo_ap_turbina DOUBLE PRECISION,
    temp_vapor_sobrecalentado_despues_atemperador_izq DOUBLE PRECISION,
    temp_vapor_recalentado_salida_caldera DOUBLE PRECISION,
    pres_domo DOUBLE PRECISION,
    pres_vap_sobrecal_a_turbina DOUBLE PRECISION,
    pres_vapor_entrada_recalentador DOUBLE PRECISION,
    
    CONSTRAINT fk_simulacion 
        FOREIGN KEY (id_simulacion) 
        REFERENCES simulacion (id_simulacion) 
        ON DELETE CASCADE
);
