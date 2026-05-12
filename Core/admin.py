from django.contrib import admin
from .models import User,HazardReport,Hospital,Patient,MissingComplaint

admin.site.register(User)
admin.site.register(HazardReport)
admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(MissingComplaint)