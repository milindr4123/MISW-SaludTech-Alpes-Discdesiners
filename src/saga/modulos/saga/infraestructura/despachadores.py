import requests
import pulsar
from pulsar.schema import *
from saga.seedwork.infraestructura import utils

class DespachadorComandos:
    def enviar_comando(self, servicio, comando, datos):
        url = f"http://{servicio}/api/{comando.lower()}"
        response = requests.post(url, json=datos)
        if response.status_code != 200:
            raise Exception(f"Fallo en {comando}")
        
        
    def publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_mensaje_async(self, mensaje, topico, schema):
        cliente =  pulsar.Client(f'pulsar://localhost:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(schema))
        publicador.send(mensaje)
        publicador.close()
        cliente.close()