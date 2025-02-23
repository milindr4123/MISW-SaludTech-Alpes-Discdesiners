from hsm.seedwork.aplicacion.comandos import Comando
from hsm.modulos.semilla.aplicacion.dto import SemillaDTO
from .base import CrearSemillaBaseHandler
from dataclasses import dataclass
from hsm.seedwork.aplicacion.comandos import ejecutar_commando as comando

from hsm.modulos.semilla.dominio.entidades import Semilla
from hsm.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from hsm.modulos.semilla.aplicacion.mapeadores import MapeadorSemilla
from hsm.modulos.semilla.infraestructura.repositorios import RepositorioSemilla

@dataclass
class CrearSemilla(Comando):
    formato: str
    lenght: str


class CrearSemillaHandler(CrearSemillaBaseHandler):
    
    def handle(self, comando: CrearSemilla):
        semilla_dto = SemillaDTO(
                length=comando.lenght,
                formato=comando.formato)

        semilla: Semilla = self.fabrica_semillas.crear_objeto(semilla_dto, MapeadorSemilla())
        semilla.crear_reserva(reserva)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioReservas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, reserva)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(CrearReserva)
def ejecutar_comando_crear_reserva(comando: CrearReserva):
    handler = CrearReservaHandler()
    handler.handle(comando)
    