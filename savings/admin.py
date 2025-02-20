from django.contrib import admin
from .models import Savings

# Register your models here.

class SavingsAdmin(admin.ModelAdmin):
    model = Savings
    fieldsets = (
        (None, {'fields': ('user', 'label', 'amount', 'date', 'frequency')}),
    )

admin.site.register(Savings, SavingsAdmin)