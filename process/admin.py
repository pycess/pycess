from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.ProcessDefinition)
class ProcessDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'status')
    list_display_links = ('id', 'name')
    ordering = ['id']
    # TODO: referring field should be initialized to the originating process when creating a copy of one
    # Which should be it's own action.
    # Probably it's also wise not to allow editing it via the GUI

class FieldPerStepInlineAdmin(admin.TabularInline):
    model = models.FieldPerstep
    extra = 1

# class ProcessStepAdmin(admin.ModelAdmin):
#  list_display = ('id', 'name', 'descript', )
# admin.site.register(models.FieldPerstep) > models.ProcessStep

@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'index', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']
    inlines = [FieldPerStepInlineAdmin]


@admin.register(models.StatusScheme)
class StatusSchemeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'status', 'step', 'prestatus', 'role', 'remark', 'logic', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']


@admin.register(models.Statuslist)
class StatusListAdmin (admin.ModelAdmin):
    list_display = ('id', 'process', 'name')
    ordering = ['id']


@admin.register(models.FieldDefinition)
class FieldDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'descript', 'fieldtype', 'length', 'type', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']
    save_on_top = True
#  list_filter = ('process') > funktioniert nicht (?)


@admin.register(models.RoleDefinition)
class RoleDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'process')
    list_display_links = ('id', 'name')
    ordering = ['id']


@admin.register(models.ProcessInstance)
class ProcessInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'runstatus', 'process')
    ordering = ['id']


@admin.register(models.RoleInstance)
class RoleInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'procinst')
    ordering = ['id']


# REFACT: should be read only?
# Ideally created by a separate system, for examle sql trigger based, to ensure a clear distinction line between the two systems
@admin.register(models.PycLog)
class PycessLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'time')
    ordering = ['id']
