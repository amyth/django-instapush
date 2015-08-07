"""
Defines the exception classes
"""


class PushError(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message
        return super(GCMPushError, self).__init__(message)


class GCMPushError(PushError):
    pass


class APNSPushError(PushError):
    pass
