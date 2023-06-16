"""Pytest configuration common to unit tests and integration tests."""
import iracing_web_api.trace as trace

# Enable logging for the requests module
trace.httpclient_logging_patch()
