from django.db import models


class GCMMessageMixin(object):
    def send_message(self, message, **kwargs):
        if self:
            from push.libs.gcm import gcm_send_bulk_message
            data = kwargs.pop("extra", {})
            if message is not None:
                data["message"] = message

            ids = [device.registration_id for device in self]
            return gcm_send_bulk_message(registration_ids=ids,
                    data=data, **kwargs)

class APNSMessageMixin(object):
    def send_message(self, message, **kwargs):
        from push.libs.apns import apns_send_bulk_message
        ids = [device.registration_id for device in self]

        return apns_send_bulk_message(registration_ids=ids,
                alert=message, **kwargs)


class GCMQuerySet(GCMMessageMixin, models.query.QuerySet):
    """
    Implements additional methods to be used by this queryset.
    """
    pass


class APNSQuerySet(APNSMessageMixin, models.query.QuerySet):
    """
    Implements additional methods to be used by this queryset.
    """
    pass
