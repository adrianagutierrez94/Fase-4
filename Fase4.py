# SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA: SOFTWARE FJ
# Lenguaje: Python

from abc import ABC, abstractmethod
from datetime import datetime
import logging
import uuid

# 1. CONFIGURACION DEL SISTEMA DE LOGS

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")

# 2. EXCEPCIONES PERSONALIZADAS

class ErrorSistema(Exception):
 """Excepcion general del sistema."""
    pass
 
class DatosInvalidosError(ErrorSistema):
"""Error cuando los datos ingresados son incorrectos."""
    pass

class ClienteNoEncontradoError(ErrorSistema):
 """Error cuando un cliente no existe."""
    pass

class ServicioNoDisponibleError(ErrorSistema):
"""Error cuando un servicio no esta disponible."""
    pass

class ReservaInvalidaError(ErrorSistema):
"""Error cuando una reserva no cumple las condiciones."""
    pass

class OperacionNoPermitidaError(ErrorSistema)
"""Error cuando se intenta realizar una operacion prohibida."""
    pass

# 3. CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):

def __init__(self):
    self._id = str(uuid.uuid4())[:8]

@property
def id(self):
return self._id

@abstractmethod
  def mostrar_informacion(self):
  pass

# 4. CLASE CLIENTE

class Cliente(Entidad):
  
def __init__(self, nombre, documento, correo, telefono):

super().__init__()

self.__nombre = self.validar_texto(nombre, "nombre")
self.__documento = self.validar_texto(documento, "documento")
self.__correo = self.validar_correo(correo)
self.__telefono = self.validar_telefono(telefono)

# Encapsulacion y validaciones

def validar_texto(self, valor, campo):

if not isinstance(valor, str) or not valor.strip():
raise DatosInvalidosError(
f"El campo {campo} no puede estar vacio."
)

return valor.strip()

def validar_correo(self, correo):

if not isinstance(correo, str):
raise DatosInvalidosError("El correo debe ser texto.")

correo = correo.strip()

if "@" not in correo or "." not in correo:
raise DatosInvalidosError("Correo electronico invalido.")

return correo

def validar_telefono(self, telefono):

if not isinstance(telefono, str):
raise DatosInvalidosError("El telefono debe ser texto.")

telefono = telefono.strip()

if not telefono.isdigit() or len(telefono) < 7:
raise DatosInvalidosError("Numero de telefono invalido.")

return telefono

@property
def nombre(self):
return self.__nombre

@property
def documento(self):
return self.__documento

@property
def correo(self):
return self.__correo

@property
def telefono(self):
return self.__telefono

def mostrar_informacion(self):

return (
f"ID: {self.id} | "
f"Nombre: {self.nombre} | "
f"Documento: {self.documento} | "
f"Correo: {self.correo} | "
f"Telefono: {self.telefono}"
)

# 5. CLASE ABSTRACTA SERVICIO

class Servicio(Entidad, ABC):

def __init__(self, nombre, precio_base):

super().__init__()

if not isinstance(nombre, str) or not nombre.strip():
raise DatosInvalidosError(
 "El nombre del servicio es obligatorio."
 )

if (
isinstance(precio_base, bool)
or not isinstance(precio_base, (int, float))
or precio_base <= 0
):
raise DatosInvalidosError(
"El precio base debe ser mayor que cero."
)

self._nombre = nombre.strip()
self._precio_base = float(precio_base)
self._disponible = True

@property
def nombre(self):
return self._nombre

@property
def precio_base(self):
return self._precio_base

@property
def disponible(self):
return self._disponible

def cambiar_disponibilidad(self, estado):

if not isinstance(estado, bool):
raise DatosInvalidosError(
"La disponibilidad debe ser verdadera o falsa."
)

self._disponible = estado

def validar_duracion(self, duracion):

if (
isinstance(duracion, bool)
or not isinstance(duracion, (int, float))
or duracion <= 0
):
raise DatosInvalidosError(
"La duracion debe ser un numero mayor que cero."
)

