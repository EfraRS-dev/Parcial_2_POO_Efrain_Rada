import datetime as dt
import random as rnd
import unittest

class Turno:
    def __init__(self, ruta, camion):
        self.ruta: Ruta = ruta
        self.camion: Camion = camion
        self.h_inicio: dt = dt.datetime.now() 

        f = self.h_inicio
        a = 0
        for i in range(1, 4):
            if f.hour + i < 23:
                a = rnd.randint(0, i) 
        ff = dt.datetime(f.year, f.month, f.day, f.hour + a, rnd.randint(0, 59), rnd.randint(0, 59))

        self.h_fin: dt = ff 
        self.duracion: dt = ff - f
        self.residuos: list[Residuo] = []

    def __iter__(self):
        return IteradorResiduosTurno(self.residuos)

    def getEmpleados(self):
        return self.camion.personal


class IteradorResiduosTurno:

    def __init__(self, datos) -> None:
            self.datos: list = datos
            self.index: int = 0

    def __iter__(self):
            return self

    def __next__(self):
            if self.index < len(self.datos):
                valor = self.data[self.index]
                self.index += 1
                return valor
            else:
                raise StopIteration


class CentroAcopio:
  
    _instance = None
    tipos = {1: 'vidrio', 2: 'papel', 3: 'plástico', 4: 'metal', 5: 'residuos orgánicos', 6: 'otro'}

    def __new__(cls):  # Implementación de patrón Singleton 
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        tipos = CentroAcopio.tipos    
        self.turnos: list[Turno] = []
        self.camiones: list[Camion] = []
        self.empleados: list[Empleado] = []
        self.rutas: list[Ruta] = []
        self.residuos: dict[str: list[Residuo]] = {tipos[1]: [], tipos[2]: [], tipos[3]: [],
                                                  tipos[4]: [], tipos[5]: [], tipos[6]: []}

    def addEmpleado(self, empleado):
        self.empleados.append(empleado)

    def addCamion(self, camion):
        self.camiones.append(camion)

    def removeEmpleado(self, empleado):
        if empleado in self.empleados:
            self.empleados.remove(empleado)
        else:
            print('El empleado no pudo ser eliminado. No existe.')

    def removeCamion(self, camion):
        if camion in self.camiones:
            self.camiones.remove(camion)
        else:
            print('El camión no pudo ser eliminado. No existe.')

  
    def getCantidadResiduo(self, tipo: str) -> float:
        # Calcula la masa total del residuo de cualquier tipo
        m_total = 0
        for t in self.turnos: 
            for r in t:
                if r.tipo == tipo:
                        m_total += r.masa
        return m_total 
        # (f'Masa total del residuo {tipo} del día {fecha}: {m_total}')

    def registrarTurno(self, ruta, camion):
        if isinstance(ruta, Ruta) and isinstance(camion, Camion):
            self.addTurno(Turno(ruta, camion))
        else:
            raise TypeError

    def addTurno(self, turno):
        self.turnos.append(turno)
        self.clasificarResiduos(turno)

    def clasificarResiduos(self, turno):
        for r in turno:
            self.residuos[r.tipo].append(r) 


class Empleado:
  def __init__(self, id: int, nombre: str, email: str, celular: int, tipo: str):
    self.id: int = id
    self.nombre: str = nombre
    self.email: str = email
    self.celular: str = celular
    self.tipo: str = tipo
    self.asignado: bool = False

  def __repr__(self) -> str:
     return f'Empleado: {self.nombre}\nId: {self.id}\nTipo: {self.tipo}'
  

class PuntoGeografico:
    def __init__(self, lat, lon):
        self.latitud: float = lat
        self.longitud: float = lon

    def __repr__(self) -> str:
       return f'({self.latitud}, {self.longitud})'


