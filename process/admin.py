from django.contrib import admin

# Register your models here.
from process.models import ProcessStep, ProcessDefinition, Statuslist, StatusScheme, FieldPerstep,  FieldDefinition, RoleDefinition, ProcessInstance, RoleInstance, PycLog


class FieldperstepInline(admin.TabularInline):
    model = FieldPerstep
    extra = 1


class ProcstepAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'index', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']
    inlines = [FieldperstepInline]
admin.site.register(ProcessStep, ProcstepAdmin)


class ProcdefAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'status')
    list_display_links = ('id', 'name')
    ordering = ['id']
admin.site.register(ProcessDefinition, ProcdefAdmin)


class StatlistAdmin (admin.ModelAdmin):
    list_display = ('id', 'process', 'name')
    ordering = ['id']
admin.site.register(Statuslist, StatlistAdmin)


class StatschemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'status', 'step', 'prestatus', 'role', 'remark', 'logic', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']
admin.site.register(StatusScheme, StatschemAdmin)

# class ProcstepAdmin(admin.ModelAdmin):
#  list_display = ('id', 'name', 'descript', )
# admin.site.register(FieldPerstep) > ProcessStep


class FielddefAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'descript', 'fieldtype', 'length', 'type', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']
    save_on_top = True
#  list_filter = ('process') > funktioniert nicht (?)
admin.site.register(FieldDefinition, FielddefAdmin)


class RoleDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']
admin.site.register(RoleDefinition,  RoleDefinitionAdmin)


class ProcinstAdmin(admin.ModelAdmin):
    list_display = ('id', 'runstatus', 'process')
    ordering = ['id']
admin.site.register(ProcessInstance, ProcinstAdmin)


class RoleinstAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'procinst')
    ordering = ['id']
admin.site.register(RoleInstance, RoleinstAdmin)


class pyclogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'time')
    ordering = ['id']
admin.site.register(PycLog, pyclogAdmin)
