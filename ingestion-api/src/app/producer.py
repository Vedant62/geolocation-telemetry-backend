from aiokafka import AIOKafkaProducer

kafka_producer : AIOKafkaProducer | None = None

def get_producer() -> AIOKafkaProducer:
    return kafka_producer
