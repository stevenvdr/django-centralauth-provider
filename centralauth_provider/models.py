from datetime import datetime, timedelta
import random

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from centralauth_provider import *

class Session(models.Model):
    user = models.ForeignKey(User, related_name="sessions")
    key = models.CharField(default=lambda: Session.generate_unique_key(), unique = True, max_length = 20)
    expire_date = models.DateTimeField(default = lambda: datetime.now()+timedelta(days=CENTRALAUTH_COOKIE_DAYS_ALIVE))

    def keep_alive(self):
        self.expire_date = datetime.now() + timedelta(days=CENTRALAUTH_COOKIE_DAYS_ALIVE)
        self.save()

    @staticmethod
    def generate_random_key(length = 20):
        key = ""
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for x in range(length):
            key += random.choice(allowed_chars)
        return key

    @staticmethod
    def generate_unique_key():
        key = Session.generate_random_key()
        while Session.objects.filter(key = key).count() > 0:
            key = Session.generate_random_key()
        return key

    @staticmethod
    def invalidate_session(session_key = None):
        if session_key is None:
            pass
        else:
            try:
                session = Session.objects.get(key = session_key)
                session.delete()
            except ObjectDoesNotExist:
                pass

    @staticmethod
    def session_key_is_valid(user, session_key):
        session = Session.objects.filter(user=user, key=session_key, expire_date__gt = datetime.now())\
        # TODO: for Django >= 1.3 use .exists()
        return bool(session)

    def has_expired(self):
        return self.expire_date < datetime.now()
    
    def __unicode__(self):
        return "[" + unicode(self.user.username) + ": " + unicode(self.key) + "]"