# Metodo con parametros opcionales.
# Permite calcular costos con diferentes combinaciones:
# calcular_costo(duracion)
# calcular_costo(duracion, descuento)
# calcular_costo(duracion, descuento, impuesto)

def calcular_costo(
self,
duracion=1,
descuento=0,
impuesto=0
):

self.validar_duracion(duracion)

if (
isinstance(descuento, bool)
or not isinstance(descuento, (int, float))
or not 0 <= descuento <= 100
):
raise DatosInvalidosError(
"El descuento debe estar entre 0 y 100."
)

if (
isinstance(impuesto, bool)
or not isinstance(impuesto, (int, float))
or not 0 <= impuesto <= 100
):
raise DatosInvalidosError(
"El impuesto debe estar entre 0 y 100."
)

subtotal = self.precio_base * duracion

valor_descuento = subtotal * descuento / 100

subtotal_con_descuento = subtotal - valor_descuento

valor_impuesto = subtotal_con_descuento * impuesto / 100

total = subtotal_con_descuento + valor_impuesto

return round(total, 2)

@abstractmethod
def validar_parametros(self, duracion):
pass

@abstractmethod
def describir_servicio(self):
pass

@abstractmethod
def mostrar_informacion(self):
pass

# 6. SERVICIO ESPECIALIZADO: RESERVA DE SALAS

class ReservaSala(Servicio):

def __init__(self, nombre, precio_base, capacidad):

super().__init__(nombre, precio_base)

if (
isinstance(capacidad, bool)
or not isinstance(capacidad, int)
or capacidad <= 0
):
raise DatosInvalidosError(
"La capacidad debe ser un entero positivo."
)

self.__capacidad = capacidad

@property
def capacidad(self):
return self.__capacidad

def validar_parametros(self, duracion):

self.validar_duracion(duracion)

if duracion > 12:
raise DatosInvalidosError(
"La sala no puede reservarse por mas de 12 horas."
)

def describir_servicio(self):

return (
f"Sala de reuniones: {self.nombre}. "
f"Capacidad: {self.capacidad} personas."
)

def mostrar_informacion(self):

return (
f"[RESERVA DE SALA] {self.describir_servicio()} "
f"Precio por hora: ${self.precio_base}"
)

# 7. SERVICIO ESPECIALIZADO: ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):

def __init__(self, nombre, precio_base, tipo_equipo):

super().__init__(nombre, precio_base)

if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
raise DatosInvalidosError(
"Debe especificar el tipo de equipo."
)

self.__tipo_equipo = tipo_equipo.strip()

@property
def tipo_equipo(self):
return self.__tipo_equipo

def validar_parametros(self, duracion):

self.validar_duracion(duracion)

if duracion > 168:
raise DatosInvalidosError(
"El alquiler no puede superar 168 horas."
)

def describir_servicio(self):

return (
f"Alquiler de equipo: {self.nombre}. "
f"Tipo: {self.tipo_equipo}."
)

def mostrar_informacion(self):

return (
f"[ALQUILER DE EQUIPO] {self.describir_servicio()} "
f"Precio por hora: ${self.precio_base}"
)

# 8. SERVICIO ESPECIALIZADO: ASESORIAS

class Asesoria(Servicio):

def __init__(self, nombre, precio_base, especialidad):

super().__init__(nombre, precio_base)

if not isinstance(especialidad, str) or not especialidad.strip():
raise DatosInvalidosError(
"Debe especificar la especialidad."
)

self.__especialidad = especialidad.strip()

@property
def especialidad(self):
return self.__especialidad

def validar_parametros(self, duracion):

self.validar_duracion(duracion)

if duracion > 8:
raise DatosInvalidosError(
"Una asesoria no puede superar 8 horas."
)

def describir_servicio(self):

return (
f"Asesoria especializada: {self.nombre}. "
f"Area: {self.especialidad}."
)

def mostrar_informacion(self):

return (
f"[ASESORIA] {self.describir_servicio()} "
f"Precio por hora: ${self.precio_base}"
)

# 9. CLASE RESERVA

class Reserva(Entidad):

def __init__(self, cliente, servicio, duracion):

super().__init__()

