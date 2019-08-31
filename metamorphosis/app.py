import time

from core.shared.common import info
from use_cases.app.start_use_case import run as app

if __name__ == '__main__':
    info("Starting Methamophosis app server...")
    app()
    time.sleep(2)
    info("Methamophosis app server terminated!")