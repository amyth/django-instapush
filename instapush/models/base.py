from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import HexIntegerField
from .managers import  APNSDeviceManager, GCMDeviceManager


try:
    instapush_settings = settings.INSTAPUSH_SETTINGS
except AttributeError:
    raise ImproperlyConfigured("Please include instapush settings dictionary "\
            "in your django settings")


class BaseDevice(models.Model):
    """
    Represents a base device object. This class defines
    the generic fields to be used by all device types.
    All other device types should inherit from this.
    """

    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    active = models.BooleanField(_('active'), default=True)

    ## as a device can not only be related to a user
    ## but any other defined models. we let the push
    ## user decide which model should be the owner
    ## of a device object. For cases, where a device
    ## does not have to be related to any model this
    ## can be left empty and hence blank and null are
    ## set to True
    owner = models.ForeignKey(instapush_settings.get('DEVICE_OWNER_MODEL'),
            blank=True, null=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        abstract = True


    def __unicode__(self):
        return self.name or self.device_id or self.registration_id


class GCMDevice(BaseDevice):
    """
    Represents an android device
    """

    device_id = HexIntegerField(_('Device ID'), blank=True, null=True,
            db_index=True)
    registration_id = models.TextField(_('Registration ID'))

    ## Set custom manager
    objects = GCMDeviceManager()

    class Meta:
        verbose_name = _('GCM Device')
        verbose_name_plural = _('GCM Devices')

    def send_message(self, message, **kwargs):
        """
        Sends a push notification to this device via GCM
        """

        from ..libs.gcm import gcm_send_message
        data = kwargs.pop("extra", {})
        if message is not None:
            data["message"] = message

        return gcm_send_message(registration_id=self.registration_id,
                data=data, **kwargs)


class APNSDevice(BaseDevice):
    """
    Represents an iOS device
    """

    device_id = models.UUIField(_('Device ID'), blank=True, null=True,
            db_index=True)
    registration_id = models.CharField(_('Registration ID'), max_length=64,
            unique=True)

    ## Set custom manager
    APNSDeviceManager()

    class Meta:
        verbose_name = _('APNS Device')
        verbose_name_plural = _('APNS Devices')

    def send_message(self, message, **kwargs):
        from ..libs.apns import apns_send_message
        return apns_send_message(registration_id=self.registration_id,
                alert=message, **kwargs)
