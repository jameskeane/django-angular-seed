from django.core.handlers.wsgi import WSGIRequest, WSGIHandler
from django_events.middleware import EventsMiddleware
from django_events import GEVENT_ENABLED, EVENTS_RESOURCE

class EventsWSGIHandler(WSGIHandler):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if not path.lstrip('/').startswith(EVENTS_RESOURCE) or not GEVENT_ENABLED:
            return self.application(environ, start_response)

        # We are making a data stream
        # first, grab the request object
        request = WSGIRequest(environ)
        return EventsMiddleware().handle_stream(request, start_response)
