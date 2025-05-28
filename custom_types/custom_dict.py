from typing import TypedDict

class KafkaProducerMessage(TypedDict):
    key: str
    value: dict
