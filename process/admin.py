from django.contrib import admin

# Register your models here.
from process.models import ProcessStep, ProcessDef, StatusScheme, FieldPerstep,  FieldDef, RoleDef, ProcInstance, RoleInstance, PycLog


admin.site.register(ProcessStep)
admin.site.register(ProcessDef)
admin.site.register(StatusScheme)
admin.site.register(FieldPerstep)
admin.site.register(FieldDef)
admin.site.register(RoleDef)
admin.site.register(ProcInstance)
admin.site.register(RoleInstance)
admin.site.register(PycLog)

