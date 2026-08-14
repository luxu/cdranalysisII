from django.contrib import admin

from cdr.models import Organization, Mno, Customer, PricePlan, NetworkProvider, Thing, Session, Device
from user.models import Profile

admin.site.register(
    [
        Organization,
        Mno,
        Customer,
        NetworkProvider,
        PricePlan,
    ]
)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'device',
        'device__iccid',
        'sessionid',
        'sessioncreatetime',
        'realusage',
        'uom',
    )
    list_filter = (
        'device__iccid',
        'sessionid',
    )
    search_fields = (
        'id',
        'sessionid',
    )

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '__str__',
        'thingsgroupid',
        'thingsgroupname',
        'customer',
    )

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'iccid',
        'imsi',
        'imei',
    )
    list_filter = (
        'imsi',
    )
