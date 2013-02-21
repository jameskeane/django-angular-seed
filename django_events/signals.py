import django.dispatch


broadcast = django.dispatch.Signal(providing_args=["event", "payload"])
