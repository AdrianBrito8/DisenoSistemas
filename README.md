# Sistema de Infraestructura Cloud (PythonCloudInfra)

Este proyecto implementa un sistema de simulación para la gestión de infraestructura de un Data Center, aplicando un conjunto estricto de patrones de diseño de software.  
Es una re-implementación conceptual del proyecto `PythonForestal`, aplicando los mismos principios a un nuevo dominio (IT y Cloud).

---

## ✨ Características Principales

El sistema simula las siguientes funcionalidades clave:

* **Gestión de Infraestructura:** Creación de `ServerRacks` (los contenedores), `DataCenters` y `RegistrosDataCenter` (el objeto persistible).
* **Gestión de Servicios:** Soporte para 4 tipos de aplicaciones (`ServicioWebApp`, `ServicioDatabase`, `ServicioCache`, `ServicioBatch`) que se ejecutan en los racks.
* **Balanceo de Carga:** Sistema concurrente (`Threads`) con `SensorCargaCPUTask` y `SensorUsoRAMTask` que informan a un `BalanceadorCargaTask`.
* **Gestión de Personal (SysOps):** Registro de `SysAdmin` (Administradores de Sistemas), asignación de `TicketSoporte` y validación de `CertificacionSeguridad`.
* **Operaciones de Cloud (Alto Nivel):** Un `CloudProviderService` que gestiona múltiples Data Centers y puede `descomisionar_servicio` (el análogo a "cosechar").
* **Persistencia:** Guardado y lectura de `RegistroDataCenter` en disco usando Pickle.

---

## 🏗️ Patrones de Diseño Implementados

Este proyecto aplica los mismos 5 patrones de diseño que el proyecto original:

1. **Singleton (Thread-Safe):** Utilizado en `ServicioRegistry` para garantizar una única instancia del registro de servicios de aplicaciones.  
2. **Factory Method:** Implementado en `ServicioFactory` para la creación desacoplada de los 4 tipos de `Servicio`.  
3. **Observer:** Usado en el sistema de monitoreo (`SensorCargaCPUTask` y `SensorUsoRAMTask` como `Observable[float]`).  
4. **Strategy:** Aplicado para definir algoritmos de consumo de recursos (`ConsumoDinamicoStrategy` para DB/Batch vs. `ConsumoFijoStrategy` para Web/Cache), inyectados en los servicios de aplicación.  
5. **Registry:** Utilizado en `ServicioRegistry` para el despacho polimórfico de operaciones (ej. `asignar_recursos`), eliminando la necesidad de `isinstance()`.

---

## 📁 Estructura del Proyecto

La estructura de archivos es análoga a la del proyecto original:

```
PythonCloudInfra/
├── python_cloud_infra/        # Paquete principal del código fuente
│   ├── constantes.py 
│   ├── entidades/ 
│   │   ├── aplicaciones/
│   │   ├── personal/
│   │   └── infra/ 
│   ├── excepciones/ 
│   ├── patrones/ 
│   ├── monitoreo/ 
│   │   ├── control/
│   │   └── sensores/
│   └── servicios/             # Lógica de negocio (Service Layer)
│       ├── aplicaciones/      # (Incluye el Registry/Singleton)
│       ├── negocio/
│       ├── personal/
│       └── infra/
├── .gitignore
├── buscar_paquete.py          # Script de integración 
├── main.py 
├── README.md 
├── RUBRICA_AUTOMATIZADA.md    # (Reutilizada)
├── RUBRICA_EVALUACION.md      # (Reutilizada)
└── USER_STORIES.md 
```

---

## 🚀 Cómo Ejecutar

### 1. Ejecutar la Simulación Principal

Este comando ejecuta el flujo completo definido en `main.py`, demostrando todas las funcionalidades:

```bash
python3 main.py
```

### 2. Generar el Archivo Integrador

Este comando utiliza el script `buscar_paquete.py` para consolidar todo el código fuente:

```bash
python3 buscar_paquete.py integrar python_cloud_infra
```

---

## Autor

**Adrián Brito**
