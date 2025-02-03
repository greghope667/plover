import objc
UNUserNotificationCenter = objc.lookUpClass('UNUserNotificationCenter')
UNMutableNotificationContent = objc.lookUpClass('UNMutableNotificationContent')
UNNotificationRequest = objc.lookUpClass('UNNotificationRequest')

NSObject = objc.lookUpClass('NSObject')

from plover import log, __name__ as __software_name__
import logging


class NotificationHandler(logging.Handler):
    """ Handler using OS X Notification Center to show messages. """

    def __init__(self):
        super().__init__()
        self.setLevel(log.WARNING)
        self.setFormatter(log.NoExceptionTracebackFormatter('%(message)s'))

    def emit(self, record):
        content = UNMutableNotificationContent.alloc().init()
        content.setTitle_(record.levelname.title())
        content.setBody_(self.format(record))

        request = UNNotificationRequest.requestWithIdentifier_content_trigger_("notification", content, None)

        center = UNUserNotificationCenter.currentNotificationCenter()
        center.requestAuthorizationWithOptions_completionHandler_(3, lambda granted, error: None)
        center.addNotificationRequest_withCompletionHandler_(request, None)


class AlwaysPresentNSDelegator(NSObject):
    """
    Custom delegator to force presenting even if Plover is in the foreground.
    """
    def userNotificationCenter_didActivateNotification_(self, ns, note):
        # Do nothing
        return

    def userNotificationCenter_shouldPresentNotification_(self, ns, note):
        # Force notification, even if frontmost application.
        return True

always_present_delegator = AlwaysPresentNSDelegator.alloc().init()
