from django.contrib import admin
from .models import Payment, Expenses

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'month', "paid_amount", 'payment_status')
    
    search_fields = (
        'student__user__first_name', 'student__user__last_name',\
        'student__user__passport', "comment"
    )
    
    list_filter = ("month", "year", "created_at", 'payment_status', 'student__group')

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('title', 'expenses_type', 'amount', "month")
    search_fields = ('title', "comment")
    list_filter = ("expenses_type", "month", "year", "created_at")