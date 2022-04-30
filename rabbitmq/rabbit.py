import pika


class Rabbit:
    def __init__(self, ip, port, queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue)
        self.queue = queue

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class RabbitProvider(Rabbit):
    def __init__(self, ip, port, queue):
        super().__init__(ip, port, queue)

    def publish(self, body):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=body)


class RabbitConsumer(Rabbit):
    def __init__(self, ip, port, queue):
        super().__init__(ip, port, queue)

    def set_callback(self, callback):
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback)
        self.channel.start_consuming()
