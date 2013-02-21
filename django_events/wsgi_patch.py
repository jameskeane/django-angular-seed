from django.core.handlers.wsgi import WSGIRequest, WSGIHandler, STATUS_CODE_TEXT
from django.core.handlers import base
from django.core import signals
from django.core.urlresolvers import set_script_prefix

from django_events.middleware import EventsMiddleware
from django_events import GEVENT_ENABLED, EVENTS_RESOURCE

class EventsWSGIHandler(WSGIHandler):
    def __init__(self, application):
        self.application = application
        super(EventsWSGIHandler, self).__init__()

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if not path.lstrip('/').startswith(EVENTS_RESOURCE) or not GEVENT_ENABLED:
            return self.application(environ, start_response)

        # We are making a data stream
        # first, grab the request object

        # Set up middleware if needed. We couldn't do this earlier, because
        # settings weren't available.
        if self._request_middleware is None:
            self.initLock.acquire()
            try:
                try:
                    # Check that middleware is still uninitialised.
                    if self._request_middleware is None:
                        self.load_middleware()
                except:
                    # Unload whatever middleware we got
                    self._request_middleware = None
                    raise
            finally:
                self.initLock.release()


        set_script_prefix(base.get_script_name(environ))
        signals.request_started.send(sender=self.__class__)
        
        # TODO: error handling, see: django.core.handlers.wsgi.WSGIHandler
        request = self.request_class(environ)
        response = None

        # Apply request middleware
        for middleware_method in self._request_middleware:
            response = middleware_method(request)
            if response:
                break

        if response is None:
            return EventsMiddleware().handle_stream(request, start_response)
        else:
            try:
                status_text = STATUS_CODE_TEXT[response.status_code]
            except KeyError:
                status_text = 'UNKNOWN STATUS CODE'
            status = '%s %s' % (response.status_code, status_text)
            response_headers = [(str(k), str(v)) for k, v in response.items()]
            for c in response.cookies.values():
                response_headers.append(('Set-Cookie', str(c.output(header=''))))
            start_response(status, response_headers)
            return response
