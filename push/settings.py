from django.conf import settings


PUSH_SETTINGS = getattr(settings, 'PUSH_SETTINGS', {})

## GCM Settings
GCM_SETTINGS = PUSH_SETTINGS.get('GCM_SETTINGS', {})
GCM_SETTINGS.setdefault('API_URL', 'https://android.googleapis.com/gcm/send')
GCM_SETTINGS.setdefault('MAX_RECIPIENTS', 1000)


## APNS Settings
APNS_SETTINGS = PUSH_SETTINGS.get('APNS_SETTINGS', {})
APNS_SETTINGS.setdefault('PORT', 2195)
APNS_SETTINGS.setdefault('FEEDBACK_PORT', 2196)
APNS_SETTINGS.setdefault('ERROR_TIMEOUT', None)
APNS_SETTINGS.setdefault('MAX_SIZE', 2048)

## Add host urls based on environment
if settings.DEBUG:
    APNS_SETTINGS.setdefault('HOST', 'gateway.sandbox.push.apple.com')
    APNS_SETTINGS.setdefault('FEEDBACK_HOST', 'feedback.sandbox.push.apple.com')
else:
    APNS_SETTINGS.setdefault('HOST', 'gateway.push.apple.com')
    APNS_SETTINGS.setdefault('FEEDBACK_HOST', 'feedback.push.apple.com')


PUSH_SETTINGS.setdefault('GCM_SETTINGS', GCM_SETTINGS)
PUSH_SETTINGS.setdefault('APNS_SETTINGS', APNS_SETTINGS)
