# Odoo Modulos Custom
## Resumen de Módulos

### 1. 🚛 Logistics (Gestión de Envíos)

Módulo integral para el control de la cadena de suministro y despacho de mercancías.

* **Integración con Ventas:** Generación automática de órdenes de envío al confirmar una *Sale Order*.
* **Logística Avanzada:** Asignacion de Flota y asignación de choferes.
* **Tracking Externo:** Portal público para que los clientes finales puedan seguir el estado de su envío en tiempo real sin necesidad de login.
* **Informes Técnicos:** Generación de remitos en PDF.

### 2. 💳 Billetera Virtual

Sistema de gestión monetaria interna entre contactos del sistema.

* **Cuentas Virtuales:** Creación de saldos por contacto (`res.partner`).
* **Transacciones:** Flujo de depósitos y transferencias internas seguras entre usuarios.
* **Integración de Pagos:** Permite utilizar el saldo de la billetera virtual como método de pago para facturas y órdenes de venta.

### 3. 🏋️ Membresia de Gimnasio (Gestión de Socios)

Especializado en el control de membresías y acceso a centros deportivos.

* **Vista 360 del Contacto:** Extensión del modelo `res.partner` mediante *Herencia* (Notebook pages) para visualizar el estado de socio, fechas de alta y vencimiento.
* **Control de Membresías:** Registro y trazabilidad de los planes contratados por cada cliente.

### 4. 🏠 Real Estate Management (Gestión Inmobiliaria)

Módulo ligero para la administración de propiedades y ofertas comerciales.

* **Gestión de Propiedades:** Registro detallado de características, ubicación y tipos de inmuebles.
* **Ciclo de Ofertas:** Sistema de registro de ofertas de compra/alquiler enviadas por interesados, con estados de aceptación o rechazo.

**Juan Ignacio Marsilli** - Analista de Sistemas / Desarrollador Python & Odoo.
