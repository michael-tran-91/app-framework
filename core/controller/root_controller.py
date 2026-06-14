from .controller import Controller, acquire_context
import queue

class RootController(Controller):
    def __init__(self):
        super().__init__()
        self.event_queue = queue.Queue()
        self.event_paths = {}

#---------------------------------------------------------------------------
# public method | event dispatch
#---------------------------------------------------------------------------

    def _register_event_path(self, event_type, controllers):
        self.event_paths[event_type] = self.event_paths.get(event_type, set())
        self.event_paths[event_type].update(controllers)
        

    def enqueue_event(self, event, anchor):
        self.event_queue.put((event, anchor))

    def process_events(self):
        to_process = self.event_queue.qsize()
        for _ in range(to_process):
            event, anchor = self.event_queue.get()
            with acquire_context(event.get("context", {})):
                controllers = self.event_paths.get(event.get("type", ""), None)
                if controllers is not None:
                    if id(anchor) in controllers:
                        anchor._dispatch_event(event, controllers)