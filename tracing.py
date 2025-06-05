import os
from opentelemetry import trace
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from socket import gethostname


def init_tracing():
    provider = TracerProvider(resource=Resource({
      ResourceAttributes.SERVICE_NAME: os.environ['OTEL_SERVICE_NAME'],
      ResourceAttributes.HOST_NAME: gethostname() or 'UNSET',
   }))
    if os.getenv('OTEL_LOG_LEVEL', '') == 'debug':
        processor = SimpleSpanProcessor(ConsoleSpanExporter())
    else:
        processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
