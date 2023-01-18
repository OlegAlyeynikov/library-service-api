from django.contrib import admin

from borrowing.models import Borrowing

# class TicketInLine(admin.TabularInline):
#     model = Ticket
#     extra = 1
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     inlines = (TicketInLine,)


admin.site.register(Borrowing)
# admin.site.register(Bus)
# admin.site.register(Trip)
# admin.site.register(Ticket)