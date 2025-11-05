"""
Modulo Centralizado de Constantes del Sistema (PythonCloudInfra)

Este archivo contiene todos los valores fijos (constantes o "magic numbers")
del sistema para cumplir con la rubrica de evaluacion (Seccion 3.4).

Mapea 1 a 1 las constantes del proyecto PythonForestal al nuevo
dominio de Data Center.
"""

# ==============================================================================
# --- EPIC 1: GESTION DE INFRAESTRUCTURA (US-002) ---
# ==============================================================================

# --- Constantes de ServerRack (US-002) ---
POTENCIA_INICIAL_RACK: float = 100.0  # MW por defecto


# ==============================================================================
# --- EPIC 2: GESTION DE SERVICIOS (US-004 a US-008) ---
# ==============================================================================

# --- Constantes de ServicioDatabase (US-004) ---
ESPACIO_U_DATABASE: int = 4  # Unidades de Rack
POTENCIA_BASE_DATABASE: float = 2.0  # MW
IOPS_INICIAL_DATABASE: int = 1000

# --- Constantes de ServicioBatch (US-005) ---
ESPACIO_U_BATCH: int = 2  # Unidades de Rack
POTENCIA_BASE_BATCH: float = 3.0  # MW
WORKERS_INICIAL_BATCH: int = 5

# --- Constantes de ServicioWebApp (US-006) ---
ESPACIO_U_WEBAPP: int = 1  # Unidad de Rack
POTENCIA_BASE_WEBAPP: float = 1.0  # MW

# --- Constantes de ServicioCache (US-007) ---
ESPACIO_U_CACHE: int = 1  # Unidad de Rack
POTENCIA_BASE_CACHE: float = 0.5  # MW

# --- Constantes de Asignación de Recursos (US-008) ---
POTENCIA_POR_ASIGNACION: float = 10.0  # MW consumidos por el rack en cada balanceo

# --- Constantes de Estrategia de Consumo (Strategy Pattern) (US-008) ---
# Estrategia Dinámica (Stateful: Database, Batch)
CONSUMO_DINAMICO_ALTO: float = 5.0  # MW
CONSUMO_DINAMICO_BAJO: float = 2.0  # MW
# (La lógica para decidir "alto" o "bajo" se implementará en el Strategy)

# Estrategia Fija (Stateless: WebApp, Cache)
CONSUMO_FIJO_WEBAPP: float = 1.0  # MW
CONSUMO_FIJO_CACHE: float = 2.0  # MW

# --- Constantes de Escalamiento (US-008) ---
ESCALA_IOPS_POR_ASIGNACION: int = 100  # IOPS sumados a DB
ESCALA_WORKERS_POR_ASIGNACION: int = 2   # Workers sumados a Batch


# ==============================================================================
# --- EPIC 3: MONITOREO Y BALANCEO (US-010 a US-013) ---
# ==============================================================================

# --- Sensor de CPU (US-010) ---
INTERVALO_SENSOR_CPU: float = 2.0  # segundos
SENSOR_CPU_MIN: int = 0  # %
SENSOR_CPU_MAX: int = 100  # %

# --- Sensor de RAM (US-011) ---
INTERVALO_SENSOR_RAM: float = 3.0  # segundos
SENSOR_RAM_MIN: int = 0  # %
SENSOR_RAM_MAX: int = 100  # %

# --- Control de Balanceo (US-012) ---
INTERVALO_CONTROL_BALANCEO: float = 2.5  # segundos
CPU_MAX_BALANCEO: int = 80  # % (Regar si CPU > 80%)
RAM_MAX_BALANCEO: int = 70  # % (Regar si RAM > 70%)

# --- Control de Threads (US-013) ---
THREAD_JOIN_TIMEOUT: float = 2.0  # segundos


# ==============================================================================
# --- EPIC 6: PERSISTENCIA (US-021) ---
# ==============================================================================

DIRECTORIO_DATA: str = "data"
EXTENSION_DATA: str = ".dat"