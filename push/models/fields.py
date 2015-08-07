"""
Code by jleclanche @ https://github.com/jleclanche/django-push-notifications/blob/master/push_notifications/fields.py
"""

import re
import struct
from django import forms
from django.core.validators import RegexValidator
from django.db import models, connection
from django.utils import six
from django.utils.translation import ugettext_lazy as _


__all__ = ["HexadecimalField", "HexIntegerField"]


hex_re = re.compile(r"^(([0-9A-f])|(0x[0-9A-f]))+$")
postgres_engines = [
    "django.db.backends.postgresql_psycopg2",
    "django.contrib.gis.db.backends.postgis",
]


class HexadecimalField(forms.CharField):
    """
    A form field that accepts only hexadecimal numbers
    """
    def __init__(self, *args, **kwargs):
        self.default_validators = [RegexValidator(hex_re, _("Enter a valid hexadecimal number"), "invalid")]
        super(HexadecimalField, self).__init__(*args, **kwargs)

    def prepare_value(self, value):
        # converts bigint from db to hex before it is displayed in admin
        if value and not isinstance(value, six.string_types) \
            and connection.vendor in ("mysql", "sqlite"):
            value = hex(value).rstrip("L")
        return super(forms.CharField, self).prepare_value(value)


class HexIntegerField(six.with_metaclass(models.SubfieldBase, models.BigIntegerField)):
    """
    This field stores a hexadecimal *string* of up to 64 bits as an unsigned integer
    on *all* backends including postgres.

    Reasoning: Postgres only supports signed bigints. Since we don't care about
    signedness, we store it as signed, and cast it to unsigned when we deal with
    the actual value (with struct)

    On sqlite and mysql, native unsigned bigint types are used. In all cases, the
    value we deal with in python is always in hex.
    """
    def db_type(self, connection):
        engine = connection.settings_dict["ENGINE"]
        if "mysql" in engine:
            return "bigint unsigned"
        elif "sqlite" in engine:
            return "UNSIGNED BIG INT"
        else:
            return super(HexIntegerField, self).db_type(connection=connection)

    def get_prep_value(self, value):
        if value is None or value == "":
            return None
        if isinstance(value, six.string_types):
            value = int(value, 16)
        # on postgres only, interpret as signed
        if connection.settings_dict["ENGINE"] in postgres_engines:
            value = struct.unpack("q", struct.pack("Q", value))[0]
        return value

    def to_python(self, value):
        if isinstance(value, six.string_types):
            return value
        if value is None:
            return ""
        # on postgres only, re-interpret from signed to unsigned
        if connection.settings_dict["ENGINE"] in postgres_engines:
            value = hex(struct.unpack("Q", struct.pack("q", value))[0])
        return value

    def formfield(self, **kwargs):
        defaults = {"form_class": HexadecimalField}
        defaults.update(kwargs)
        # yes, that super call is right
        return super(models.IntegerField, self).formfield(**defaults)

    def run_validators(self, value):
        # make sure validation is performed on integer value not string value
        return super(models.BigIntegerField, self).run_validators(self.get_prep_value(value))
