# Historias de Usuario - Sistema de Infraestructura Cloud **Proyecto**: PythonCloudInfra **Version**: 1.0.0 **Fecha**: Noviembre 2025 **Metodologia**: User Story Mapping (Traducción 1:1 de PythonForestal) --- ## Indice 1. [Epic 1: Gestion de Infraestructura y Racks](#epic-1-gestion-de-infraestructura-y-racks) 2. [Epic 2: Gestion de Servicios de Aplicación](#epic-2-gestion-de-servicios-de-aplicación) 3. [Epic 3: Sistema de Monitoreo y Balanceo](#epic-3-sistema-de-monitoreo-y-balanceo) 4. [Epic 4: Gestion de Personal de SysOps](#epic-4-gestion-de-personal-de-sysops) 5. [Epic 5: Operaciones de Cloud (Alto Nivel)](#epic-5-operaciones-de-cloud-alto-nivel) 6. [Epic 6: Persistencia y Auditoria](#epic-6-persistencia-y-auditoria) 7. [Historias Tecnicas (Patrones de Diseno)](#historias-tecnicas-patrones-de-diseno) ---

## Epic 1: Gestion de Infraestructura y Racks
### US-001: Registrar DataCenter Físico **Como** gerente de infraestructura **Quiero** registrar un DataCenter con su ID único y potencia total **Para** tener un control oficial de mis activos de infraestructura #### Criterios de Aceptacion - [x] El sistema debe permitir crear un DataCenter con: - ID de DataCenter único (entero positivo) - Potencia total en MW (numero positivo) - Ubicación geográfica (cadena de texto) - [x] La potencia debe ser mayor a 0, si no lanzar ValueError - [x] El DataCenter debe poder modificarse posteriormente - [x] El sistema debe validar que los datos sean consistentes #### Detalles Tecnicos **Clase**: DataCenter (python_cloud_infra/entidades/infra/datacenter.py) **Servicio**: DataCenterService (python_cloud_infra/servicios/infra/datacenter_service.py) **Codigo de ejemplo**:
python
from python_cloud_infra.servicios.infra.datacenter_service import DataCenterService

datacenter_service = DataCenterService()
datacenter = datacenter_service.crear_datacenter_con_rack(
    id_datacenter=101,
    potencia_total_mw=50.0,
    ubicacion_geografica="Ashburn, Virginia",
    nombre_rack="Rack A-01"
)

US-002: Crear ServerRack en DataCenter

Como administrador de infraestructura Quiero crear un ServerRack asociado a un DataCenter Para organizar los servicios en unidades físicas identificables

Criterios de Aceptacion

    [x] Un ServerRack debe tener:

        Nombre identificatorio unico

        Espacio máximo en Unidades de Rack (U)

        Potencia disponible inicial (100 MW por defecto)

        Lista de servicios (vacia al inicio)

        Lista de SysAdmins (vacia al inicio)

    [x] El rack debe estar asociado a un DataCenter valido

    [x] La potencia disponible no puede ser negativa

    [x] El sistema debe controlar el espacio ocupado vs disponible

Detalles Tecnicos

Clase: ServerRack (python_cloud_infra/entidades/infra/server_rack.py) Servicio: ServerRackService (python_cloud_infra/servicios/infra/server_rack_service.py)

Codigo de ejemplo:
Python

from python_cloud_infra.entidades.infra.server_rack import ServerRack

rack = ServerRack(
    nombre="Rack A-01",
    espacio_maximo_u=42,
    potencia=100
)

US-003: Crear Registro de DataCenter Completo

Como auditor de activos Quiero crear un registro que vincule DataCenter, Rack, Cliente y Valoración Para tener documentacion oficial completa

Criterios de Aceptacion

    [x] Un RegistroDataCenter debe contener:

        ID de DataCenter (numero unico)

        Referencia a DataCenter

        Referencia a ServerRack

        Nombre del cliente corporativo

        Valoración de activos (numero decimal positivo)

    [x] Todos los campos son obligatorios

    [x] El registro debe poder persistirse y recuperarse

    [x] El registro debe poder mostrarse en consola con formato

Detalles Tecnicos

