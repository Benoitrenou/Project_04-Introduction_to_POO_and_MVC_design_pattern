class ExceptionsView:
    """Views of customed errors."""

    def __init__(self, message):
        print(message)


class CustomTypeError(TypeError, BaseException):
    """Handle TypeError of application."""

    def __init__(self, message):
        self.view = ExceptionsView(message)


class CustomValueError(ValueError, BaseException):
    """Handle ValueError of application."""

    def __init__(self, message):
        self.view = ExceptionsView(message)


class CustomAssertionError(AssertionError, BaseException):
    """Handle AssertionError of application."""

    def __init__(self, message):
        self.view = ExceptionsView(message)
