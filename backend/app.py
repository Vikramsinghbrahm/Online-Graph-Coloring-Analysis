import logging
import signal
import sys

from graph_coloring.api import create_app

app = create_app()
logger = logging.getLogger(__name__)


def _handle_shutdown(signal_number, _frame):
    signal_name = signal.Signals(signal_number).name
    logger.info("app.shutdown_requested", extra={"signal_name": signal_name})
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _handle_shutdown)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _handle_shutdown)

    app.run(
        host=app.config["APP_HOST"],
        port=app.config["APP_PORT"],
        debug=app.config["APP_DEBUG"],
    )
