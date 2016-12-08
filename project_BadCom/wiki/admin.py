from django.contrib import admin
from wiki.models import *

admin.site.register(User)
admin.site.register(Document)
admin.site.register(Comment)


