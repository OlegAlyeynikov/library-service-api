from django.contrib import admin

from payment.models import Payment

# class TicketInLine(admin.TabularInline):
#     model = Ticket
#     extra = 1
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     inlines = (TicketInLine,)


admin.site.register(Payment)
# admin.site.register(Bus)
# admin.site.register(Trip)
# admin.site.register(Ticket)