class Camion:
    def __init__(self, placa: str, marca: str, combustible: int, capacidad: float):
      self.placa: str = placa
      self._marca: str = marca
      self._combustible: int = combustible  # galones
      self.capacidad: float = capacidad  # kg.
      self.personal: list[Empleado] = []
      self.residuos: list[Residuo] = []

    def addPersonal(self, empleado: Empleado):
        if not empleado.asignado:
            if len(self.personal) < 3:
                if empleado.tipo == 'Conductor':
                    for e in self.personal:
                        if e.tipo == empleado.tipo:
                            print('Ya hay un conductor en este camión.')
                            return
                    empleado.asignado = True
                    self.personal.append(empleado)        
                else:
                    empleado.asignado = True
                    self.personal.append(empleado)
                print(f'El empleado/a {empleado.nombre} ha sido agregado al sistema.')
            else:
                print(f'El camión {self.placa} ya tiene asignado todo su personal.')
        else:
            print(f'El empleado/a {empleado.nombre} ya se encuentra asignado.')

    def removePersonal(self, empleado: Empleado):
        if empleado in self.personal:
            self.personal.remove(empleado)
            print(f'El empleado/a {empleado.nombre} ha sido eliminado del sistema.')
        else:
            print(f'El empleado/a {empleado.nombre} no pudo ser eliminado. No existe.')

    def recogerResiduo(self, residuo):
        cap = residuo.masa
        for rs in self.residuos:
            cap += rs.masa
        if self.capacidad > cap:
            self.residuos.append(residuo)
        else:
            print('El camión se encuentra completamente lleno.')
        

      
class Residuo:
    tipos = {1: 'vidrio', 2: 'papel', 3: 'plástico', 4: 'metal', 5: 'residuos orgánicos', 6: 'otro'}
  
    def __init__(self, masa, tipo):
        self.masa: float = masa
        self.tipo: str = Residuo.tipos[tipo]



class Ruta:
    def __init__(self, puntos: list[PuntoGeografico]):
        self.ubicaciones: list[PuntoGeografico] = puntos


""" A partir de aquí, se definirá la clase de pruebas unitarias y sus respectivas pruebas con el módulo Unittest  """

class PruebasUnitarias(unittest.TestCase):
    def test_excepcionRegistroTurno(self):
        sistema_test = CentroAcopio()
        self.assertRaises(TypeError, CentroAcopio.registrarTurno, sistema_test, 1, 'str')

    def test_getResiduos(self):
        sistema_test = CentroAcopio()
        self.assertIsInstance()

          

""" Esta sección del código es la implementación de las clases anteriores. Todo se realiza sin input del usuario. """

