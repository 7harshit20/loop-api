from django.contrib import admin
from .models import Timing, Timezone, StoreStatus

# Register your models here.
admin.site.register(Timing)
admin.site.register(Timezone)
admin.site.register(StoreStatus)