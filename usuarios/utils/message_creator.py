from datetime import datetime

class MessageCreator:
    def __init__(self, message, code):
        self.pedido_finalizado = datetime.strptime(message.get('pedidoListoTimestamp'), "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
        self.pedido_id = message.get("pedido_id")[-4:]
        self.code = code

    def final_message(self):
        return f"""Hola,
        Tu pedido finalizado en {self.pedido_id} ha finalizado a las {self.pedido_finalizado}.
        
        Puedes acercarte a reclamarlo al restaurante con el código {self.code}.
        """
