"""
The flask application package.
"""

from flask import Flask

from flask import request

import threading
import time
import logging
import sys
import os
import gaiaenv
from collections import OrderedDict
from core.confluent_kafka import Producer, Consumer, KafkaError
from deployer import Deployer

from flask import jsonify

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)
app.logger.info('app startup')

# Create the GaiaEnv object which allows us to introspect the Gaia environment
gaia_env = gaiaenv.GaiaEnv()

config = {
    "bootstrap.servers": "10.191.26.29:9092",
    "group.id": "mygroup",
    "auto.offset.reset": "earliest"
}

import webserver.views
