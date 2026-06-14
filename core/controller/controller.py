import threading, copy

thread_event = threading.local()
thread_event.context = {
    "controllers" : set()
}

def acquire_context(ctx):
    old_ctx = thread_event.context
    thread_event.context = ctx
    yield
    thread_event.context = old_ctx

class Event:
    def __init__(self, event_type: str, data: dict|None = None):
        self._event_type = event_type
        self._data = data
        self._propagation = True
        self._context = {
            "controller" : set()    
        }

    @property
    def event_type(self):
        return self._event_type
    
    @property
    def data(self):
        return self._data
    
    @property
    def context(self):
        return self._context

    def is_continue_propagation(self):
        return self._propagation
    
    def stop_propagation(self):
        self._propagation = False


class Controller():
    def __init__(self):
        super().__init__()
        self.childrens = []
        self.parent = None
        self.event_handlers = {}

#---------------------------------------------------------------------------
# property
#---------------------------------------------------------------------------
    @property
    def root(self):
        ctrl = self
        while ctrl.parent:
            ctrl = ctrl.parent
        return ctrl
    
#---------------------------------------------------------------------------
# private method | tree structure
#---------------------------------------------------------------------------
    def _on_attached(self):
        pass

#---------------------------------------------------------------------------
# public method | tree structure
#---------------------------------------------------------------------------
    def add_child(self, child : Controller):
        self.childrens.append(child)
        child.parent = self
        child._on_attached()
        return child

    def remove_child(self, child : Controller):
        if child in self.childrens:
            child.on_shutdown()
            child.remove_childrens()
            child.parent = None
            self.childrens.remove(child)            

    def remove_childrens(self):
        while self.childrens:
            self.remove_child(self.childrens[0])

    def remove_self(self):
        if self.parent:
            self.parent.remove_child(self)

#---------------------------------------------------------------------------
# public method | context manager
#---------------------------------------------------------------------------
    def union_context(self, extra = None):
        new_ctx = copy.deepcopy(thread_event.context)
        new_ctx["controller"] = new_ctx.get("controller", set())
        new_ctx["controller"].add(id(self))
        if extra:
            new_ctx.update(extra)

        old_ctx = thread_event.context
        thread_event.context = new_ctx
        yield
        thread_event.context = old_ctx

    def new_context(self, extra = None):
        old_ctx = thread_event.context
        thread_event.context = {
            "controller": set([id(self)])
        }
        if extra:
            thread_event.context.update(extra)
        yield
        thread_event.context = old_ctx

#---------------------------------------------------------------------------
# public method | event handlers
#---------------------------------------------------------------------------
    def register_event_handler(self, event_type, handler : callable, required_controllers = None):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

        rqids = set()
        if required_controllers is not None:
            for _i in required_controllers:
                if isinstance(_i, Controller):
                    rqids.add(id(_i))
                elif isinstance(_i, int):
                    rqids.add(_i)

        self.event_handlers[event_type].append((handler, rqids))

        controllers = set()
        ctrl = self
        while ctrl:
            controllers.add(id(ctrl))
            ctrl = ctrl.parent

        root = self.root
        if hasattr(root, "_register_event_path"):
            root._register_event_path(event_type, controllers)

#---------------------------------------------------------------------------
# public method | event dispatch
#---------------------------------------------------------------------------
    def bubble_event(self, event: Event, reuse_context = False):
        self._prepare_event_context(event, reuse_context)

        ctrl = self
        while ctrl:
            if ctrl._handle_event(event):
                return
            ctrl = ctrl.parent

    def post_event(self, event: Event, reuse_context = False):
        self._prepare_event_context(event, reuse_context)

        root = self.root
        if hasattr(root, "enqueue_event"):
            root.enqueue_event(event, self)

    def dispatch_event(self, event: Event, reuse_context = False):
        self._prepare_event_context(event, reuse_context)
        self._dispatch_event(event, None)

#---------------------------------------------------------------------------
# private method | event dispatch
#---------------------------------------------------------------------------
    def _dispatch_event(self, event: Event, controllers):
        if self._handle_event(event):
            return True
        
        for child in self.childrens:
            if controllers is not None and id(child) not in controllers:
                continue

            if child._dispatch_event(event, controllers):
                return True

        return False

    def _handle_event(self, event: Event):
        if not self._in_event_context(event):
            return False
        ctrl_ids = event.context["controller"]

        handlers = self.event_handlers.get(event.event_type, [])
        for handler, required_ids in handlers:
            if ctrl_ids.issuperset(required_ids):
                if handler(event):
                    return True
        return False
    
#---------------------------------------------------------------------------
# private method | paticipate int event context
#---------------------------------------------------------------------------
    def _in_event_context(self, event: Event):
        ctrl_ids = event.context["controller"]
        return id(self) in ctrl_ids
    
    def _prepare_event_context(self, event: Event, reuse_context = False):
        if reuse_context:
            event.context.update(thread_event.context)

        ctrl = self
        while ctrl:
            event.context["controller"].add(id(ctrl))
            ctrl = ctrl.parent

#---------------------------------------------------------------------------
# private method
#---------------------------------------------------------------------------
    def _on_shutdown(self):
        pass
    