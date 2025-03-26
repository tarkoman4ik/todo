import logging
import os

from opentelemetry import trace
from pythonjsonlogger import json


class TracingFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        span = trace.get_current_span()
        if span and span.is_recording():
            context = span.get_span_context()
            log_record.update({
                "traceId": f"{context.trace_id:032x}",
                "spanId": f"{context.span_id:016x}",
            })


def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), "var", "logs")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = TracingFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s %(threadName)s',
        rename_fields={'levelname': 'level', 'asctime': 'timestamp', 'name': 'logger_name', 'threadName': 'thread_name'}
    )

    file_handler = logging.FileHandler(os.path.join(log_dir, "todo.log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
