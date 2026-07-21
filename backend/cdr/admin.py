from django.contrib import admin

from cdr.models import Organization, Mno, Customer, PricePlan, NetworkProvider, Thing, Session, Device

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
        '__str__',
        'device',
        'sessioncreatetime',
        'realusage',
        'uom',
    )
    list_filter = (
        'device__imsi',
        'sessionid',
    )
    search_fields = (
        'sessionid',

    )

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '__str__',
        'thingsgroupid',
        'customer__customername',
    )

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '__str__',
        'iccid',
        'imsi',
        'msisdn',
        'imei',
    )
    list_filter = (
        'imsi',
    )