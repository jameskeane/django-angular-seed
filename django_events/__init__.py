from django.conf import settings

try:
    import os
    import gevent
    GEVENT_ENABLED = os.fork is gevent.fork
except Exception, e:
    GEVENT_ENABLED = False

EVENTS_RESOURCE = getattr(settings, 'EVENTS_RESOURCE', '__event_source')
