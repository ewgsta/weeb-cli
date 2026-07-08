"""OpenTelemetry integration for Weeb CLI.

Provides distributed tracing, metrics, and log correlation.
Zero overhead when disabled or when telemetry packages are not installed.

Configuration is set in code - no environment variables needed:
    - Telemetry is ON by default (opt-out)
    - Disable via: config.set("telemetry_enabled", False)
    - Or via CLI settings menu
    
Advanced users can override with OTEL_SDK_DISABLED="true" to force disable.
"""

import os
import threading
from functools import wraps
from typing import Any, Optional

_initialized = False
_init_lock = threading.Lock()

OTEL_PROXY_ENDPOINT = "https://weeb-otel-proxy.ewgsta.workers.dev"
OTEL_PROTOCOL = "http/protobuf"
SERVICE_NAME = "weeb-cli"
CONSOLE_DEBUG = False

def is_enabled() -> bool:
    """Check if telemetry is enabled.
    
    Priority order:
    1. OTEL_SDK_DISABLED env var (force disable)
    2. User config: telemetry_enabled setting
    """
    # Force disable override
    if os.environ.get("OTEL_SDK_DISABLED", "").lower() == "true":
        return False

    # Check user config
    try:
        from weeb_cli.config import config
        return bool(config.get("telemetry_enabled", False))
    except Exception:
        return False


def init_telemetry(environment: str = "production") -> None:
    global _initialized
    with _init_lock:
        if _initialized:
            return

        _initialized = True

        if not is_enabled():
            return

        try:
            _setup_providers(environment)
        except ImportError:
            pass
        except Exception:
            pass


