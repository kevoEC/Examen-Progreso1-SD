-- Crear la base de datos
CREATE DATABASE BioNetDB;
GO

USE BioNetDB;
GO

-- Tabla principal de resultados
CREATE TABLE resultados_examenes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    laboratorio_id INT NOT NULL,
    paciente_id INT NOT NULL,
    tipo_examen NVARCHAR(100) NOT NULL,
    resultado NVARCHAR(100),
    fecha_examen DATE NOT NULL,
    CONSTRAINT UQ_resultado UNIQUE (paciente_id, tipo_examen, fecha_examen) -- Para evitar duplicados
);
GO

-- Tabla de auditoría (trigger)
CREATE TABLE log_cambios_resultados (
    id INT IDENTITY(1,1) PRIMARY KEY,
    operacion NVARCHAR(10), -- 'INSERT' o 'UPDATE'
    paciente_id INT,
    tipo_examen NVARCHAR(100),
    fecha DATETIME DEFAULT GETDATE()
);
GO

-- Trigger para registrar inserciones o actualizaciones
CREATE TRIGGER trg_log_resultados
ON resultados_examenes
AFTER INSERT, UPDATE
AS
BEGIN
    INSERT INTO log_cambios_resultados (operacion, paciente_id, tipo_examen)
    SELECT 
        CASE 
            WHEN EXISTS (SELECT * FROM inserted EXCEPT SELECT * FROM deleted) THEN 'UPDATE'
            ELSE 'INSERT'
        END,
        paciente_id,
        tipo_examen
    FROM inserted;
END;
GO

SELECT * FROM resultados_examenes;
SELECT * FROM log_cambios_resultados;