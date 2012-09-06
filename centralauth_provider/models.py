from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Session(models.Model):
    user = models.ForeignKey(User, related_name="sessions")
    key = models.CharField(unique = True, max_length = 20)
    expire_date = models.DateTimeField(default = lambda: datetime.now()+timedelta(days=30))
    
    @staticmethod
    def generate_unique_key():
        key = generate_random_key()
        while Session.objects.filter(key = key).count() > 0:
            key = generate_random_key()
        return key

    @staticmethod
    def generate_random_key(length = 20):
        key = ""
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for x in range(length):
	    key += random.choice(allowed_chars)
        return key

    def has_expired(self):
        return self.expire_date < datetime.now()
    
    def __unicode__(self):
        return "[" + unicode(self.user.username) + ": " + unicode(self.key) + "]"