Clase: RegistroDataCenter (python_cloud_infra/entidades/infra/registro_datacenter.py) Servicio: RegistroDataCenterService (python_cloud_infra/servicios/infra/registro_datacenter_service.py)

Codigo de ejemplo:
Python

from python_cloud_infra.entidades.infra.registro_datacenter import RegistroDataCenter

registro = RegistroDataCenter(
    id_datacenter=101,
    datacenter=datacenter,
    server_rack=rack,
    cliente_corporativo="TechCorp Inc.",
    valoracion_activos=25000000.00
)

Epic 2: Gestion de Servicios de Aplicación

US-004: Desplegar Servicio de Base de Datos (Stateful)

Como Ingeniero DevOps Quiero desplegar un servicio de Base de Datos (ej. PostgreSQL) Para proveer persistencia de datos a las aplicaciones

Criterios de Aceptacion

    [x] Debe poder desplegar multiples instancias de DB

    [x] Cada ServicioDatabase debe tener:

        Tipo de motor (PostgreSQL, MySQL, Mongo, etc.)

        Espacio: 4U (Unidades de Rack)

        Potencia base: 2 MW

        IOPS inicial: 1000

    [x] El sistema debe verificar espacio disponible en el rack

    [x] Si no hay espacio, lanzar EspacioInsuficienteException

    [x] Los servicios deben crearse via Factory Method

Detalles Tecnicos

Clase: ServicioDatabase (python_cloud_infra/entidades/aplicaciones/servicio_database.py) Servicio: ServicioDatabaseService Factory: ServicioFactory

Codigo de ejemplo:
Python

from python_cloud_infra.servicios.infra.server_rack_service import ServerRackService

rack_service = ServerRackService()

# Desplegar 2 instancias de DB (usa Factory Method internamente)
rack_service.desplegar_servicio(rack, "Database", 2)

# Espacio requerido: 2 * 4U = 8U

US-005: Desplegar Servicio de Procesamiento Batch (Stateful)

Como Ingeniero de Datos Quiero desplegar un servicio de procesamiento Batch (ej. Spark) Para ejecutar tareas pesadas (ETL, IA, Reportes)

Criterios de Aceptacion

    [x] Debe poder desplegar multiples servicios Batch

    [x] Cada ServicioBatch debe tener:

        Tipo de Proceso (ETL, IA, REPORTING)

        Espacio: 2U

        Potencia base: 3 MW

        Workers iniciales: 5

    [x] El sistema debe verificar espacio disponible

    [x] Los servicios deben crearse via Factory Method

Detalles Tecnicos

Clase: ServicioBatch (.../aplicaciones/servicio_batch.py) Enum: TipoProceso (.../aplicaciones/tipo_proceso.py) Servicio: ServicioBatchService

Codigo de ejemplo:
Python

# Desplegar 3 servicios Batch
rack_service.desplegar_servicio(rack, "Batch", 3)

# Espacio requerido: 3 * 2U = 6U

US-006: Desplegar Servicio Web App (Stateless)

Como Desarrollador Backend Quiero desplegar una aplicación web (ej. API de Flask/Django) Para atender peticiones de usuarios

Criterios de Aceptacion

    [x] Debe poder desplegar multiples servicios WebApp

    [x] Cada ServicioWebApp debe tener:

        Framework (Flask, Django, FastAPI, etc.)

        Espacio: 1U

        Potencia base: 1 MW

        Balanceado: True (siempre tras un Load Balancer)

    [x] El sistema debe verificar espacio disponible

Detalles Tecnicos

Clase: ServicioWebApp (.../aplicaciones/servicio_webapp.py) Servicio: ServicioWebAppService

Codigo de ejemplo:
Python

# Desplegar 10 instancias de WebApp
rack_service.desplegar_servicio(rack, "WebApp", 10)

# Espacio requerido: 10 * 1U = 10U

US-007: Desplegar Servicio de Cache (Stateless)

Como Ingeniero SRE Quiero desplegar un servicio de Cache (ej. Redis) Para acelerar la respuesta de las WebApps

Criterios de Aceptacion

    [x] Debe poder desplegar multiples servicios de Cache

    [x] Cada ServicioCache debe tener:

        InMemoria (True/False)

        Espacio: 1U

        Potencia base: 0.5 MW

        Balanceado: False (acceso directo)

    [x] El sistema debe verificar espacio disponible