def _setup_providers(environment: str) -> None:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource

    try:
        from weeb_cli import __version__
    except ImportError:
        __version__ = "unknown"

    import socket

    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "service.version": __version__,
        "deployment.environment": environment,
        "service.instance.id": f"{socket.gethostname()}-{os.getpid()}",
    })

    # Configure endpoint and protocol
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = OTEL_PROXY_ENDPOINT
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = OTEL_PROTOCOL

    span_exporter = _create_span_exporter()
    metric_exporter = _create_metric_exporter()

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    reader = PeriodicExportingMetricReader(
        metric_exporter,
        export_interval_millis=30000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    _setup_log_bridge(resource)
    _install_auto_instrumentors()

    import atexit
    atexit.register(shutdown_telemetry)


def _create_span_exporter():
    """Create span exporter based on configuration."""
    if CONSOLE_DEBUG:
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter
        return ConsoleSpanExporter()

    # Use configured protocol (http/protobuf for Cloudflare Worker)
    if OTEL_PROTOCOL == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    else:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    return OTLPSpanExporter()


def _create_metric_exporter():
    """Create metric exporter based on configuration."""
    if CONSOLE_DEBUG:
        from opentelemetry.sdk.metrics.export import ConsoleMetricExporter
        return ConsoleMetricExporter()

    # Use configured protocol (http/protobuf for Cloudflare Worker)
    if OTEL_PROTOCOL == "grpc":
        from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    else:
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    return OTLPMetricExporter()


def _setup_log_bridge(resource) -> None:
    """Setup log bridge for log correlation."""
def _setup_log_bridge(resource) -> None:
    """Setup log bridge for log correlation."""
    try:
        from opentelemetry.sdk._logs import LoggerProvider
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
        from opentelemetry._logs import set_logger_provider

        if CONSOLE_DEBUG:
            from opentelemetry.sdk._logs.export import ConsoleLogExporter
            log_exporter = ConsoleLogExporter()
        else:
            # Use configured protocol
            if OTEL_PROTOCOL == "grpc":
                from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
            else:
                from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            log_exporter = OTLPLogExporter()

        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        set_logger_provider(logger_provider)
    except ImportError:
        pass


def _install_auto_instrumentors() -> None:
    """Install automatic instrumentation for common libraries."""
    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        RequestsInstrumentor().instrument()
    except (ImportError, Exception):
        pass

    try:
        from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
        URLLib3Instrumentor().instrument()
    except (ImportError, Exception):
        pass

    try:
        from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
        SQLite3Instrumentor().instrument()
    except (ImportError, Exception):
        pass
def shutdown_telemetry() -> None:
    try:
        from opentelemetry import trace
        provider = trace.get_tracer_provider()
        if hasattr(provider, "shutdown"):
            provider.shutdown()
    except Exception:
        pass

    try:
        from opentelemetry import metrics
        provider = metrics.get_meter_provider()
        if hasattr(provider, "shutdown"):
            provider.shutdown()
    except Exception:
        pass

    try:
        from opentelemetry._logs import get_logger_provider
        provider = get_logger_provider()
        if hasattr(provider, "shutdown"):
            provider.shutdown()
    except Exception:
        pass


def get_tracer(name: str = "weeb-cli"):
    try:
        from opentelemetry import trace
        try:
            from weeb_cli import __version__
        except ImportError:
            __version__ = "unknown"
        return trace.get_tracer(name, __version__)
    except ImportError:
        return _NoOpTracer()


def get_meter(name: str = "weeb-cli"):
    try:
        from opentelemetry import metrics
        try:
            from weeb_cli import __version__
        except ImportError:
            __version__ = "unknown"
        return metrics.get_meter(name, __version__)
    except ImportError:
        return _NoOpMeter()


def record_exception(span: Any, exception: Exception) -> None:
    try:
        from opentelemetry.trace import StatusCode
    except ImportError:
        return

    if not hasattr(span, "is_recording") or not span.is_recording():
        return

    attrs = {"exception.type": type(exception).__name__}
    try:
        from weeb_cli.exceptions import WeebCLIError
        if isinstance(exception, WeebCLIError):
            if exception.code:
                attrs["weeb.error.code"] = exception.code
            if exception.message:
                attrs["weeb.error.message"] = exception.message
    except ImportError:
        pass

    span.set_status(StatusCode.ERROR, str(exception))
    span.record_exception(exception, attributes=attrs)


def traced(name: Optional[str] = None, attributes: Optional[dict] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            span_name = name or f"{func.__module__}.{func.__qualname__}"
            with tracer.start_as_current_span(span_name, attributes=attributes) as span:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    record_exception(span, e)
                    raise
        return wrapper
    return decorator


def instrument_flask_app(app: Any) -> None:
    if not _initialized or not is_enabled():
        return
    try:
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        FlaskInstrumentor().instrument_app(app)
    except (ImportError, Exception):
        pass


def instrument_curl_session(session: Any) -> Any:
    if not _initialized or not is_enabled():
        return session
    try:
        from opentelemetry import trace
    except ImportError:
        return session

    tracer = get_tracer()
    original_get = session.get
    original_post = session.post

    @wraps(original_get)
    def traced_get(url, *args, **kwargs):
        with tracer.start_as_current_span("HTTP GET", attributes={
            "http.method": "GET",
            "http.url": str(url)[:256],
        }) as span:
            resp = original_get(url, *args, **kwargs)
            if hasattr(resp, "status_code"):
                span.set_attribute("http.status_code", resp.status_code)
            return resp

    @wraps(original_post)
    def traced_post(url, *args, **kwargs):
        with tracer.start_as_current_span("HTTP POST", attributes={
            "http.method": "POST",
            "http.url": str(url)[:256],
        }) as span:
            resp = original_post(url, *args, **kwargs)
            if hasattr(resp, "status_code"):
                span.set_attribute("http.status_code", resp.status_code)
            return resp

    session.get = traced_get
    session.post = traced_post
    return session


# -- Metrics holder --

class _MetricsHolder:
    __slots__ = (
        "http_request_duration", "cache_operations", "download_duration",
        "download_status", "provider_requests",
    )

    def __init__(self, meter):
        self.http_request_duration = meter.create_histogram(
            "weeb.http.request.duration",
            unit="ms",
            description="HTTP request duration",
        )
        self.cache_operations = meter.create_counter(
            "weeb.cache.operations",
            description="Cache operations count",
        )
        self.download_duration = meter.create_histogram(
            "weeb.download.duration",
            unit="s",
            description="Download duration",
        )
        self.download_status = meter.create_counter(
            "weeb.download.status",
            description="Download completion status counts",
        )
        self.provider_requests = meter.create_counter(
            "weeb.provider.requests",
            description="Provider request counts",
        )


_metrics: Optional[_MetricsHolder] = None
_metrics_lock = threading.Lock()


def get_metrics() -> _MetricsHolder:
    global _metrics
    if _metrics is None:
        with _metrics_lock:
            if _metrics is None:
                _metrics = _MetricsHolder(get_meter())
    return _metrics


# -- No-op fallbacks when opentelemetry-api is not installed --

class _NoOpSpan:
    def is_recording(self):
        return False

    def set_attribute(self, key, value):
        pass

    def set_status(self, *args, **kwargs):
        pass

    def record_exception(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class _NoOpTracer:
    def start_as_current_span(self, name, **kwargs):
        return _NoOpSpan()

    def start_span(self, name, **kwargs):
        return _NoOpSpan()


class _NoOpInstrument:
    def add(self, amount, attributes=None):
        pass

    def record(self, amount, attributes=None):
        pass


class _NoOpMeter:
    def create_counter(self, name, **kwargs):
        return _NoOpInstrument()

    def create_histogram(self, name, **kwargs):
        return _NoOpInstrument()

    def create_up_down_counter(self, name, **kwargs):
        return _NoOpInstrument()
