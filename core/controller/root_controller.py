from .controller import Controller, acquire_context
import queue

class RootController(Controller):
    def __init__(self):
        super().__init__()
        self.event_queue = queue.Queue()

    def enqueue_event(self, event, anchor):
        self.event_queue.put((event, anchor))

    def process_events(self):
        while not self.event_queue.empty():
            event, anchor = self.event_queue.get()
            with acquire_context(event.get("context", {})):
                anchor._handle_event(event)