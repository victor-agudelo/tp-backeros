import pytest
from datetime import datetime
from utils.message_creator import MessageCreator


def test_message_creator_initialization():
    message = {
        "pedidoListoTimestamp": "2025-01-14T15:30:45.123",
        "pedido_id": "123456789"
    }
    code = "1234"
    creator = MessageCreator(message, code)

    assert creator.pedido_finalizado == "2025-01-14 15:30:45"
    assert creator.pedido_id == "6789"
    assert creator.code == "1234"

def test_final_message_format():
    message = {
        "pedidoListoTimestamp": "2025-01-14T15:30:45.123",
        "pedido_id": "123456789"
    }
    code = "1234"
    creator = MessageCreator(message, code)

    expected_message = (
        """Hola,
        Tu pedido finalizado en 6789 ha finalizado a las 2025-01-14 15:30:45.
        
        Puedes acercarte a reclamarlo al restaurante con el código 1234.
        """
    )

    assert creator.final_message() == expected_message

def test_missing_fields_in_message():
    message = {
        "pedidoListoTimestamp": "2025-01-14T15:30:45.123"
    }
    code = "1234"
    with pytest.raises(TypeError):
        MessageCreator(message, code)

def test_invalid_timestamp_format():
    message = {
        "pedidoListoTimestamp": "invalid-timestamp",
        "pedido_id": "123456789"
    }
    code = "1234"
    with pytest.raises(ValueError):
        MessageCreator(message, code)

def test_short_pedido_id():
    message = {
        "pedidoListoTimestamp": "2025-01-14T15:30:45.123",
        "pedido_id": "123"
    }
    code = "1234"
    creator = MessageCreator(message, code)

    assert creator.pedido_id == "123"
