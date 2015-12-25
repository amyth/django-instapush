"""
Defines the exception classes
"""


class PushError(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message
        return super(PushError, self).__init__(message)


class GCMPushError(PushError):
    pass


class APNSPushError(PushError):
    pass


class APNSDataOverflow(APNSPushError):
    pass


class APNSServerError(APNSPushError):
    def __init__(self, status, identifier):
        super(APNSServerError, self).__init__(status, identifier)
        self.status = status
        self.identifier = identifier