Detalles Tecnicos

Clase: ServicioCache (.../aplicaciones/servicio_cache.py) Servicio: ServicioCacheService

Codigo de ejemplo:
Python

# Desplegar 2 instancias de Cache
rack_service.desplegar_servicio(rack, "Cache", 2)

# Espacio requerido: 2 * 1U = 2U

US-008: Asignar Recursos a Todos los Servicios

Como sistema de balanceo automático Quiero asignar recursos (potencia) a todos los servicios del rack Para manejar fluctuaciones de carga

Criterios de Aceptacion

    [x] La asignación debe:

        Consumir potencia del rack (10 MW por asignación)

        Distribuir potencia a todos los servicios

        Cada servicio consume según su estrategia

        Stateful (DB, Batch): Consumo Dinámico (ej. 5 MW alto, 2 MW bajo)

        Stateless (Web, Cache): Consumo Fijo (ej. 1-2 MW)

    [x] Si no hay suficiente potencia, lanzar PotenciaInsuficienteException

    [x] Los servicios Stateful deben escalar (IOPS, Workers) al recibir recursos

    [x] El sistema debe usar el patron Strategy para consumo

Detalles Tecnicos

Servicio: ServerRackService.asignar_recursos() Estrategias:

    ConsumoDinamicoStrategy (Stateful)

    ConsumoFijoStrategy (Stateless)

Escalamiento:
Python

# ServicioDatabase: +100 IOPS por asignación
# ServicioBatch: +2 Workers por asignación

US-009: Mostrar Datos de Servicios por Tipo

Como SysAdmin Quiero ver los datos de cada servicio de forma especifica Para conocer el estado actual de mis despliegues

Criterios de Aceptacion

    [x] El sistema debe mostrar datos especificos por tipo:

        Database: Servicio, Espacio(U), Potencia(MW), ID, IOPS, Motor

        Batch: Servicio, Espacio(U), Potencia(MW), ID, Workers, Tipo Proceso

        WebApp: Servicio, Espacio(U), Potencia(MW), Framework, Balanceado

        Cache: Servicio, Espacio(U), Potencia(MW), InMemoria

    [x] Usar el patron Registry para dispatch polimorfico

    [x] NO usar cascadas de isinstance()

Detalles Tecnicos

Registry: ServicioRegistry.mostrar_datos()

Epic 3: Sistema de Monitoreo y Balanceo

US-010: Monitorear Carga de CPU en Tiempo Real

Como sistema de monitoreo Quiero leer la carga de CPU cada 2 segundos Para tomar decisiones de balanceo basadas en condiciones reales

Criterios de Aceptacion

    [x] El sensor debe:

        Ejecutarse en un thread daemon separado

        Leer CPU cada 2 segundos

        Generar lecturas aleatorias entre 0% y 100%

        Notificar a observadores cada vez que lee

        Soportar detencion graceful con timeout

    [x] Implementar patron Observer (Observable)

    [x] Usar Generics para tipo-seguridad: Observable[float]

Detalles Tecnicos

Clase: SensorCargaCPUTask (.../monitoreo/sensores/sensor_carga_cpu_task.py) Patron: Observer (Observable[float])

US-011: Monitorear Uso de RAM en Tiempo Real

Como sistema de monitoreo Quiero leer el uso de RAM cada 3 segundos Para complementar datos de CPU en decisiones de balanceo

Criterios de Aceptacion

    [x] El sensor debe:

        Ejecutarse en un thread daemon separado

        Leer RAM cada 3 segundos

        Generar lecturas aleatorias entre 0% y 100%

        Notificar a observadores cada vez que lee

        Soportar detencion graceful con timeout

    [x] Implementar patron Observer (Observable)

    [x] Usar Generics para tipo-seguridad: Observable[float]

Detalles Tecnicos

Clase: SensorUsoRAMTask (.../monitoreo/sensores/sensor_uso_ram_task.py) Patron: Observer (Observable[float])

US-012: Control Automático de Balanceo Basado en Sensores

Como sistema de balanceo de carga Quiero asignar recursos automaticamente cuando se cumplan condiciones Para optimizar el rendimiento de los servicios

