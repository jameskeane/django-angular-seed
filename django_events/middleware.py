import time
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module
from django_events import GEVENT_ENABLED, EVENTS_RESOURCE
import json

class EventsMiddleware(object):
    def process_request(self, request):
        if request.path.lstrip('/') == EVENTS_RESOURCE and not GEVENT_ENABLED:
            self.handle_poll(request)

    def handle_poll(self, request):
        pass

    def handle_stream(self, request, start_response):
        start_response("200", [('Content-Type', 'text/event-stream')])
        engine_class = import_module( getattr(settings, 'EVENTS_ENGINE', 'django_events.backends.memory_backend')).Engine
        engine = engine_class(request.user, request.session)

        while True:
            event = engine.queue.get()

            yield 'data: %s\n\n' % event['payload']
