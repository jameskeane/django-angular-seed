from django_events import signals
from gevent.event import Event
from gevent.queue import Queue

class Engine(object):

    def __init__(self, user, session):
        self.user = user
        self.queue = Queue()

        if user.is_authenticated():
            self._register_user()

        # register the broadcast message
        signals.broadcast.connect(self.on_broadcast)

    def on_broadcast(self, sender, **kwargs):
        self.queue.put_nowait(kwargs)

    def _register_user(self):
        pass