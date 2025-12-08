class AppException(Exception):

    def __init__(self, message: str = "An application error occurred"):
        self.message = message
        super().__init__(self.message)