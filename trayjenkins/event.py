class IEvent(object):

    def register(self, handler):
        """
        @arg handler: Callable
        """

    def fire(self, *args, **kargs):
        """
        Calls all registered handlers with given arguments.
        """


class Event(IEvent):

    def __init__(self):
        self.handlers = set()

    def register(self, handler):
        self.handlers.add(handler)

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)
