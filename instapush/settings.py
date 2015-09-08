from django.conf import settings


def gcm_deactivate(rids):
    pass

INSTAPUSH_SETTINGS = getattr(settings, 'INSTAPUSH_SETTINGS', {})

## GCM Settings
GCM_SETTINGS = INSTAPUSH_SETTINGS.get('GCM_SETTINGS', {})
GCM_SETTINGS.setdefault('API_URL', 'https://android.googleapis.com/gcm/send')
GCM_SETTINGS.setdefault('MAX_RECIPIENTS', 1000)
GCM_SETTINGS.setdefault('DEACTIVATE_UNREG_CALLBACK', gcm_deactivate)


## APNS Settings
APNS_SETTINGS = INSTAPUSH_SETTINGS.get('APNS_SETTINGS', {})
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


INSTAPUSH_SETTINGS.setdefault('GCM_SETTINGS', GCM_SETTINGS)
INSTAPUSH_SETTINGS.setdefault('APNS_SETTINGS', APNS_SETTINGS)
