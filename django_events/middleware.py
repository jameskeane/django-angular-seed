import time
from django.conf import settings
from django.http import HttpResponse
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
        yield json.dumps(request.user.is_authenticated())
        yield "3"
        time.sleep(10)
        yield "4"
