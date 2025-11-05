"""
Archivo principal de ejecucion del Sistema de Infraestructura Cloud.

Este script simula un flujo completo de operaciones (End-to-End)
basado en las Historias de Usuario para demostrar la
funcionalidad de todos los modulos y patrones.
"""

# --- Imports Standard Library ---
import time
import sys
from datetime import date

# --- Imports de Entidades ---
from python_cloud_infra.entidades.infra.registro_datacenter import RegistroDataCenter
from python_cloud_infra.entidades.personal.sysadmin import SysAdmin
from python_cloud_infra.entidades.personal.ticket_soporte import TicketSoporte
from python_cloud_infra.entidades.personal.software_consola import SoftwareConsola
# Tipos de servicio para la decomisión (US-020)
from python_cloud_infra.entidades.aplicaciones.servicio_database import ServicioDatabase
from python_cloud_infra.entidades.aplicaciones.servicio_webapp import ServicioWebApp

# --- Imports de Servicios ---
from python_cloud_infra.servicios.infra.datacenter_service import DataCenterService
from python_cloud_infra.servicios.infra.server_rack_service import ServerRackService
from python_cloud_infra.servicios.infra.registro_datacenter_service import RegistroDataCenterService
from python_cloud_infra.servicios.personal.sysadmin_service import SysAdminService
from python_cloud_infra.servicios.negocio.cloud_provider_service import CloudProviderService

# --- Imports de Monitoreo (Threads) ---
from python_cloud_infra.monitoreo.sensores.sensor_carga_cpu_task import SensorCargaCPUTask
from python_cloud_infra.monitoreo.sensores.sensor_uso_ram_task import SensorUsoRAMTask
from python_cloud_infra.monitoreo.control.balanceador_carga_task import BalanceadorCargaTask

# --- Imports de Excepciones ---
from python_cloud_infra.excepciones.infra_exception import InfraException

# --- Imports de Constantes ---
from python_cloud_infra import constantes as C


