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

