##
# File: core\shared\broker_consumer.py.
#
# Summary:  Broker consumer class.

import asyncio
import os
import signal
import sys

from confluent_kafka import Consumer, KafkaError, KafkaException

from metamorphosis.core.shared.common import get_logger, info


class BrokerConsumer(object):

    def __init__(self, *args, **kwargs):
        # Consumer configuration
        # See
        # https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        config = {
            "bootstrap.servers": os.environ["CLOUDKARAFKA_BROKERS"],
            "group.id": "%s-consumer" % os.environ["CLOUDKARAFKA_USERNAME"],
            "session.timeout.ms": 6000,
            "default.topic.config": {"auto.offset.reset": "smallest"},
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "SCRAM-SHA-256",
            "sasl.username": os.environ["CLOUDKARAFKA_USERNAME"],
            "sasl.password": os.environ["CLOUDKARAFKA_PASSWORD"]
        }

        self.topic_prefix = os.environ["CLOUDKARAFKA_TOPIC_PREFIX"]
        self.consumer = Consumer(**config)
        self.handlers = {}
        self.logger = get_logger()
        self.loop = asyncio.get_event_loop()
        # return super().__init__(*args, **kwargs)

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
            handlers = self.handlers[msg.topic()]
            for handler in handlers:
                handler(msg)
            self.consumer.commit()
        except Exception as e:
            self.logger.critical(str(e), exc_info=1)
            # self.consumer.close()
            sys.exit("Exited due to exception")

    def _signal_term_handler(self, signal, frame):
        info("closing consumer")
        # self.consumer.close()
        # sys.exit(0)

    def start(self):
        topics = [*self.handlers.keys()]
        self.consumer.subscribe(topics=topics)
        info("starting consumer...registered signterm")

        signal.signal(signal.SIGTERM, self._signal_term_handler)
        signal.signal(signal.SIGINT, self._signal_term_handler)
        # signal.signal(signal.SIGQUIT, self._signal_term_handler)
        # signal.signal(signal.SIGHUP, self._signal_term_handler)

        self.loop.run_until_complete(self._consume())
        # from python 3.7+ will be to wonder use
        # asyncio.run(self._consume())

    async def _consume(self):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue
                if msg.error():
                    # Error or event
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        info("Reached end at offset {0}\n".format(
                            msg.offset()))
                    elif msg.error():
                        # Error
                        raise KafkaException(msg.error())
                else:
                    self._run_handlers(msg)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
