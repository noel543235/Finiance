from django.contrib import admin
from .models import Loan, Subscription, OneTime

# Register your models here.
   
class LoanAdmin(admin.ModelAdmin):
    model = Loan
    fieldsets = (
        (None, {'fields': ('user', 'label', 'date', 'amount', 'category', 'interest_rate', 'term', 'term_amt')}),
    )
   
    
class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    fieldsets = (
        (None, {'fields': ('user', 'label', 'amount', 'category', 'frequency')}),
    )
 
    
class OneTimeAdmin(admin.ModelAdmin):
    model = OneTime
    fieldsets = (
        (None, {'fields': ('user', 'label', 'amount', 'category')}),
    )

admin.site.register(Loan, LoanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(OneTime, OneTimeAdmin)