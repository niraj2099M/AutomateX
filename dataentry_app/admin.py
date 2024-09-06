from django.contrib import admin

# Register your models here.

from .models import Customer, Employee, Student

admin.site.register(Student)
admin.site.register(Customer)
admin.site.register(Employee)