Criterios de Aceptacion

    [x] El controlador debe:

        Ejecutarse en un thread daemon separado

        Evaluar condiciones cada 2.5 segundos

        Obtener datos de sensores (PULL, no Observer)

        Asignar recursos cuando:

            CPU > 80%, O

            RAM > 70%

        NO asignar si condiciones no se cumplen

        Manejar excepcion si no hay potencia disponible

    [x] Recibir sensores via inyeccion de dependencias

Detalles Tecnicos

Clase: BalanceadorCargaTask (.../monitoreo/control/balanceador_carga_task.py)

Logica de decision:
Python

if (cpu > CPU_MAX_BALANCEO) or (ram > RAM_MAX_BALANCEO):
    # ASIGNAR RECURSOS
    server_rack_service.asignar_recursos(rack)
else:
    # NO ASIGNAR
    pass

US-013: Detener Sistema de Monitoreo de Forma Segura

Como SysAdmin Quiero detener el sistema de monitoreo de forma controlada Para evitar corrupcion de datos o procesos incompletos

Criterios de Aceptacion

    [x] El sistema debe:

        Detener todos los threads con threading.Event

        Esperar finalizacion con timeout configurable (2s)

        NO forzar terminacion abrupta

        Permitir que threads completen operacion actual

    [x] Threads deben ser daemon

Detalles Tecnicos

Codigo de ejemplo:
Python

# Detener sensores y control
tarea_cpu.detener()
tarea_ram.detener()
tarea_balanceo.detener()

# Esperar finalizacion
tarea_cpu.join(timeout=THREAD_JOIN_TIMEOUT)
...

Epic 4: Gestion de Personal de SysOps

US-014: Registrar SysAdmin con Tickets Asignados

Como jefe de SysOps Quiero registrar SysAdmins con sus tickets asignados Para organizar el trabajo de soporte

Criterios de Aceptacion

    [x] Un SysAdmin debe tener:

        ID de empleado unico (numero entero)

        Nombre completo

        Lista de Tickets de Soporte (puede estar vacia)

        Certificacion de Seguridad (inicialmente sin certificar)

    [x] Los tickets deben tener:

        ID unico

        Fecha de apertura

        Descripcion del problema

        Estado (abierto/cerrado)

    [x] Un SysAdmin puede tener multiples tickets

    [x] Lista de tickets es inmutable (defensive copy)

Detalles Tecnicos

Clases:

    SysAdmin (.../entidades/personal/sysadmin.py)

    TicketSoporte (.../entidades/personal/ticket_soporte.py)

US-015: Asignar Certificación de Seguridad a SysAdmin

Como auditor de seguridad Quiero asignar una Certificacion de Seguridad a un SysAdmin Para certificar que esta apto para manejar infraestructura sensible

Criterios de Aceptacion

    [x] Una CertificacionSeguridad debe tener:

        Estado de aptitud (True/False)

        Fecha de emision

        Nivel de certificación (ej. CISSP, CompTIA+)

    [x] El sistema debe verificar cert. antes de resolver tickets

    [x] Si no tiene cert. valida, no puede ejecutar tickets

    [x] El servicio debe permitir asignar/actualizar cert.

Detalles Tecnicos

Clase: CertificacionSeguridad (.../entidades/personal/certificacion_seguridad.py) Servicio: SysAdminService.asignar_certificacion()

US-016: Resolver Tickets Asignados a SysAdmin

Como SysAdmin Quiero resolver los tickets que me fueron asignados Para completar mi jornada laboral

Criterios de Aceptacion

    [x] El SysAdmin debe:

        Tener certificacion de seguridad valida

        Resolver solo tickets de la fecha especificada

        Usar una consola de software asignada

        Marcar tickets como cerrados

    [x] Los tickets deben resolverse en orden ID descendente

    [x] Si no tiene certificacion, retornar False (no ejecuta)

    [x] Si tiene certificacion, retornar True (ejecuta)

Detalles Tecnicos

Servicio: SysAdminService.resolver_tickets() Clase: SoftwareConsola (.../entidades/personal/software_consola.py) (ej. SSH Client, PowerShell)

US-017: Asignar SysAdmins a ServerRack