if not isinstance(cliente, Cliente):
raise DatosInvalidosError(
"Debe proporcionar un cliente valido."
)

if not isinstance(servicio, Servicio):
raise DatosInvalidosError(
"Debe proporcionar un servicio valido."
)

servicio.validar_parametros(duracion)

if not servicio.disponible:
raise ServicioNoDisponibleError(
"El servicio seleccionado no esta disponible."
)

self.__cliente = cliente
self.__servicio = servicio
self.__duracion = duracion
self.__estado = "PENDIENTE"
self.__costo = 0

logger.info(
f"Reserva creada: {self.id} - Cliente: {cliente.nombre}"
)

@property
def estado(self):
return self.__estado

@property
def costo(self):
return self.__costo

@property
def cliente(self):
return self.__cliente

@property
def servicio(self):
return self.__servicio

def confirmar(self):

try:

if self.__estado != "PENDIENTE":
raise OperacionNoPermitidaError(
"Solo se pueden confirmar reservas pendientes."
)

if not self.__servicio.disponible:
raise ServicioNoDisponibleError(
"El servicio ya no esta disponible."
)

self.__costo = self.__servicio.calcular_costo(
self.__duracion,
descuento=0,
impuesto=19
)

self.__estado = "CONFIRMADA"

logger.info(
f"Reserva {self.id} confirmada. "
f"Costo: ${self.__costo}"
)

return self.__costo

except ErrorSistema as error:

logger.error(
f"Error al confirmar reserva {self.id}: {error}"
)

raise

def cancelar(self):

try:

if self.__estado != "PENDIENTE":
raise OperacionNoPermitidaError(
"No se puede cancelar una reserva "
"que no este pendiente."
)

self.__estado = "CANCELADA"

logger.info(
f"Reserva {self.id} cancelada."
)

except ErrorSistema as error:

logger.error(
f"Error al cancelar reserva {self.id}: {error}"
)

raise

def procesar(self):

try:

if self.__estado != "PENDIENTE":
raise OperacionNoPermitidaError(
"La reserva no se encuentra pendiente."
)

return self.confirmar()

except Exception as error:

logger.exception(
f"Error durante el procesamiento de la reserva {self.id}"
)

raise ReservaInvalidaError(
"No fue posible procesar la reserva."
) from error

finally:

logger.info(
f"Finalizo el procesamiento de la reserva {self.id}."
)

def mostrar_informacion(self):

return (
f"Reserva: {self.id} | "
f"Cliente: {self.cliente.nombre} | "
f"Servicio: {self.servicio.nombre} | "
f"Duracion: {self.__duracion} horas | "
f"Estado: {self.estado} | "
f"Costo: ${self.costo}"
)

# 10. CLASE GESTOR DEL SISTEMA

class GestorSistema:

def __init__(self):

self.__clientes = []
self.__servicios = []
self.__reservas = []

logger.info("Sistema Software FJ iniciado.")

# REGISTRAR CLIENTES

def registrar_cliente(self, cliente):

if not isinstance(cliente, Cliente):
raise DatosInvalidosError(
"El objeto proporcionado no es un cliente valido."
)

for existente in self.__clientes:

if existente.documento == cliente.documento:
raise OperacionNoPermitidaError(
"Ya existe un cliente con ese documento."
)

self.__clientes.append(cliente)

logger.info(
f"Cliente registrado: {cliente.nombre}"
)

return cliente

# REGISTRAR SERVICIOS

def registrar_servicio(self, servicio):

if not isinstance(servicio, Servicio):
raise DatosInvalidosError(
"El objeto proporcionado no es un servicio valido."
)

for existente in self.__servicios:

if existente.id == servicio.id:
raise OperacionNoPermitidaError(
"El servicio ya se encuentra registrado."
)

self.__servicios.append(servicio)

logger.info(
f"Servicio registrado: {servicio.nombre}"
)

return servicio

# BUSCAR CLIENTES

def buscar_cliente(self, documento):

for cliente in self.__clientes:

if cliente.documento == documento:
return cliente

raise ClienteNoEncontradoError(
"No se encontro el cliente solicitado."
)

# BUSCAR SERVICIOS

