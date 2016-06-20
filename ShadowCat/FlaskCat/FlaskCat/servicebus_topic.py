from azure.servicebus import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME
import ast


class ServiceBusTopic(object):
    rule = None
    topic_name = ''
    topic_options = None

    def __init__(self,
                 namespace,
                 access_key_name,
                 access_key_value,
                 topic_name,
                 subscription_name='',
                 topic_max_size='5120',
                 msg_ttl='PT1M'):
        self.bus_service = ServiceBusService(
            service_namespace=namespace,
            shared_access_key_name=access_key_name,
            shared_access_key_value=access_key_value
        )
        self.create_topic(topic_name, topic_max_size, msg_ttl)

        if subscription_name != '':
            self.create_subscription(subscription_name)

    def create_topic(self,
                     topic_name,
                     topic_max_size='5120',
                     msg_ttl='PT1M'):
        self.topic_name = topic_name
        self.topic_options = Topic()
        self.topic_options.max_size_in_megabytes = topic_max_size
        self.topic_options.default_message_time_to_live = msg_ttl

    def create_subscription(self, subscription_name):
        self.bus_service.create_subscription(self.topic_name, subscription_name)

    def create_filter(self,
                      filter_type,
                      filter_expression,
                      subscription_name,
                      rule_name):
        self.rule = Rule()
        self.rule.filter_type = filter_type
        self.rule.filter_expression = filter_expression

        self.bus_service.create_rule(self.topic_name, subscription_name, rule_name, self.rule)
        self.bus_service.delete_rule(self.topic_name, subscription_name, DEFAULT_RULE_NAME)

    def send(self, msg):
        message = Message(bytes(msg))
        self.bus_service.send_topic_message(self.topic_name, message)

    def receive(self, subscription_name, lock_message=False):
        message = self.bus_service.receive_subscription_message(
            self.topic_name, subscription_name, peek_lock=lock_message
        )
        return message.body

    def lock_and_receive(self, subscription_name):
        return self.receive(subscription_name, True)
