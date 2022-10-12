from django.contrib import admin

# Register your models here.
from.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test, Daytbl, Working_days
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Slot)
admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Home)
admin.site.register(Info)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Result)
admin.site.register(Test)
admin.site.register(Daytbl)
admin.site.register(Working_days)
