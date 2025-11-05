"""
Modulo centralizado para los mensajes de error del sistema (Dominio CloudInfra).
"""

# --- Mensajes de Excepciones de Dominio ---

# PotenciaInsuficienteException (US-008)
TEC_POTENCIA_INSUFICIENTE = "Potencia disponible ({:.2f} MW) es menor que la requerida ({} MW)"
USR_POTENCIA_INSUFICIENTE = "No hay suficiente potencia (MW) en el rack para esta operacion."

# EspacioInsuficienteException (US-004)
TEC_ESPACIO_INSUFICIENTE = "Espacio disponible ({} U) es menor que el requerido ({} U)"
USR_ESPACIO_INSUFICIENTE = "No hay suficiente espacio (U) en el server rack."

# --- Mensajes de Excepciones de Persistencia ---

# Leer (US-022)
TEC_LEER_NO_EXISTE = "IOError: Archivo no encontrado en {}"
USR_LEER_NO_EXISTE = "Error de lectura: El archivo de registro no existe."
TEC_LEER_CORRUPTO = "PickleError / EOFError: El archivo {} esta corrupto o vacio."
USR_LEER_CORRUPTO = "Error de lectura: El archivo de registro parece estar corrupto."
TEC_LEER_OTRO = "Exception: Error desconocido al leer el archivo {}."
USR_LEER_OTRO = "Error de lectura: Ocurrio un problema desconocido."

# Escribir (US-021)
TEC_ESCRIBIR_IO = "IOError: No se pudo escribir en el directorio {}"
USR_ESCRIBIR_IO = "Error de escritura: No se tienen permisos o el directorio no existe."
TEC_ESCRIBIR_PICKLE = "PickleError: Error al serializar el objeto {}."
USR_ESCRIBIR_PICKLE = "Error de escritura: No se pudo guardar el registro del DataCenter."
TEC_ESCRIBIR_OTRO = "Exception: Error desconocido al escribir el archivo {}."
USR_ESCRIBIR_OTRO = "Error de escritura: Ocurrio un problema desconocido."