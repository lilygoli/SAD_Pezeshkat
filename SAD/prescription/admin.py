from django.contrib import admin

from prescription.models import Prescriptions, Tests, Medicine, Injections

admin.site.register(Prescriptions)
admin.site.register(Tests)
admin.site.register(Medicine)
admin.site.register(Injections)