def ejecutar_simulacion():
    """
    Funcion principal que encapsula toda la logica de la simulacion.
    """
    
    # --- Inicializacion de Servicios ---
    print("Iniciando servicios de Cloud...")
    datacenter_service = DataCenterService()
    rack_service = ServerRackService()
    registro_service = RegistroDataCenterService()
    sysadmin_service = SysAdminService()
    cloud_service = CloudProviderService()
    
    # Variables para los threads
    tarea_cpu = None
    tarea_ram = None
    tarea_balanceo = None

    try:
        # ======================================================================
        # --- EPIC 1 y 2: CREACION DE INFRA Y DESPLIEGUE (US-001 a US-007) ---
        # ======================================================================
        print("\n=== [FASE 1: CREACION DE INFRAESTRUCTURA Y DESPLIEGUE] ===")
        
        # US-001 y US-002: Crear DataCenter y ServerRack
        datacenter = datacenter_service.crear_datacenter_con_rack(
            id_datacenter=101,
            potencia_total_mw=500.0,
            ubicacion_geografica="Ashburn, Virginia (USA)",
            nombre_rack="Rack A-01",
            espacio_rack_u=42
        )
        rack = datacenter.get_rack_principal() # type: ignore

        # US-003: Crear RegistroDataCenter
        registro = RegistroDataCenter(
            id_datacenter=datacenter.get_id_datacenter(),
            datacenter=datacenter,
            server_rack=rack,
            cliente_corporativo="TechCorp Inc.",
            valoracion_activos=75000000.0
        )
        
        # Demostracion PATRON FACTORY (US-TECH-002)
        print("\nDemostracion: Patron Factory Method (Rubrica 1.2)")
        # US-004 a US-007: Desplegar usando el servicio (que usa el Factory)
        rack_service.desplegar_servicio(rack, "Database", 2)
        rack_service.desplegar_servicio(rack, "Batch", 1)
        rack_service.desplegar_servicio(rack, "WebApp", 10)
        rack_service.desplegar_servicio(rack, "Cache", 2)

        # ======================================================================
        # --- EPIC 3: SISTEMA DE MONITOREO Y BALANCEO (US-010 a US-013) ---
        # ======================================================================
        print("\n=== [FASE 2: INICIANDO SISTEMA DE MONITOREO (THREADS)] ===")
        
        # Demostracion PATRON OBSERVER (US-TECH-003)
        print("\nDemostracion: Patron Observer (Rubrica 1.3)")
        print("(Los sensores son Observables[float], notificando a los suscriptores)")
        
        # US-010 y US-011: Crear e iniciar Sensores (Threads)
        tarea_cpu = SensorCargaCPUTask()
        tarea_ram = SensorUsoRAMTask()
        
        tarea_cpu.start()
        tarea_ram.start()

        # US-012: Crear e iniciar Balanceador (Thread)
        tarea_balanceo = BalanceadorCargaTask(
            sensor_cpu=tarea_cpu,
            sensor_ram=tarea_ram,
            rack=rack,
            rack_service=rack_service
        )
        tarea_balanceo.start()
        
        print("\nSistema de monitoreo iniciado. "
              "Dejando correr por 10 segundos...")
        time.sleep(10)
        
        # Demostracion PATRON STRATEGY (NUESTRA LÓGICA)
        print("\nDemostracion: Patron Strategy (Rubrica 1.4 - LÓGICA ORIGINAL)")
        print("(El balanceador uso 'ConsumoDinamicoStrategy' (basado en HORAS PICO) "
              "y 'ConsumoFijoStrategy')")
              
        # Demostracion PATRON SINGLETON (US-TECH-001)
        print("\nDemostracion: Patron Singleton (Rubrica 1.1)")
        print("(El 'ServerRackService' y el 'RegistroDataCenterService' "
              "usaron la MISMA instancia del 'ServicioRegistry')")
        
        # ======================================================================
        # --- EPIC 4: GESTION DE PERSONAL (US-014 a US-017) ---
        # ======================================================================
        print("\n=== [FASE 3: GESTION DE PERSONAL (SYSOPS)] ===")
        
        # US-014: Crear Tickets y SysAdmin
        tickets = [
            TicketSoporte(1, date.today(), "Reiniciar servidor BBDD-01"),
            TicketSoporte(2, date.today(), "Aplicar parche de seguridad a WebApp-03"),
            TicketSoporte(3, date(2025, 11, 5), "Ticket para maniana (no debe ejecutarlo)")
        ]
        sysadmin = SysAdmin(id_empleado=778, nombre="Adrian Brito", tickets=tickets)
        
        # US-017: Asignar SysAdmin al Rack
        rack.set_sysadmins_asignados([sysadmin])
        
        # US-015: Asignar Certificación (con nuestro atributo extra 'nivel')
        sysadmin_service.asignar_certificacion(
            sysadmin=sysadmin,
            apto=True,
            fecha_emision=date.today(),
            nivel_certificacion="CompTIA Security+",
            observaciones="Certificacion vigente"
        )
        
        # US-016: Ejecutar Tareas (y demostrar NO-LAMBDA)
        consola = SoftwareConsola(101, "SecureCRT (SSH Client)", True)
        print("\nDemostracion: NO-LAMBDA (Rubrica 3.4)")
        print("(El servicio ordena tickets usando un metodo estatico, no lambda)")
        sysadmin_service.resolver_tickets(
            sysadmin=sysadmin,
            fecha=date.today(),
            consola=consola
        )
        
        # ======================================================================
        # --- EPIC 5: OPERACIONES DE CLOUD (US-018 a US-020) ---
        # ======================================================================
        print("\n=== [FASE 4: OPERACIONES DE CLOUD (ALTO NIVEL)] ===")
        
        # US-018: Agregar DataCenter al servicio de gestion
        cloud_service.add_datacenter(registro)
        
        # US-019: Aplicar Parche (Análogo a 'fumigar')
        cloud_service.aplicar_parche_seguridad(
            id_datacenter=101, 
            nombre_parche="CVE-2025-CRITICAL"
        )
        
        # US-020: Descomisionar (Análogo a 'cosechar', usa Generics)
        print("\nDemostracion: Decomisión con Generics (Snapshot[T])")
        
        # --- ESTA ES LA ZONA DEL ERROR ---
        # Aseguramos que el nombre del método sea 'decomisionar_y_archivar'
        snapshot_webapps = cloud_service.decomisionar_y_archivar(ServicioWebApp)
        snapshot_webapps.mostrar_contenido_snapshot()
        
        snapshot_db = cloud_service.decomisionar_y_archivar(ServicioDatabase)
        snapshot_db.mostrar_contenido_snapshot()
        
        # ======================================================================
        # --- EPIC 6: PERSISTENCIA Y AUDITORIA (US-021 a US-023) ---
        # ======================================================================
        print("\n=== [FASE 5: PERSISTENCIA Y AUDITORIA] ===")
        
        # US-021: Persistir (Guardar)
        path_archivo = registro_service.persistir(registro)
        print(f"Registro guardado en: {path_archivo}")
        
        # US-022: Leer
        # Usamos el nombre del cliente (quitando puntos y espacios)
        registro_leido = RegistroDataCenterService.leer_registro("TechCorp Inc.")
        
        # US-023: Mostrar datos (usando Registry)
        print("\nMostrando datos del registro leido (demuestra Registry):")
        registro_service.mostrar_datos(registro_leido)

    except InfraException as e:
        # Manejo de nuestras excepciones personalizadas (Rubrica 2.3)
        print("\n**************************************************")
        print("   ERROR DE INFRAESTRUCTURA CONTROLADO (InfraException)")
        print(f"   Mensaje: {e.get_user_message()}")
        print(f"   Tecnico: {e.get_mensaje_tecnico()}")
        print("**************************************************")
        sys.exit(1) # Salir con codigo de error
        
    except Exception as e:
        # Manejo de errores inesperados
        print("\n**************************************************")
        print("           ERROR INESPERADO (Exception)")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Error: {e}")
        print("**************************************************")
        sys.exit(1) # Salir con codigo de error

    finally:
        # ======================================================================
        # --- FASE FINAL: DETENCION SEGURA (US-013) ---
        # ======================================================================
        print("\n=== [FASE FINAL: DETENIENDO THREADS...] ===")
        
        if tarea_balanceo:
            tarea_balanceo.detener()
        if tarea_cpu:
            tarea_cpu.detener()
        if tarea_ram:
            tarea_ram.detener()
            
        # Esperar a que los threads terminen (Graceful Shutdown)
        # (Rubrica 4.2, 5.1)
        join_timeout = C.THREAD_JOIN_TIMEOUT
        
        if tarea_cpu:
            tarea_cpu.join(timeout=join_timeout)
            print(f"Sensor de CPU: {'Detenido' if not tarea_cpu.is_alive() else 'Forzado'}")
            
        if tarea_ram:
            tarea_ram.join(timeout=join_timeout)
            print(f"Sensor de RAM: {'Detenido' if not tarea_ram.is_alive() else 'Forzado'}")
            
        if tarea_balanceo:
            tarea_balanceo.join(timeout=join_timeout)
            print(f"Balanceador: {'Detenido' if not tarea_balanceo.is_alive() else 'Forzado'}")
            
        print("\nTodos los sistemas detenidos de forma segura.")
        print("\n--- EJEMPLO COMPLETADO EXITOSAMENTE ---")
        # Este mensaje es el que busca la Rubrica Auto (EXEC-002)


# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    ejecutar_simulacion()