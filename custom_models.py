from django.db.models.fields import (SmallIntegerField, AutoField)
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey

class TinyIntegerField(SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)