if __name__ == "__main__":

    print('\nSistema de recolección - Trash City\n')
    # Rutas generadas al azar
    ruta1 = Ruta([PuntoGeografico(10.982978, -74.788391),
                PuntoGeografico(10.977623, -74.792509),
                PuntoGeografico(10.990705, -74.802147),
                PuntoGeografico(11.002209, -74.805451)])
    ruta2 = Ruta([PuntoGeografico(10.985366, -74.794895),
                PuntoGeografico(10.993726, -74.794684),
                PuntoGeografico(10.979849, -74.804511),
                PuntoGeografico(11.006281, -74.783942)])
    ruta3 = Ruta([PuntoGeografico(10.988205, -74.798023),
                PuntoGeografico(10.994617, -74.785942),
                PuntoGeografico(10.968143, -74.791982),
                PuntoGeografico(10.997529, -74.806495),
                PuntoGeografico(10.984051, -74.787314)])

    rutas_list = [ruta1, ruta2, ruta3]
    rtp = {1: 'vidrio', 2: 'papel', 3: 'plástico', 4: 'metal', 5: 'residuos orgánicos', 6: 'otro'}
    trc = CentroAcopio()

    trc.addEmpleado(Empleado(12345678, 'Efraín Rada', 'eradaa@uninorte.edu.co', '3128267589', 'Conductor'))
    trc.addEmpleado(Empleado(98765432, 'Carlos Sánchez', '', '3104567890', 'Conductor'))
    trc.addEmpleado(Empleado(12365478, 'Juan Pérez', 'jp567@uninorte.edu.co', '3155678901', 'Recolector'))
    trc.addEmpleado(Empleado(45678912, 'Liliana Escobar', '', '3042197654', 'Recolector'))
    trc.addEmpleado(Empleado(98745612, 'Andrea Buitrago', 'andreab1@uninorte.edu.co', '3114665321', 'Recolector'))
    trc.addEmpleado(Empleado(97531123, 'Manuel Yepes', 'myepes@uninorte.edu.co', '304567218', 'Recolector'))

    cm1 = Camion('OQR202', 'Volvo', 43, 6000)
    cm1.addPersonal(trc.empleados[0])
    cm1.addPersonal(trc.empleados[2])
    cm1.addPersonal(trc.empleados[1])  # Ya hay un conductor.
    cm1.addPersonal(trc.empleados[3])
    cm1.addPersonal(trc.empleados[1])  # El camión cm1 ya está lleno.

    cm2 = Camion('FGX892', 'Chevrolet', 41, 5500)
    cm2.addPersonal(trc.empleados[0])  # Este empleado ya fue asignado.
    cm2.addPersonal(trc.empleados[1])  
    cm2.addPersonal(trc.empleados[4])
    cm2.addPersonal(trc.empleados[3])  # Este empleado ya fue asignado.
    cm2.addPersonal(trc.empleados[5])

    cm3 = Camion('AJG887', 'Volkswagen', 39, 3700)

    trc.addCamion(cm1)
    trc.addCamion(cm2)
    trc.addCamion(cm3)
    trc.removeCamion(cm3)

    cm1 = trc.camiones[0]
    cm2 = trc.camiones[1]

    for ruta in rutas_list:
        cm1.recogerResiduo(Residuo(20 + 10 * rnd.random(), rnd.randint(1,6)))
        cm1.recogerResiduo(Residuo(30 + 10 * rnd.random(), rnd.randint(1,6)))
        trc.registrarTurno(ruta, cm1)
        cm2.recogerResiduo(Residuo(20 + 10 * rnd.random(), rnd.randint(1,6)))
        cm2.recogerResiduo(Residuo(30 + 10 * rnd.random(), rnd.randint(1,6)))
        trc.registrarTurno(ruta, cm2)

    
    unittest.main()
    





""" La empresa de manejo de residuos “TrashCity” necesita un sistema de información
para administrar su operación. El primer servicio de la empresa consiste en la
recolección de los residuos de la ciudad: camiones de la empresa recorren la ciudad
en rutas preestablecidas tomando los residuos dispuestos por los usuarios. Una ruta
contiene la serie de puntos geográficos (latitud, longitud) por donde debe pasar es
camión.

Cada camión cuenta con un conductor y dos asistentes de recolección en un turno. Un turno
define el recorrido completo de un camión y su equipo a recoger residuos, en un rango de día
y hora de inicio y finalización, siguiendo una de las rutas existentes. En el turno se almacena
la localización geográfica y tiempo en el que pasó en su recorrido.

Al final de turno, la carga del camión pasa a ser clasificada en un centro de acopio. El
resultado de la separación se almacena en el sistema asociado al turno: cuántas toneladas
de vidrio, papel, plástico, metal y residuos orgánicos.

De los elementos camión y persona se almacena información básica de identificación.

Para resolver este problema usted debe:
a. Realizar un diagrama de clase UML para representar el modelo de la solución.
(Criterios de evaluación: Clases necesarias, relaciones adecuadas, uso del estándar,
estructura que reduce redundancia de información y facilidad de acceso a la
información)

b. Implemente en Python los métodos que permitan el cálculo de la cantidad de vidrio
que se recogió en todas las rutas de un día en específico. Asuma que métodos get y
set de los atributos ya existen, y que clases como LocalDateTime ya existen en el
sistema. La clase de punto geográfico debe ser definida por en el UML.

c. Implemente un plan de pruebas donde verifique la funcionalidad de su solución para
este sistema de información.
Nota: Deberá compartir si solución como un repositorio en git, donde se encuentre todo lo
necesario para poder ejecutar y así mismo la documentación lo más detallada posible. """