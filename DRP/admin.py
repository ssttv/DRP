from django.contrib import admin
from models import LabGroup, License, Compound, ChemicalClass, CompoundRole
from models import PerformedReaction
from forms import LabGroupForm, CompoundAdminForm, PerformedRxnAdminForm

class LabGroupAdmin(admin.ModelAdmin):
  form = LabGroupForm

def licenseSnippet(license):
  return license.text[:100] + '...'

licenseSnippet.short_description = 'License Snippet'

class LicenseAdmin(admin.ModelAdmin):

  list_display = (licenseSnippet, 'effectiveDate')

class CompoundAdmin(admin.ModelAdmin):
  form = CompoundAdminForm

  list_display = ('abbrev', 'name', 'CSID', 'custom', 'labGroup')

class ChemicalClassAdmin(admin.ModelAdmin):
  
  list_display = ('label', 'description')

class CompoundRoleAdmin(admin.ModelAdmin):

  list_display = ('label', 'description')

class PerformedRxnAdmin(admin.ModelAdmin):

  list_display = ('Reference', 'user', 'labGroup', 'performedDateTime')
  form = PerformedRxnAdminform

admin.site.register(LabGroup, LabGroupAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Compound, CompoundAdmin)
admin.site.register(ChemicalClass, ChemicalClassAdmin)
admin.site.register(CompoundRole, CompoundRoleAdmin)
admin.site.register(Performedreaction, PerformedRxnAdmin)
