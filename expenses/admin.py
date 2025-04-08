from django.contrib import admin
from .models import *

# Register your models here.

class LoanAdmin(admin.ModelAdmin):
    model = Loan
    fieldsets = (
        (None, {'fields': ('user', 'label', 'principal', 'amount', 'apr', 'term_amt', 'frequency', 'start_date', 'category')}),
    )


class RecurringAdmin(admin.ModelAdmin):
    model = Recurring
    fieldsets = (
        (None, {'fields': ('user', 'label', 'amount', 'start_date', 'frequency', 'end_date', 'category')}),
    )


class OneTimeAdmin(admin.ModelAdmin):
    model = OneTime
    fieldsets = (
        (None, {'fields': ('user', 'label', 'amount', 'date_purchased', 'category', 'description')}),
    )


class LoanPaymentAdmin(admin.ModelAdmin):
    model = LoanPayment
    fieldsets = (
        (None, {'fields': ('loan', 'payment_date', 'amount')}),
    )
<<<<<<< HEAD
    
    
=======


>>>>>>> releasev3
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
<<<<<<< HEAD
    
=======

>>>>>>> releasev3

admin.site.register(Loan, LoanAdmin)
admin.site.register(Recurring, RecurringAdmin)
admin.site.register(OneTime, OneTimeAdmin)
admin.site.register(LoanPayment, LoanPaymentAdmin)
admin.site.register(Category, CategoryAdmin)