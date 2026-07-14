from django.contrib import admin

from cdr.models import Organization, Mno, Customer, PricePlan, NetworkProvider, Thing

admin.site.register(
    [
        Organization,
        Mno,
        Customer,
        NetworkProvider,
        PricePlan,
        Thing,
    ]
)


# class ThingAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'thingname',
#         'thingnameraw',
#         'thingsgroupname',
#         'thingsgroupid',
#         'thingsgroupidraw',
#     )
# admin.site.register(Thing, ThingAdmin)
