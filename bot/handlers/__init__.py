# Import all handler modules so their @app.on_* decorators register with the client.
from handlers import start, help, protect, callbacks, messages, group, ping  # noqa: F401
