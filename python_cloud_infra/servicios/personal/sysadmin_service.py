"""
Modulo del servicio SysAdminService.
Maneja la logica de negocio de la gestion de personal (SysOps).
"""
from datetime import date
from typing import List, TYPE_CHECKING

# --- Imports de Entidades ---
from python_cloud_infra.entidades.personal.sysadmin import SysAdmin
from python_cloud_infra.entidades.personal.certificacion_seguridad import CertificacionSeguridad
from python_cloud_infra.entidades.personal.ticket_soporte import TicketSoporte, EstadoTicket

if TYPE_CHECKING:
    from python_cloud_infra.entidades.personal.software_consola import SoftwareConsola

class SysAdminService:
    """
    Servicio para gestionar la logica de negocio de los SysAdmins.
    
    Implementa US-015 (Asignar Certificación) y US-016 (Resolver Tickets).
    """

    def asignar_certificacion(self,
                              sysadmin: SysAdmin,
                              apto: bool,
                              fecha_emision: date,
                              nivel_certificacion: str,
                              observaciones: str | None = None) -> None:
        """
        Crea y asigna una CertificacionSeguridad a un SysAdmin.
        Implementacion de US-015.

        Args:
            sysadmin (SysAdmin): El SysAdmin a certificar.
            apto (bool): True si esta apto (certificado).
            fecha_emision (date): Fecha del certificado.
            nivel_certificacion (str): Nivel de la certificacion (ej. "CISSP").
            observaciones (str | None, optional): Comentarios.
        """
        print(f"\n--- Asignando Certificacion de Seguridad a {sysadmin.get_nombre()} ---")
        
        # 1. Crear la entidad CertificacionSeguridad (con nuestro atributo extra)
        certificacion = CertificacionSeguridad(
            apto=apto,
            fecha_emision=fecha_emision,
            nivel_certificacion=nivel_certificacion,
            observaciones=observaciones
        )
        
        # 2. Asignarla al SysAdmin
        sysadmin.set_certificacion(certificacion)
        
        if apto:
            print(f"SysAdmin {sysadmin.get_nombre()} ahora esta APTO (Nivel: {nivel_certificacion}).")
        else:
            print(f"SysAdmin {sysadmin.get_nombre()} ahora esta NO APTO.")

    @staticmethod
    def _obtener_id_ticket(ticket: TicketSoporte) -> int:
        """
        Metodo helper estatico para el ordenamiento de tickets.
        
        Se usa en lugar de 'lambda' para cumplir con la
        Rubrica 3.4 y Rubrica Auto (QUAL-002).
        (Análogo a '_obtener_id_tarea')
        
        Args:
            ticket (TicketSoporte): El ticket del que se extrae el ID.

        Returns:
            int: El ID del ticket.
        """
        return ticket.get_id_ticket()

    def resolver_tickets(self,
                         sysadmin: SysAdmin,
                         fecha: date,
                         consola: 'SoftwareConsola') -> bool:
        """
        Ejecuta los tickets asignados a un SysAdmin para una fecha dada.
        Implementacion de US-016. (Análogo a 'trabajar')

        Args:
            sysadmin (SysAdmin): El SysAdmin que ejecutara las tareas.
            fecha (date): La fecha de los tickets a resolver.
            consola (SoftwareConsola): El software a utilizar.

        Returns:
            bool: True si pudo trabajar, False si no tenia certificacion.
        """
        print(f"\n--- {sysadmin.get_nombre()} intenta resolver tickets (Fecha: {fecha}) ---")
        
        # 1. Validacion de Certificacion de Seguridad (Criterio de Aceptacion US-016)
        cert = sysadmin.get_certificacion()
        if cert is None or not cert.esta_apto():
            print(f"ERROR: {sysadmin.get_nombre()} no puede trabajar. "
                  f"No tiene Certificacion de Seguridad vigente.")
            return False # No puede trabajar

        # 2. Obtener todos los tickets
        todos_los_tickets = sysadmin.get_tickets()
        
        # 3. Filtrar tickets por fecha y estado
        tickets_para_hoy = [
            t for t in todos_los_tickets
            if t.get_fecha() == fecha and t.get_estado() == EstadoTicket.ABIERTO
        ]

        if not tickets_para_hoy:
            print(f"{sysadmin.get_nombre()} no tiene tickets abiertos para hoy.")
            return True # Pudo "trabajar" (no hacer nada)

        # 4. Ordenar por ID descendente (Criterio US-016)
        #    Usamos el metodo estatico en 'key' para evitar lambda
        tickets_para_hoy.sort(key=self._obtener_id_ticket, reverse=True)

        # 5. Ejecutar (resolver) tickets
        print(f"{sysadmin.get_nombre()} comienza a resolver tickets con: {consola.get_nombre()}")
        for ticket in tickets_para_hoy:
            print(f"  -> Resolviendo ticket {ticket.get_id_ticket()}: {ticket.get_descripcion()}")
            ticket.cerrar_ticket() # Marcar como cerrado
            
        print(f"Tickets de {sysadmin.get_nombre()} resueltos.")
        return True # Trabajo exitoso