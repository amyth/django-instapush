## Django Instapush (Push Notifications for Django)
---

This django app can be used to send [gcm](https://developers.google.com/cloud-messaging/) and [apns](https://developer.apple.com/library/ios/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/Chapters/ApplePushService.html) push notifications to mobile devices. The app implements models for sql based databases and monogoengine documents. You can specify the settings to either use a sql based model or a mongoengine model to store your device data.

## Documentation
For tutorial and documentation > [Click Here](http://www.techstricks.com/django-push-notifications-mongoengine/)

##Models
---
**SQL Models**

There are 3 sql models to store the device information `BaseDevice`, `GCMDevice` and `APNSDevice`. Both GCMDevice and APNSDevice extends from the BaseDevice model. You can either use these models to store your device information or can create a custom model extending from the BaseDevice model.

#### Using builtin GCM model
---
```
from instapush.models.base import BaseDevice, GCMDevice, APNSDevice

device_id = preferences.get_unique_id()
reg_id = preferences.get_registration_id()
user = preferences.get_user()

device = GCMDevice.objects.create(registration_id=reg_id, device_id=device_id, owner=user)
```

#### Using builtin APNS model
---
```
from instapush.models.base import BaseDevice, GCMDevice, APNSDevice

device_id = preferences.get_unique_id()
reg_id = preferences.get_registration_id()
user = preferences.get_user()

device = APNSDevice.objects.create(registration_id=reg_id, device_id=device_id, owner=user)
```

#### Using a custom model
---
```
from instapush.models.base import BaseDevice, GCMDevice, APNSDevice

device_id = preferences.get_unique_id()
reg_id = preferences.get_registration_id()
company = preferences.get_company()

#custom/models.py
class CompanyGCMDevice(BaseDevice):
    regid = models.CharField(max_length=255)
    custom_device_attribute = models.CharField(255)

device = CompanyGCMDevice.objects.create(registration_id=reg_id, device_id=device_id, owner=company)
```

**Mongoengine Models**

This app also support mongoengine Documents as django models. It implements the similar 3 models that can be used to send push notifications, in case your project uses mongoengine to define the models. The models would work the same as shown above in the sql models section. The only change is that you'd need to import it from the `mondels.mongo` module instead of `models.base`

```
from instapush.models.mongo import BaseDevice, GCMDevice, APNSDevice
```

##Push Notifications
---

Instapush django push notifications support both GCM and APNS. The device object saved in the models have a method `send_message` attribute to send the push notifications.

#### Sending Exclusive GCM/APNS push notification to a device
---

To send an exclusive method to a particular device you'll need to fetch the device that you'd want to send a push notification to and call the send_message on the device object to exclusively send a notification to that device.

```
from instapush.models.mongo import APNSDevice, GCMDevice

device = GCMDevice.objects.get(owner=request.user)
device.send_message({"type": "notify", "message": "You've a new notification"})


device = APNSDevice.objects.get(owner=request.user)
device.send_message({"type": "notify", "message": "You've a new notification"})
```

#### Sending bulk GCM/APNS push notification to multiple devices
---

Instapush allows you to send bulk gcm and apns push notifications to multiple devices at a time. It implements 2 methods `gcm_send_bulk_message` and `apns_send_bulk_message` to send notification to android and ios devices respectively. Both these methods accept 2 arguments:

1. List of device registration ids to send messages to
2. The message data


```
from apps.communication.instapush.libs import apns, gcm
from apps.communication.instapush.models.mongo import APNSDevice, GCMDevice

gcm_devices = GCMDevice.objects.filter(owner__in=[user1, user2, user3])
apns_devices = APNSDevice.objects.filter(owner__in=[user4, user5, user6])

gcm_registration_ids = [device.registration_id for device in gcm_devices]
apns_registration_ids = [device.registration_id for device in apns_devices]

## Send bulk GCM notifications
gcm.gcm_send_bulk_message(registration_ids, {"type": "3", "message": "You have a notification"})

## Send bulk APNS notifications
apns.apns_send_bulk_message(registration_ids, {"type": "3", "message": "You have a notification"})
```

##Settings
---

Instapush settings should be a `dictionary` object named `INSTAPUSH_SETTINGS` defined in your django settings. The generic settings to be used for both gcm and apns notifications are directly a key:value pair within the `INSTAPUSH_SETTINGS`. For settings specific to `gcm` and `apns` the key:value pair should be defined under `GCM_SETTINGS` and `APNS_SETTINGS` keys as a dictionary object which are defined under `INSTAPUSH_SETTINGS`.

**Generic Settings**

Name|Required|Default Value
:--|:--|:--
DEVICE_OWNER_MODEL|yes|-

**GCM Settings**

Name|Required|Default Value
:--|:--|:--
API_KEY|yes|-
API_URL|no|https://android.googleapis.com/gcm/send
DEACTIVATE_UNREG_CALLBACK|yes|-
MAX_RECIPIENTS|no|1000

**APNS Settings**

Name|Required|Default Value
:--|:--|:--
APNS_CERTIFICATE|yes|-
HOST|no|gateway.sandbox.push.apple.com
PORT|no|2195
MAX_SIZE|no|2048
FEEDBACK_HOST|no|feedback.sandbox.push.apple.com'
FEEDBACK_PORT|no|2196
ERROR_TIMEOUT|no|None

**Exampe Settings Dict**

```
INSTAPUSH_SETTINGS = {
    'DEVICE_OWNER_MODEL': 'accounts.models.UserAccount',
    'GCM_SETTINGS': {
        'API_KEY': 'my gcm api key'
    },
    'APNS_SETTINGS': {
        'APNS_CERTIFICATE': os.path.join(PROJECT_ROOT, 'keys/apns_sandbox.pem')
    }
} 
```

## Contact & Social
---

If you face any issues or have any queries regarding using this app, you can either open an issue here or contact me directly on any of the following:

| ![Twitter](https://cdn1.iconfinder.com/data/icons/logotypes/32/twitter-16.png)  [@mytharora](https://twitter.com/mytharora) |
![Google+](https://cdn1.iconfinder.com/data/icons/logotypes/32/circle-google-plus-16.png)  [Amyth+](https://plus.google.com/+AmythArora/posts) | ![Instagram](https://cdn1.iconfinder.com/data/icons/logotypes/32/instagram-16.png)  [therealamyth](https://instagram.com/therealamyth/) | ![Website](https://cdn1.iconfinder.com/data/icons/logotypes/32/chrome-16.png) [www.techstricks.com](http://www.techstricks.com) |
