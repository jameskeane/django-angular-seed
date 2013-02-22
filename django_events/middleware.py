import time
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module
from django_events import GEVENT_ENABLED, EVENTS_RESOURCE
import json
from exceptions import GeneratorExit
from gevent.queue import Empty


class EventsMiddleware(object):
    def process_request(self, request):
        if request.path.lstrip('/') == EVENTS_RESOURCE and not GEVENT_ENABLED:
            self.handle_poll(request)

    def handle_poll(self, request):
        pass

    def handle_stream(self, request, start_response, socket):
        start_response("200 OK", [('Content-Type', 'text/event-stream'), ('Cache-Control', 'no-cache')])
        engine_class = import_module(getattr(settings, 'EVENTS_ENGINE', 'django_events.backends.memory_backend')).Engine
        engine = engine_class(request.user, request.session)
        yield ':stay cool\n\n'

        while True:
            try:
                event = engine.queue.get(timeout=10)
                yield 'event: %s\ndata: %s\n\n' % (event['event'], json.dumps(event['payload']))
            except GeneratorExit:
                break
            except Empty:
                yield ':stay cool\n\n'  # Send a keep alive every ten seconds
