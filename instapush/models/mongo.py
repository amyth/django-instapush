import mongoengine

from django.conf import settings
from django.utils import timezone

from .querysets import APNSMongoQuerySet, GCMMongoQuerySet
from ..settings import INSTAPUSH_SETTINGS as instapush_settings
from ..utils import get_model


class BaseOwner(mongoengine.Document):
    pass


class BaseDevice(mongoengine.Document):
    """
    A basic device document. This class defines the generic
    fields to be used by all device models/documents. All
    other device models should inherit this base device doc.
    """

    name = mongoengine.StringField()
    active = mongoengine.BooleanField(default=True)
    owner = mongoengine.ReferenceField(get_model(instapush_settings.get(
        'DEVICE_OWNER_MODEL')), required=False)
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

    def send_message(self, data, **kwargs):
        from ..libs.gcm import gcm_send_message

        extra_data = kwargs.pop("extra", {})
        data.update(extra_data)

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
        from ..libs.apns import apns_send_message
        return apns_send_message(registration_id=self.registration_id,
                alert=message, **kwargs)
