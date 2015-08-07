import mongoengine

from django.conf import settings
from django.utils import timezone

from .querysets import APNSMongoQuerySet, GCMMongoQuerySet


instapush_settings = settings.get('INSTAPUSH_SETTINGS')


class BaseDevice(mongoengine.Document):
    """
    A basic device document. This class defines the generic
    fields to be used by all device models/documents. All
    other device models should inherit this base device doc.
    """

    name = mongoengine.StringField()
    active = mongoengine.BooleanField(default=True)
    user = mongoengine.ReferenceField(instapush_settings.get(
        'DEVICE_OWNER_MODEL'), required=False)
    date_created = mongoengine.DateTimeField(default=timezone.now())

    meta = {'collection': 'devices', 'allow_inheritance': True}


class GCMDevice(BaseDevice):
    """
    This document represents a device that is uses google cloud
    messaging service aka GCM. In simple words this document
    represents an android device.
    """

    device_id = mongoengine.StringField()
    registration_id = mongoengine.StringField()

    meta = {
        'queryset_class': GCMMongoQuerySet,
        'indexes': [{'fields': ['device_id'], 'unique': True, 'sparse': True}]
    }

    def send_message(self, message, **kwargs):
        from instapush.lib.gcm import gcm_send_message
        data = kwargs.pop("extra", {})
        if message is not None:
            data['message'] = message

        return gcm_send_message(registration_id=self.registration_id,
                data=data, **kwargs)


class APNSDevice(BaseDevice):
    """
    This document represents an iOS device that uses APNS
    to send push notifications.
    """

    device_id = mongoengine.StringField()
    registration_id = mongoengine.StringField()

    meta = {
        'queryset_class': APNSMongoQuerySet,
        'indexes': [{'fields': ['device_id'], 'unique': True, 'sparse': True}]
    }

    def send_message(self, message, **kwargs):
        #TODO: uncomment the following once APNS is implemented
        #from instapush.libs.apns import apns_send_message
        #return apns_send_message(registration_id-self.registration_id,
        #        alert=message, **kwargs)
        pass