Como jefe de SysOps Quiero asignar SysAdmins a un ServerRack especifico Para organizar el personal por rack

Criterios de Aceptacion

    [x] Un ServerRack debe poder tener multiples SysAdmins

    [x] La lista de SysAdmins debe ser inmutable (defensive copy)

    [x] Debe poder obtener lista de SysAdmins

    [x] Debe poder reemplazar lista completa de SysAdmins

Detalles Tecnicos

Clase: ServerRack.set_sysadmins()

Epic 5: Operaciones de Cloud (Alto Nivel)

US-018: Gestionar Múltiples DataCenters

Como proveedor de Cloud Quiero gestionar varios DataCenters desde un servicio centralizado Para tener control unificado de todas mis propiedades

Criterios de Aceptacion

    [x] El servicio debe permitir:

        Agregar DataCenters (RegistroDataCenter)

        Buscar DataCenter por ID

        Aplicar parches a un DataCenter especifico

        Descomisionar y archivar por tipo de servicio

    [x] Debe manejar multiples DataCenters simultaneamente

    [x] Debe usar diccionario interno para almacenar DataCenters

Detalles Tecnicos

Servicio: CloudProviderService (.../servicios/negocio/cloud_provider_service.py)

US-019: Aplicar Parche de Seguridad a DataCenter

Como ingeniero de seguridad Quiero aplicar un parche de seguridad a todos los servicios de un DataCenter Para mitigar vulnerabilidades

Criterios de Aceptacion

    [x] Debe permitir especificar:

        ID de DataCenter a parchear

        Nombre del parche (ej. "CVE-2025-1234")

    [x] Debe aplicar parche a todos los servicios del rack

    [x] Debe mostrar mensaje de confirmacion

    [x] Si DataCenter no existe, manejar error

Detalles Tecnicos

Servicio: CloudProviderService.aplicar_parche_seguridad()

US-020: Descomisionar y Archivar Servicios por Tipo

Como administrador de finanzas Quiero decomisionar todos los servicios de un tipo especifico y archivarlos Para liberar recursos y reducir costos

Criterios de Aceptacion

    [x] Debe permitir decomisionar por tipo de servicio (Class type)

    [x] Debe:

        Buscar todos los servicios del tipo especificado

        Removerlos de todos los ServerRacks

        Archivarlos en un Snapshot generico tipo-seguro

        Mostrar cantidad decomisionada

    [x] Usar Generics para tipo-seguridad: Snapshot[T]

    [x] Permitir mostrar contenido del snapshot

Detalles Tecnicos

Servicio: CloudProviderService.descomisionar_y_archivar() Clase: Snapshot[T] (.../servicios/negocio/snapshot.py)

Codigo de ejemplo:
Python

from python_cloud_infra.entidades.aplicaciones.servicio_webapp import ServicioWebApp

# Decomisionar todas las WebApps
snapshot_webapps = cloud_service.descomisionar_y_archivar(ServicioWebApp)
snapshot_webapps.mostrar_contenido_snapshot()

Epic 6: Persistencia y Auditoria

US-021: Persistir RegistroDataCenter en Disco

Como administrador del sistema Quiero guardar registros de DataCenters en disco Para mantener datos permanentes entre ejecuciones

Criterios de Aceptacion

    [x] El sistema debe:

        Serializar RegistroDataCenter completo con Pickle

        Guardar en directorio data/

        Nombre de archivo: {cliente_corporativo}.dat

        Crear directorio si no existe

        Mostrar mensaje de confirmacion

    [x] Si ocurre error, lanzar InfraPersistenciaException

    [x] Cerrar recursos apropiadamente en bloque finally

Detalles Tecnicos

Servicio: RegistroDataCenterService.persistir()

US-022: Recuperar RegistroDataCenter desde Disco

Como auditor Quiero recuperar registros de DataCenters guardados previamente Para consultar historicos y realizar auditorias

Criterios de Aceptacion

    [x] El sistema debe:

        Deserializar archivo .dat con Pickle

        Buscar en directorio data/

        Validar que cliente no sea nulo/vacio

        Retornar RegistroDataCenter completo

        Mostrar mensaje de confirmacion

    [x] Si archivo no existe, lanzar InfraPersistenciaException

    [x] Si archivo corrupto, lanzar InfraPersistenciaException

    [x] Cerrar recursos apropiadamente en bloque finally

