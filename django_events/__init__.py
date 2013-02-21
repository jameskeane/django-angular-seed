from django.conf import settings
from django_events import signals

try:
    import os
    import gevent
    GEVENT_ENABLED = os.fork is gevent.fork
except Exception, e:
    GEVENT_ENABLED = False

EVENTS_RESOURCE = getattr(settings, 'EVENTS_RESOURCE', '__event_source')

def broadcast(event, payload):
    signals.broadcast.send(sender=None, event=event, payload=payload)
