from django.db import models
from .querysets import APNSQuerySet, GCMQuerySet


class GCMDeviceManager(models.Manager):
    """
    A manager to be used for GCM Devices
    """

    def get_queryset(self):
        return GCMQuerySet(self.model)


class APNSDeviceManager(models.Manager):
    """
    A manager to be used for iOS devices
    """

    def get_queryset(self):
        APNSQuerySet(self.model)
