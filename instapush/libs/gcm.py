"""
A stand-alone library to send GCM push notifications
"""

import json

## import urllib methods
try:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import Request, urlopen
    from urllib import urlencode

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

from ..exceptions import GCMPushError
from ..settings import INSTAPUSH_SETTINGS as settings


class GCMMessenger(object):

    def __init__(self, registration_id, data, encoding='utf-8', **kwargs):

        self._registration_id = registration_id
        self._data = data
        self._kwargs = kwargs
        self.encoding = encoding

        ## Check for required settings
        self._prepare_settings()

    def _chunks(self):
        for item in range(0, len(self.registration_id), self.max_recipients):
            yield self.registration_id[item:item+self.max_recipients]

    def _prepare_settings(self):

        cons = ['API_KEY',]
        gcm_settings = settings.get('GCM_SETTINGS')

        for x in cons:
            item = gcm_settings.get(x)
            if not item:
                raise ImproperlyConfigured("Please add %s to your "\
                        "GCM_SETTINGS to send notifications through gcm" % x)

        for x in gcm_settings:
            setattr(self, x.lower(), gcm_settings[x])

    def send_plain(self):
        """
        Sends a text/plain GCM message
        """

        values = {"registration_id": self._registration_id}

        for key, val in self._data.items():
            values["data.%s" % (key)] = val.encode(self.encoding)

        for key, val in self._kwargs.items():
            if val and isinstance(val, bool):
                val = 1
                values[key] = val

        data = urlencode(sorted(values.items())).encode(self.encoding)
        result = self._send(data, "application/x-www-form-urlencoded;charset=UTF-8")

        if result.startswith("Error="):
            if result in ("Error=NotRegistered", "Error=InvalidRegistration"):
                ## TODO: deactivate the unregistered device
                return result

            raise GCMPushError(result)

        return result

    def send_json(self, ids=None):
        """
        Sends a json GCM message
        """

        items = ids or self._registration_id
        values = {"registration_ids": items}

        if self._data is not None:
            values["data"] = self._data

        for key, val in self._kwargs.items():
            if val:
                values[key] = val

        data = json.dumps(values, separators=(",", ":"), sort_keys=True).encode(
                self.encoding)

        result = json.loads(self._send(data, "application/json"))

        if ("failure" in result) and (result["failure"]):
            unregistered = []
            throw_error = False

            for index, error in enumerate(result.get("results", [])):
                error = error.get("error", "")
                if error in ("NotRegistered", "InvalidRegistration"):
                    unregistered.append(items[index])
                elif error != "":
                    throw_error = True

            self.deactivate_unregistered_devices(unregistered)
            if throw_error:
                raise GCMPushError(result)

        return result

    def send_bulk(self):
        if len(self._registration_id) > self.max_recipients:
            result = []
            for chunk in self._chunks():
                result.append(self.send_json(ids=chunk))

            return result
        return self.send_json()

    def deactivate_unregistered_devices(self, rids):
        deactivate_callback = getattr(settings, 'DEACTIVATE_UNREG_CALLBACK')
        deactivate_callback(rids)


    def _send(self, data, content_type):
        """
        Sends a GCM message with the given content type
        """

        headers = {
            "Content-Type": content_type,
            "Authorization": "key=%s" % (self.api_key),
            "Content-Length": str(len(data))
        }

        request = Request(self.api_url, data, headers)
        return urlopen(request).read().decode(self.encoding)


def gcm_send_message(registration_id, data, encoding='utf-8', **kwargs):
    """
    Standalone method to send a single gcm notification
    """

    messenger = GCMMessenger(registration_id, data, encoding=encoding, **kwargs)
    return messenger.send_plain()


def gcm_send_bulk_message(registration_ids, data, encoding='utf-8', **kwargs):
    """
    Standalone method to send bulk gcm notifications
    """

    messenger = GCMMessenger(registration_ids, data, encoding=encoding, **kwargs)
    return messenger.send_bulk()
