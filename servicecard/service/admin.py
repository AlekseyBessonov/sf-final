from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Car)
admin.site.register(models.CarModel)
admin.site.register(models.Engine)
admin.site.register(models.Transmition)
admin.site.register(models.LeadBridge)
admin.site.register(models.ControlBridge)
admin.site.register(models.MaintainceType)
admin.site.register(models.BrokeCharacter)
#admin.site.register(models.RepairType)
admin.site.register(models.RecoveryMethod)
admin.site.register(models.ServiceCompany)
admin.site.register(models.Complaint)
admin.site.register(models.Maintains)
