from django.contrib import admin

# Register your models here.
from . import models
from . import utils

class StatusInlineAdmin(admin.TabularInline):
    model = models.Status
    extra = 0
    show_change_link = True

class ProcessStepInlineAdmin(admin.TabularInline):
    model = models.ProcessStep
    extra = 0
    show_change_link = True

class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = models.FieldDefinition
    extra = 0
    show_change_link = True
    fields = ('name', 'descript', 'fieldtype', 'length', )

@admin.register(models.ProcessDefinition)
class ProcessDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'status')
    list_display_links = ('id', 'name', 'descript')
    ordering = ['id']
    inlines=[StatusInlineAdmin, ProcessStepInlineAdmin, FieldDefinitionInlineAdmin]
    # TODO this should provide a link to the app from the admin page
    # def view_on_site(self, instance):
    #     reverse()
    # TODO: referring field should be initialized to the originating process when creating a copy of one
    # Which should be it's own action.
    # Probably it's also wise not to allow editing it via the GUI
    # REFACT consider adding status schemes inline here?


class FieldPerStepInlineAdmin(admin.TabularInline):
    model = models.FieldPerstep
    extra = 0
    show_change_link = True

class StatusInlineAdmin(admin.TabularInline):
    model = models.Status
    extra = 0
    show_change_link = True


@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    # REFACT process should auto populate with process from whom this is created
    list_display = ('id', 'name', 'descript', 'index', 'process')
    list_display_links = ('id', 'name')
    ordering = ('id',)
    inlines = (FieldPerStepInlineAdmin, StatusInlineAdmin)


# REFACT rename StatusTransitionAdmin
@admin.register(models.StatusTransition)
class StatusTransitionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'status', 'prestatus', 'remark', 'logic', 'process', )
    list_display_links = ('id', 'name')
    ordering = ('id',)
    # fields = ('process', 'name', ('prestatus', 'prestatus_link'), ('status', 'status_link'), 'remark')
    exclude = ('logic', ) # TODO: enable when it actually does something
    # TODO investigate overriding the form used to generate the widgets, this should allow customizing the widgets
    # see: https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_form
    # TODO investigate overriding the response from change_view (which should be after the widgets are created but before they are rendered)
    # https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.change_view
    # TODO formfield_overrides should allow me to specify a custom ForeignKey Widget - probably the most direct route to success
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': }
    # }


class StatusTransitionInlineAdmin(admin.TabularInline):
    model = models.StatusTransition
    extra = 0
    show_change_link = True
    # fk_name = 'status'
    verbose_name = 'StatusTransition'
    verbose_name_plural = 'StatusTransitions'
    fields = ('process', 'name', 'prestatus', 'status',)
    # REFACT: auto set process, should filter choices to process


class StatusTransitionIncommingInlineAdmin(StatusTransitionInlineAdmin):
    fk_name = 'status'
    verbose_name = 'Incomming StatusTransition'
    verbose_name_plural = 'Incomming StatusTransitions'
    # REFACT: auto set process, should filter choices to process


class StatusTransitionOutgoingInlineAdmin(StatusTransitionInlineAdmin):
    fk_name = 'prestatus'
    verbose_name = 'Outgoing StatusTransition'
    verbose_name_plural = 'Outgoing StatusTransitions'
    # REFACT: auto set process, should filter choices to process


@admin.register(models.Status)
class StatusAdmin (admin.ModelAdmin):
    list_display = ('id', 'process', 'name', 'role', 'step')
    list_display_links = ('id', 'name')
    ordering = ['id']
    inlines = [StatusTransitionIncommingInlineAdmin, StatusTransitionOutgoingInlineAdmin]


@admin.register(models.FieldDefinition)
class FieldDefinitionAdmin(admin.ModelAdmin):
    # process field should auto populate with process of process step when it is created
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
    list_display_links = ('id', 'runstatus')
    ordering = ['id']


@admin.register(models.RoleInstance)
class RoleInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'procinst')
    ordering = ['id']

class UsergroupMemberInlineAdmin(admin.TabularInline):
    model = models.UsergroupMember
    extra = 0
    show_change_link = True
    verbose_name = 'GroupMember'
    verbose_name_plural = 'GroupMembers'
    fields = ('pycuser', )

@admin.register(models.Usergroup)
class UsergroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript')
    list_display_links = ('id', 'name')
    ordering = ['id']
    inlines = [UsergroupMemberInlineAdmin]

# @admin.register(models.UsergroupMember)
# class RoleInstanceAdmin(admin.ModelAdmin):
#    list_display = ('id', 'usergroup', 'pycuser')
#    ordering = ['id']

# REFACT: should be read only?
# Ideally created by a separate system, for examle sql trigger based, to ensure a clear distinction line between the two systems
@admin.register(models.PycessLog)
class PycessLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'time')
    ordering = ['id']
