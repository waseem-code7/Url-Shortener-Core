from typing import Dict, TypedDict

class KafkaProducerMessage(TypedDict):
    key: str
    value: str