Detalles Tecnicos

Servicio: RegistroDataCenterService.leer_registro() (metodo estatico)

US-023: Mostrar Datos Completos de RegistroDataCenter

Como auditor Quiero ver todos los datos de un registro de DataCenter en formato legible Para analizar la informacion completa de un activo

Criterios de Aceptacion

    [x] El sistema debe mostrar:

        Encabezado "REGISTRO DATACENTER"

        ID de DataCenter

        Cliente Corporativo

        Valoración de Activos

        Ubicación Geográfica

        Espacio total en U del Rack

        Cantidad de servicios desplegados

        Listado detallado de cada servicio

    [x] Cada servicio debe mostrarse con datos especificos de su tipo

    [x] Usar Registry para dispatch polimorfico

Detalles Tecnicos

Servicio: RegistroDataCenterService.mostrar_datos()

Historias Tecnicas (Patrones de Diseno)

US-TECH-001: Implementar Singleton para ServicioRegistry

Como arquitecto de software Quiero garantizar una unica instancia del registro de servicios de aplicación Para compartir estado consistente entre todos los servicios

Criterios de Aceptacion

    [x] Implementar patron Singleton thread-safe

    [x] Usar double-checked locking con Lock

    [x] Metodo get_instance() para acceso

    [x] Constructor __new__ para controlar instanciacion

Detalles Tecnicos

Clase: ServicioRegistry

US-TECH-002: Implementar Factory Method para Creacion de Servicios

Como arquitecto de software Quiero centralizar creacion de servicios mediante Factory Method Para desacoplar cliente de clases concretas

Criterios de Aceptacion

    [x] Crear clase ServicioFactory con metodo estatico

    [x] Soportar creacion de: Database, Batch, WebApp, Cache

    [x] Usar diccionario de factories (no if/elif cascades)

    [x] Lanzar ValueError si especie desconocida

    [x] Retornar tipo base Servicio (no tipos concretos)

    [x] NO usar lambdas - usar metodos estaticos dedicados

Detalles Tecnicos

Clase: ServicioFactory

US-TECH-003: Implementar Observer Pattern para Sensores

Como arquitecto de software Quiero implementar patron Observer con Generics Para notificar cambios de sensores de forma tipo-segura

Criterios de Aceptacion

    [x] Crear clase Observable[T] generica

    [x] Crear interfaz Observer[T] generica

    [x] Soportar multiples observadores

    [x] Sensores heredan de Observable[float] (para CPU% y RAM%)

    [x] Thread-safe en notificaciones

Detalles Tecnicos

Clases: Observable[T], Observer[T]

US-TECH-004: Implementar Strategy Pattern para Consumo de Recursos

Como arquitecto de software Quiero implementar algoritmos intercambiables de consumo de recursos Para permitir diferentes estrategias segun tipo de servicio

Criterios de Aceptacion

    [x] Crear interfaz ConsumoRecursosStrategy abstracta

    [x] Implementar ConsumoDinamicoStrategy (Stateful)

    [x] Implementar ConsumoFijoStrategy (Stateless)

    [x] Inyectar estrategia en constructor de servicios

    [x] Servicios delegan calculo a estrategia

    [x] Estrategias usan constantes de constantes.py

Detalles Tecnicos

Interfaz: ConsumoRecursosStrategy Implementaciones: ConsumoDinamicoStrategy, ConsumoFijoStrategy

US-TECH-005: Implementar Registry Pattern para Dispatch Polimorfico

Como arquitecto de software Quiero eliminar cascadas de isinstance() Para mejorar mantenibilidad y extensibilidad

Criterios de Aceptacion

    [x] Crear diccionarios de handlers por tipo

    [x] Registrar handler para cada tipo de servicio

    [x] Metodo asignar_recursos() usa dispatch automatico

    [x] Metodo mostrar_datos() usa dispatch automatico

    [x] Lanzar error si tipo no registrado

    [x] NO usar lambdas - usar metodos de instancia dedicados

Detalles Tecnicos

Clase: ServicioRegistry
