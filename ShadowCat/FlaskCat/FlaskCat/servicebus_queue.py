from azure.servicebus import ServiceBusService, Message, Queue
import ast


class ServiceBusQueue(object):
    def __init__(self,
                 namespace,
                 access_key_name,
                 access_key_value,
                 q_name,
                 q_max_size='5120',
                 msg_ttl='PT1M'):
        self.bus_svc = ServiceBusService(
            service_namespace=namespace,
            shared_access_key_name=access_key_name,
            shared_access_key_value=access_key_value
        )
        self.queue_options = Queue()
        self.queue_options.max_size_in_megabytes = q_max_size
        self.queue_options.default_message_time_to_live = msg_ttl

        self.queue_name = q_name
        self.bus_svc.create_queue(self.queue_name, self.queue_options)

    def send(self, msg):
        message = bytes(msg)
        message = Message(message)
        self.bus_svc.send_queue_message(self.queue_name, message)

    def receive(self):
        msg = self.bus_svc.receive_queue_message(self.queue_name, peek_lock=False)
        data = ast.literal_eval(msg.body)
        return data