def buscar_servicio(self, identificador):

for servicio in self.__servicios:

if servicio.id == identificador:
return servicio

raise ServicioNoDisponibleError(
"No se encontro el servicio solicitado."
)

# CREAR RESERVAS 

def crear_reserva(self, documento, id_servicio, duracion):

cliente = self.buscar_cliente(documento)

servicio = self.buscar_servicio(id_servicio)

reserva = Reserva(
cliente,
servicio,
duracion
)

self.__reservas.append(reserva)

logger.info(
f"Reserva {reserva.id} agregada al sistema."
)

return reserva

# MOSTRAR CLIENTES

def listar_clientes(self):

print("\n========== LISTA DE CLIENTES ==========")

if not self.__clientes:
print("No hay clientes registrados.")
return

for cliente in self.__clientes:
print(cliente.mostrar_informacion())

# MOSTRAR SERVICIOS

def listar_servicios(self):

print("\n========== LISTA DE SERVICIOS ==========")

if not self.__servicios:
print("No hay servicios registrados.")
return

for servicio in self.__servicios:
print(servicio.mostrar_informacion())

# MOSTRAR RESERVAS 

def listar_reservas(self):

print("\n========== LISTA DE RESERVAS ==========")

if not self.__reservas:
print("No hay reservas registradas.")
return

for reserva in self.__reservas:
print(reserva.mostrar_informacion())

# 11. FUNCION PARA EJECUTAR OPERACIONES CON EXCEPCIONES 

def ejecutar_operacion(nombre, funcion):

print(f"\n>>> OPERACION: {nombre}")

try:

resultado = funcion()

except ErrorSistema as error:

print(f"[ERROR CONTROLADO] {error}")

logger.error(
f"Operacion '{nombre}' fallida: {error}"
)

except (TypeError, ValueError) as error:

print(f"[ERROR DE DATOS] {error}")

logger.exception(
f"Error de datos en '{nombre}'"
)

except Exception as error:

print(f"[ERROR INESPERADO] {error}")

logger.exception(
f"Error inesperado en '{nombre}'"
)

else:

print("[CORRECTO] Operacion realizada.")

if resultado is not None:
print(resultado)

finally:

print("Operacion finalizada.")

logger.info(
f"Finalizo la operacion: {nombre}"
)

# 12. SIMULACION DE OPERACIONES 

def main():

print("=" * 60)
print("       SISTEMA INTEGRAL DE GESTION")
print("                 SOFTWARE FJ")
print("=" * 60)

sistema = GestorSistema()

# OPERACION 1: REGISTRAR CLIENTE VALIDO

def operacion_1():

cliente = Cliente(
"Carlos Ramirez",
"100100100",
"carlos@gmail.com",
"3101234567"
)

sistema.registrar_cliente(cliente)

return cliente.mostrar_informacion()

ejecutar_operacion(
"Registrar cliente valido",
operacion_1

# OPERACION 2: REGISTRAR OTRO CLIENTE

def operacion_2():

cliente = Cliente(
"Maria Lopez",
"200200200",
"maria@gmail.com",
"3201234567"
)

sistema.registrar_cliente(cliente)

return cliente.mostrar_informacion()

ejecutar_operacion(
"Registrar segundo cliente",
operacion_2
)
)

# OPERACION 3: REGISTRAR CLIENTE INVALIDO

def operacion_3():

cliente = Cliente(
"",
"300300300",
"correo_invalido",
"123"
)
sistema.registrar_cliente(cliente)

ejecutar_operacion(
"Registrar cliente con datos invalidos",
operacion_3
)

# OPERACION 4: REGISTRAR SERVICIO DE SALA

def operacion_4():

sala = ReservaSala(
"Sala de conferencias",
50000,
20
)

sistema.registrar_servicio(sala)

return sala.mostrar_informacion()

ejecutar_operacion(
"Registrar servicio de sala",
operacion_4
)

#OPERACION 5: REGISTRAR ALQUILER DE EQUIPOS

def operacion_5():

equipo = AlquilerEquipo(
"Computador portatil",
15000,
"Portatil"
)

sistema.registrar_servicio(equipo)

