from metamorphosis.core.shared.common import info
from metamorphosis.use_cases.app.start import run as app

if __name__ == "__main__":
    info("Starting Methamophosis app server...")
    app()
    info("Methamophosis app server terminated!")
    