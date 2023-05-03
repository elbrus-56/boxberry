from django.contrib import admin
from delivery.models import DeliveryData, PickPoint




@admin.register(DeliveryData)
class DeliveryDataAdmin(admin.ModelAdmin):
    search_fields = ("departure_city", "destination_city", "address")
    list_display = ("__str__",)
    readonly_fields = ("id",)


@admin.register(PickPoint)
class PickPointAdmin(admin.ModelAdmin):
    search_fields = ("short_name", "full_name", "pick_point")
    list_display = ('id',"__str__",'short_name', 'pick_point')



