import os
import signal
import sys

from confluent_kafka import Consumer as BrokerConsumer

from core.shared.common import get_logger


class Consumer(object):

    def __init__(self, *args, **kwargs):
        # Consumer configuration
        # See
        # https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        self.config = {
            'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
            'group.id': "%s-consumer" % os.environ['CLOUDKARAFKA_USERNAME'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
            'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
        }
        
        self.topic_prefix = os.environ['CLOUDKARAFKA_TOPIC_PREFIX']
        self.consumer = BrokerConsumer(**self.config)
        self.handlers = {}
        self.logger = get_logger()

        return super().__init__(*args, **kwargs)

    def _add_handler(self, topic, handler):
        if self.handlers.get(topic) is None:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def handle(self, topic):
        def decorator(f):
            self._add_handler(topic, f)
            return f
        return decorator

    def _run_handlers(self, msg):
        try:
            handlers = self.handlers[msg.topic]
            for handler in handlers:
                handler(msg)
            self.consumer.commit()
        except Exception as e:
            self.logger.critical(str(e), exc_info=1)
            self.consumer.close()
            sys.exit("Exited due to exception")

    def signal_term_handler(self, signal, frame):
        self.logger.info("closing consumer")
        self.consumer.close()
        sys.exit(0)

    def start(self):
        #
        self.consumer.subscribe(topics=["siumlj60-default"])
        #self.consumer.subscribe(topics=" ".join(self.handlers.keys()))
        self.logger.info("starting consumer...registered signterm")

        signal.signal(signal.SIGTERM, self.signal_term_handler)
        signal.signal(signal.SIGINT, self.signal_term_handler)
        #signal.signal(signal.SIGQUIT, self.signal_term_handler)
        #signal.signal(signal.SIGHUP, self.signal_term_handler)

        for msg in self.consumer:
            self.logger.info(
                "TOPIC: {}, PAYLOAD: {}".format(msg.topic, msg.value))
            self._run_handlers(msg)

# try:
#    while True:
#        msg = c.poll(timeout=1.0)

#        if msg is None:
#            continue
#        if msg.error():
#            # Error or event
#            if msg.error().code() == KafkaError._PARTITION_EOF:
#                # End of partition event
#                sys.stderr.write('%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset()))
#            elif msg.error():
#                # Error
#                raise KafkaException(msg.error())
#        else:
#            # Proper message
#            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' % (msg.topic(), msg.partition(), msg.offset(),
#                                str(msg.key())))
#            print(msg.value())

# except KeyboardInterrupt:
#    sys.stderr.write('%% Aborted by user\n')

# Close down consumer to commit final offsets.
# c.close()

# self.c =
# c.subscribe(self.topics)
#self.topics = os.environ['CLOUDKARAFKA_TOPIC'].split(",")
