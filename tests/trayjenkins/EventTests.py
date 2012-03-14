from unittest import TestCase

from trayjenkins.event import Event


class SingleArgumentHandler:
    def __init__(self):
        self.argument = None

    def __call__(self, argument):
        self.argument = argument


class EventTests(TestCase):

    def test_fire_SingleHandlerSingleArgument_HandlerCalledAsFunctionWithArgument(self):

        handler = SingleArgumentHandler()

        event = Event()
        event.register(handler)

        event.fire('arg 1')

        self.assertEqual('arg 1', handler.argument)

    def test_fire_SingleHandlerTwoArguments_HandlerCalledAsFunctionWithBothArguments(self):

        class Handler:
            def __init__(self):
                self.arguments = []

            def __call__(self, argumentOne, argumentTwo):
                self.arguments.append(argumentOne)
                self.arguments.append(argumentTwo)

        handler = Handler()
        event = Event()
        event.register(handler)

        event.fire('arg 1', 'arg 2')

        self.assertEqual(['arg 1', 'arg 2'], handler.arguments)

    def test_fire_TwoHandlers_BothHandlersCalledAsFunction(self):

        handlerOne = SingleArgumentHandler()
        handlerTwo = SingleArgumentHandler()

        event = Event()
        event.register(handlerOne)
        event.register(handlerTwo)

        event.fire('arg 1')

        self.assertEqual('arg 1', handlerOne.argument)
        self.assertEqual('arg 1', handlerTwo.argument)

    def test_fire_SameHandlerRegisteredTwice_HandlerOnlyCalledOnce(self):

        class CallCountHandler:
            def __init__(self):
                self.callCount = 0

            def __call__(self, argument):
                self.callCount += 1

        handler = CallCountHandler()

        event = Event()
        event.register(handler)
        event.register(handler)

        event.fire('arg 1')

        self.assertEqual(1, handler.callCount)
