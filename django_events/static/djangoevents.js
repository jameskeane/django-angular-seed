$(function() {
    if (!window.EventSource) {
      // patch event source
    }

    var es = new EventSource('/__event_source?' + Math.random().toString(34).substring(2));

    es.addEventListener('message', function(e) {
        console.log(e.data);
    }, false);

    es.addEventListener('open', function(e) {
      // Connection was opened.
      console.log('opened');
    }, false);

    es.addEventListener('error', function(e) {
        console.log(e);
      if (e.eventPhase == EventSource.CLOSED) {
        // Connection was closed.
      }
    }, false);
});
