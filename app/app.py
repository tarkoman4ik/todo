import logging

from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

from logging_config import setup_logging

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

setup_logging()

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

logger = logging.getLogger(__name__)


@app.route('/api/logs')
def LogPyController():
    logger.info("Test user logging", extra={
        'user': 'john_doe',
        'ip': '192.168.1.1',
        'tags': ['auth', 'success']
    })
    logger.warning('Some warn')
    logger.error('Some error')
    try:
        raise Exception("Test exception")
    except Exception as e:
        logger.error("Database error", exc_info=True, extra={
            'component': 'database',
            'query': 'SELECT * FROM users'
        })
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
