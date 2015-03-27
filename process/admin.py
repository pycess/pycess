from django.contrib import admin

# Register your models here.
from . import models

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

# Not a nice monkey patch - but it works. :/ -mh
# from django.utils.translation import ugettext as _
# from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
# class RelatedFieldWithEditLinkWidget(RelatedFieldWidgetWrapper):
#
#     def render(self, name, value, *args, **kwargs):
#         output = [super(RelatedFieldWithEditLinkWidget, self).render(name, value, *args, **kwargs)]
#         try:
#             rel_to = self.rel.to
#             info = (rel_to._meta.app_label, rel_to._meta.model_name)
#             # import sys; sys.stdout = sys.__stdout__; from pdb import set_trace; set_trace()
#             model_id = value
#             related_url = reverse('admin:%s_%s_change' % info, current_app=self.admin_site.name, args=(model_id,))
#             output.append('<a href="%s" class="edit" id="edit_id_%s" title="%s">%s</a>'
#                       % (related_url, name, _('Edit'), _('Edit')))
#             return mark_safe(''.join(output))
#         except Exception as e:
#             import logging
#             logging.exception('tried to add my edit link')
#             return output[0]
#
# class ModelAdmin(admin.ModelAdmin):
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         widget = super(ModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
#         print('formfield_for_foreignkey', 'widget', widget)
#         return widget

import django.contrib.admin.widgets
django.contrib.admin.widgets.RelatedFieldWidgetWrapper = RelatedFieldWithEditLinkWidget

class InlineEditLinkMixin(object):
    "Needs to be inherited from BEFORE admin.*Inline"
    readonly_fields = ['edit_details']
    edit_label = "Edit"
    def edit_details(self, obj):
        if obj.id:
            opts = self.model._meta
            return "<a href='%s'>%s</a>" % (reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()),
                args=[obj.id]
            ), self.edit_label)
        else:
            return "(save to edit details)"
    edit_details.allow_tags = True


class StatusListInlineAdmin(InlineEditLinkMixin, admin.TabularInline):
    model = models.Statuslist
    extra = 0

class ProcessStepInlineAdmin(InlineEditLinkMixin, admin.TabularInline):
    model = models.ProcessStep
    extra = 0
    fields = ('name', 'edit_details')

@admin.register(models.ProcessDefinition)
class ProcessDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descript', 'status')
    list_display_links = ('id', 'name')
    ordering = ['id']
    inlines=[StatusListInlineAdmin, ProcessStepInlineAdmin]
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


class StatusSchemeInlineAdmin(InlineEditLinkMixin, admin.TabularInline):
    model = models.StatusScheme
    extra = 0
    # fk_name = 'status'
    verbose_name = 'StatusTransition'
    verbose_name_plural = 'StatusTransitions'
    fields = ('process', 'name', 'step', 'prestatus', 'status', 'role', 'edit_details', )
    # REFACT: auto set process, should filter choices to process


# class ProcessStepAdmin(admin.ModelAdmin):
#  list_display = ('id', 'name', 'descript', )
# admin.site.register(models.FieldPerstep) > models.ProcessStep

@admin.register(models.ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    # REFACT process should auto populate with process from whom this is created
    list_display = ('id', 'name', 'descript', 'index', 'process')
    list_display_links = ('id', 'name')
    ordering = ('id',)
    inlines = (FieldPerStepInlineAdmin, StatusSchemeInlineAdmin)

from django.contrib.contenttypes.fields import GenericForeignKey

class StatuslistInlineAdmin(InlineEditLinkMixin, admin.TabularInline):
    model = models.Statuslist
    extra = 0

@admin.register(models.StatusScheme)
# @add_link_field('statuslist', 'status', field_name='status_link', short_description='Edit')
# @add_link_field('statuslist', 'prestatus', field_name='prestatus_link', short_description='Edit')
class StatusSchemeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'status', 'step', 'prestatus', 'role', 'remark', 'logic', 'process', )
    list_display_links = ('id', 'name')
    ordering = ('id',)
    # fields = ('process', 'name', ('prestatus', 'prestatus_link'), ('status', 'status_link'), 'step', 'role', 'remark')
    exclude = ('logic', ) # TODO: enable when it actually does something
    # TODO investigate overriding the form used to generate the widgets, this should allow customizing the widgets
    # see: https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_form
    # TODO investigate overriding the response from change_view (which should be after the widgets are created but before they are rendered)
    # https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#django.contrib.admin.ModelAdmin.change_view
    # TODO formfield_overrides should allow me to specify a custom ForeignKey Widget - probably the most direct route to success
    # formfield_overrides = {
    #     models.ForeignKey: {'widget': }
    # }


class StatusSchemeIncommingInlineAdmin(StatusSchemeInlineAdmin):
    fk_name = 'status'
    verbose_name = 'Incomming StatusTransition'
    verbose_name_plural = 'Incomming StatusTransitions'
    # REFACT: auto set process, should filter choices to process


class StatusSchemeOutgoingInlineAdmin(StatusSchemeInlineAdmin):
    fk_name = 'prestatus'
    verbose_name = 'Outgoing StatusTransition'
    verbose_name_plural = 'Outgoing StatusTransitions'
    # REFACT: auto set process, should filter choices to process


@admin.register(models.Statuslist)
class StatusListAdmin (admin.ModelAdmin):
    list_display = ('id', 'process', 'name')
    list_display_links = ('id', 'name')
    ordering = ['id']
    inlines = [StatusSchemeIncommingInlineAdmin, StatusSchemeOutgoingInlineAdmin]


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
