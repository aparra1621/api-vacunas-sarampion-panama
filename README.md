# API RESTful de vacunación contra el sarampión en Panamá

## Descripción
Este proyecto implementa una API RESTful de solo lectura para consultar datos históricos sobre la cobertura de vacunación contra el sarampión en niños de 12 a 23 meses en Panamá, utilizando el indicador `SH.IMM.MEAS` del Banco Mundial.

La API expone endpoints GET para consultar todos los registros, un año específico y un endpoint opcional por provincia con datos simulados para fines académicos.

---

## Endpoints

### GET /vacunas
Devuelve todos los registros disponibles.

### GET /vacunas/<anio>
Devuelve el registro correspondiente al año solicitado.
