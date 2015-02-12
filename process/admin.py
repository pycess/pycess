from django.contrib import admin

# Register your models here.
from process.models import ProcessStep, ProcessDef, StatusScheme, FieldPerstep,  FieldDef, RoleDef, ProcInstance, RoleInstance, PycLog

class FieldperstepInline(admin.TabularInline):
  model = FieldPerstep
  extra = 1
class ProcstepAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'descript', 'index', 'process', 'role')
  list_display_links = ('id', 'name')
  inlines = [FieldperstepInline]
admin.site.register(ProcessStep, ProcstepAdmin)

class ProcdefAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'descript', 'status')
  list_display_links = ('id', 'name')
admin.site.register(ProcessDef, ProcdefAdmin)

class StatschemAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'selfstep', 'prestep', 'remark', 'logic', 'process')
  list_display_links = ('id', 'name')
admin.site.register(StatusScheme, StatschemAdmin)

#class ProcstepAdmin(admin.ModelAdmin):
#  list_display = ('id', 'name', 'descript', )
# admin.site.register(FieldPerstep) > ProcessStep

class FielddefAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'descript', 'fieldtype', 'length', 'type', 'process')
  list_display_links = ('id', 'name')
admin.site.register(FieldDef, FielddefAdmin)

class RoledefAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'descript', 'process')
  list_display_links = ('id', 'name')
admin.site.register(RoleDef,  RoledefAdmin)

class ProcinstAdmin(admin.ModelAdmin):
  list_display = ('id', 'status', 'process')
admin.site.register(ProcInstance, ProcinstAdmin)

class RoleinstAdmin(admin.ModelAdmin):
  list_display = ('id', 'role', 'procinst')
admin.site.register(RoleInstance, RoleinstAdmin)

class pyclogAdmin(admin.ModelAdmin):
  list_display = ('id', 'action', 'time')
admin.site.register(PycLog, pyclogAdmin)