return equipo.mostrar_informacion()

ejecutar_operacion(
"Registrar servicio de alquiler de equipos",
operacion_5
)

# OPERACION 6: REGISTRAR ASESORIA

def operacion_6():

asesoria = Asesoria(
"Asesoria tecnologica",
80000,
"Ingenieria de sistemas"
)

sistema.registrar_servicio(asesoria)

return asesoria.mostrar_informacion()

ejecutar_operacion(
"Registrar servicio de asesoria",
operacion_6
)

# OPERACION 7: CREAR SERVICIO INVALIDO

def operacion_7():

servicio = ReservaSala(
"Sala invalida",
-5000,
0
)

sistema.registrar_servicio(servicio)

ejecutar_operacion(
"Crear servicio con parametros incorrectos",
operacion_7
)

# OPERACION 8: CREAR RESERVA EXITOSA

reserva_exitosa = None

def operacion_8():

nonlocal reserva_exitosa

cliente = sistema.buscar_cliente("100100100")

sala = sistema._GestorSistema__servicios[0]

reserva_exitosa = sistema.crear_reserva(
cliente.documento,
sala.id,
3
)

costo = reserva_exitosa.procesar()

return (
reserva_exitosa.mostrar_informacion()
)

ejecutar_operacion(
"Crear y confirmar reserva exitosa",
operacion_8
)

# OPERACION 9: CREAR RESERVA CON DURACION INVALIDA

def operacion_9():

cliente = sistema.buscar_cliente("100100100")

sala = sistema._GestorSistema__servicios[0]

sistema.crear_reserva(
cliente.documento,
sala.id,
20
)

ejecutar_operacion(
"Crear reserva con duracion incorrecta",
operacion_9
)

# OPERACION 10: BUSCAR CLIENTE INEXISTENTE

def operacion_10():

return sistema.buscar_cliente("999999999")

ejecutar_operacion(
"Buscar cliente inexistente",
 operacion_10
)

# OPERACION 11: SERVICIO NO DISPONIBLE

def operacion_11():

sala = sistema._GestorSistema__servicios[0]

sala.cambiar_disponibilidad(False)

return "El servicio fue marcado como no disponible."

ejecutar_operacion(
"Deshabilitar servicio",
operacion_11
)

# OPERACION 12: INTENTAR RESERVAR SERVICIO NO DISPONIBLE

def operacion_12():

cliente = sistema.buscar_cliente("200200200")

sala = sistema._GestorSistema__servicios[0]

sistema.crear_reserva(
cliente.documento,
sala.id,
2
)

ejecutar_operacion(
"Reservar servicio no disponible",
operacion_12
)

# OPERACION 13: INTENTAR CANCELAR RESERVA CONFIRMADA

 def operacion_13():

reserva_exitosa.cancelar()

ejecutar_operacion(
"Cancelar una reserva confirmada",
operacion_13
)

# OPERACION 14: CALCULO CON DESCUENTO E IMPUESTOS

 def operacion_14():

equipo = sistema._GestorSistema__servicios[1]

costo = equipo.calcular_costo(
5,
descuento=10,
impuesto=19
)

return f"Costo final del alquiler: ${costo}"

ejecutar_operacion(
"Calcular costo con descuento e impuestos",
operacion_14
)

# OPERACION 15: MOSTRAR INFORMACION DEL SISTEMA

def operacion_15():

sistema.listar_clientes()

sistema.listar_servicios()

sistema.listar_reservas()

ejecutar_operacion(
"Consultar informacion general",
operacion_15
)

# FINALIZACION

print("\n" + "=" * 60)
print("       SIMULACION FINALIZADA")
print("       SOFTWARE FJ")
print("=" * 60)

print("\nTodos los errores y eventos fueron registrados")
print("en el archivo: software_fj.log")

# 13. EJECUCION PRINCIPAL

if __name__ == "__main__":

try:

main()

except Exception as error:

logger.critical(
"Error critico durante la ejecucion del sistema.",
exc_info=True
)

print("Se produjo un error critico:", error)

finally:

print("\nSistema Software FJ finalizado.")
