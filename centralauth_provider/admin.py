from models import *
from django.contrib import admin
from django.utils.translation import ugettext as _

def user_name(obj):
    return obj.user.username
user_name.short_description = "Username"

class SessionAdmin(admin.ModelAdmin):
    list_display = (user_name, 'key', 'expire_date')
    search_fields = ["user__first_name", "user__last_name", "user__email", "key", "expire_date"]
    fieldsets = (
        ('', {'fields': ('user', 'key', 'expire_date', ),}),
    )

admin.site.register(Session, SessionAdmin)

