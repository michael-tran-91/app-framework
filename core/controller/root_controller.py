from .controller import Controller, acquire_context
import queue

class RootController(Controller):
    def __init__(self):
        super().__init__()
        self.event_queue = queue.Queue()

#---------------------------------------------------------------------------
# public method | event dispatch
#---------------------------------------------------------------------------

    def enqueue_event(self, event, anchor):
        self.event_queue.put((event, anchor))

    def process_events(self):
        to_process = self.event_queue.qsize()
        for _ in range(to_process):
            event, anchor = self.event_queue.get()
            with acquire_context(event.get("context", {})):
                anchor.dispatch_event(event)