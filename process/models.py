# coding: utf8
from __future__ import unicode_literals
"""
WARNING: all __str__() methods need to return unicode - else python 2 will get confused

The reason for this is that python3 handles everything as unicode - thus we decorate all the models
to move __str__ into __unicode__ and synthesized a __str__ that will encode __unicode__ as utf8.
"""

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import json

from . import utils

# REFACT consider to extract name, description and help fields into abstract superclass

# REFACT: consider rename, collides with StatusTransition and Status
class StatusChoices(object):
    PLANNED, IN_DEVELOPMENT, USABLE, ACTIVE, DEPRECATED, DISABLED = range(6)

## I - Prozess-Definition
# REFACT rename Process
class ProcessDefinition(models.Model):
    """Represents one of many different processes. Can be derived from another process."""
    name = models.CharField(max_length=200)
    descript = models.CharField(max_length=200, blank=True)
    
    status = models.PositiveSmallIntegerField(choices=utils.choices(StatusChoices))
    
    version = models.PositiveSmallIntegerField(default=1)
    # TODO: Simple counter, should be increased for each new version
    
    refering = models.ForeignKey('ProcessDefinition', null=True, blank=True)
    # TODO: Should refer to the original this process was forked from.
    
    class Meta:
        verbose_name_plural = "1. Process Definitions"
    
    def create_instance(self, creator):
        instance = ProcessInstance.objects.create(
            process=self,
            currentstatus=self.first_transition().status,
            starttime=timezone.now(),
            stoptime=timezone.now(),
            runstatus=StatusChoices.ACTIVE,
        )
        if not instance.currentstatus.role.role_instance.filter(pycuser=creator).exists():
            RoleInstance.objects.create(
                role=instance.currentstatus.role,
                procinst=instance,
                pycuser=creator,
                entrytime=timezone.now(),
            )
        return instance
    
    def __str__(self):
        return self.name
    
    def first_transition(self):
        # REFACT: rename first_transition
        # REFACT: consider changing to  first_transition(for_role) api
        # return self.schemes.filter(prestatus=None).first()
        return StatusTransition.objects.get(process=self, prestatus=None)
    

# REFACT consider rename to State, Status, ProcessNode, ProcessStatus, ProcessState
class Status(models.Model):
    """Node in the process state machine"""
    # Neu hinzu per 14.03.15, da StatusTransition nun 1..n Tupel pro Status haben kann
    process = models.ForeignKey('ProcessDefinition', null=True, related_name='status_list')
    name    = models.CharField(max_length=20)
    role    = models.ForeignKey('RoleDefinition', null=True)
    step    = models.ForeignKey('ProcessStep', related_name='status_step', null=True)
    
    
    # REFACT: consider adding description and help fields
    
    class Meta:
        verbose_name_plural = "3. Status"
        unique_together = ('process', 'name',)
    
    def __str__(self):
        return self.name
    
    def is_editable_by_user(self, user):
        return self.role.role_instance.filter(pycuser=user).exists()
    
    def possible_transitions(self):
        return StatusTransition.objects.filter(prestatus=self).all()
    

class ProcessStep(models.Model):
    """Ties a role to a specific set of fields (and later actions). 
    
    Tells the state machine who can trigger and execute this state machine and what kind of interface
    he will see for it.
    REFACT what is this exactly required for? Seems like it's quite redundant with the Status
    """
    
    process = models.ForeignKey('ProcessDefinition', related_name='steps', null=True)
    # role-Verweis wurde per 19.03.15 nach StatusTransition verschoben
    name = models.CharField(max_length=200)
    descript = models.CharField(max_length=200, blank=True)
    
    # REFACT: remove until we actually ue this for something? --dwt
    # also: self.id is available and guaranteed to be unique within the process definition
    index = models.PositiveSmallIntegerField(default=0)
    """Id innerhalb der ProcDef"""
    
    # REFACT: remove until we actually need / use this? --dwt
    class ActiontypeChoices(object):
        NOT_USED = 0
    
    actiontype = models.PositiveSmallIntegerField(choices=utils.choices(ActiontypeChoices), default=0)
    """Etwa 'Entscheidung', 'Freigabe', 'Kalkulation' > Logik dahinter"""
    # REFACT consider to pull out into a 1:n linked model like role and fields
    
    class Meta:
        verbose_name_plural = "2. Process Steps"
    
    def overview_fields(self):
        return [
            field 
            for field in self.field_perstep.order_by('order').all()
            if field.is_part_of_overview
        ]
    
    def __str__(self):
        return self.name
    
    def json_schema(self):
        # See: https://github.com/jdorn/json-editor
        return {
            'type': 'object',
            'title': self.name,
            'properties': dict(
                # REFACT: consider moving key generation into field
                # REFACT: find a way to get a better css id/class on the fields
                # should be id-name or something like that
                (field.field_definition.name, field.json_schema()) 
                    for field in self.field_perstep.all()
            ),
            'defaultProperties': [field.field_definition.name for field in self.field_perstep.all()]
        }
    
    # REFACT: inline? --dwt
    def json_data(self, an_instance):
        # FIXME: need to filter out only the values interesting for the current step
        # that should be possible with some clever use of json schema
        return an_instance.procdata
    
class StatusTransition(models.Model):
    """Edges in the process state machine"""
    
    # pre_status == NULL for entry step into the process
    # Use case: process which can be started at many places - by different roles? 
    # Use case: allowing steps that loop on the same state, but with logic. E.g.: remind me after x days.
    
    process   = models.ForeignKey('ProcessDefinition', related_name='schemes', null=True)
    # REFACT: consider to get rid of ht eprocess here - pre- and post-status already fully append this to a (or more) specific processes
    
    name      = models.CharField(max_length=20) # REFACT: too short
    prestatus = models.ForeignKey('Status' , related_name='scheme_prestatus', null=True, blank=True)
    status    = models.ForeignKey('Status' , related_name='scheme_status', null=True)
    
    remark = models.CharField(max_length=200, blank=True)
    
    logic  = models.CharField(max_length=200, blank=True)
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift
    #  und bei >1 moeglichen Folge-Steps den konkreten ermittelt
    # Could also be used to auto transition a process to a new state if the process has lingered in a specific state for some time.¡
    
    class Meta:
        verbose_name_plural = "4. Status Transitions"
    
    def __str__(self):
        return self.name
    

class FieldPerstep(models.Model):
    """Describes how a fields is tied to a specific step"""
    
    step  = models.ForeignKey('ProcessStep', related_name='field_perstep')
    field_definition = models.ForeignKey('FieldDefinition')
    interaction = models.PositiveSmallIntegerField(default=0)
    # 0: Show  2: Editable - 3: Not-NULL forced
    # REFACT: consider splitting this into several bools for 1. Ease of manipulation in django admin, 2. ease of debugging (no more json errors because somebody can't type perfect json in the django admin), ... --dwt
    # REFACT consider moving interaction into parameters?
    
    editdefault = models.CharField(max_length=200, blank=True)
    # wird bei interaction>0 und leerem Feld eingesetzt
    #   Typ ist ggf. umzusetzen, z.B. text>integer
    order = models.PositiveSmallIntegerField(default=1)
    #   Abfolge des Felds im Formular. Evt. in 10er Stufen, 
    #     damit bei Umstellungen nicht alle order-s zu aendern sind.
    
    is_part_of_overview = models.BooleanField(default=False)
    "Wether this field should be shown in the overview"
    
    class Meta:
        unique_together = ('step', 'field_definition', )
    
    def __str__(self):
        return str(self.id)
    
    def json_schema(self):
        schema = self.field_definition.json_schema()
        schema['propertyOrder'] = self.order
        return schema
    

class FieldDefinition(models.Model):
    """Defines a field in a process"""
    
    # REFACT remove, should be attached to a process via a process-step. Doing away with the direct connection could also help in pulling in fields through the steps that are triggered, thus having an easier time defining reusable fields
    process   = models.ForeignKey('ProcessDefinition', null=True)
    name      = models.CharField(max_length=200)
    # REFACT: rename description
    descript  = models.CharField(max_length=200, blank=True)
    
    # REFACT: remove length description to allow longer help texts if neccessary?
    # REFACT: rename help / helptext
    fieldhelp = models.CharField(max_length=200, blank=True)
    # In einem Formular ggf. angezeigte ausfuehrlichere Erklaerung zur Bedeutung des Feldes
    
    class FieldtypeChoices(object):
        STRING, INTEGER, FLOAT, FINANCE_NUMBER_TBD, DATE, DATETIME, BLOB_TBD, ENUM_TBD = range(8)
    # TODO: need bool field
    
    # REFACT: consider rename to field_type / type
    fieldtype = models.PositiveSmallIntegerField(choices=utils.choices(FieldtypeChoices))
    
    # TODO: what is this field actually meant for? -mh
    length = models.PositiveSmallIntegerField(default=1)
    # Length 1 bei Typen mit impliziter Laenge, etwa Date
    
    parent = models.ForeignKey('FieldDefinition', null=True, blank=True)
    # Field-Struktur ermoeglicht 1:n Datenbeziehungen auf Instanz-Ebene
    
    # REFACT: consider renaming to resolve naming collision with type() and fieldtype
    class TypeChoices(object):
        NORMAL, INTERNAL_TBD, JAVASCRIPT_INTERNAL_TBD = range(3)
    type = models.PositiveSmallIntegerField(choices=utils.choices(TypeChoices), default=0)
    
    class Meta:
        verbose_name_plural = "5. Field Definitions"
    
    def __str__(self):
        return self.name
    
    def json_schema(self):
        type_mapping = {
            1: 'string',
            5: 'string',
        }
        format_mapping = {
            1: 'textarea',
            5: 'date',
        }
        if self.fieldtype not in type_mapping:
            print("Missing type mapping for type %s" % self.fieldtype)
        if self.fieldtype not in format_mapping:
            print("Missing format mapping for type %s" % self.fieldtype)
        
        return {
            'type': type_mapping.get(self.fieldtype, 'string'),
            'title': self.descript,
            'format': format_mapping.get(self.fieldtype, 'string')
        }
    

# REFACT rename UserRole?
class RoleDefinition(models.Model):
    """Roles available for a process"""
    
    process   = models.ForeignKey('ProcessDefinition')
    usergroup = models.ForeignKey('Usergroup', null=True, blank=True)
    #  Optional - Group from which a user may be chosen for a process-Instance
    name      = models.CharField(max_length=200)
    descript  = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = "6. Role Definitions"
    
    def __str__(self):
        return self.name
    

class ProcessInstance(models.Model):
    """Runtime Instances for a process"""
    
    process   = models.ForeignKey('ProcessDefinition', related_name="instances")
    # TODO: Need a way to merge in updates to this field
    # TODO: need a standard way to get a meaningfull abbreviation of the current step data to serve as headline
    # procdata= models.JSONdata() .. TODO
    procdata  = models.TextField(default='{}')
    # REFACT: consider to change to a log storage here, that stores changes and who did them when
    # The current idea is to use a db driven log storage here, but making this explicit would be very nice, as it allows this to be accessed easily from the app. That would probably mean a to many relation to the log storage facility and then getting the latest of the linked entries - maybe even one is marked as current from here.
    # This could also allow some simple conflict resolution to be done?
    
    currentstatus = models.ForeignKey('Status', blank=True, null=True)
    starttime = models.DateTimeField()
    stoptime  = models.DateTimeField(null=True)
    
    runstatus = models.PositiveSmallIntegerField(choices=utils.choices(StatusChoices))
    "TODO: Should determine where / wether this process is displayed in lists"
    
    class Meta:
        verbose_name_plural = "7. Process Instances"
    
    def __str__(self):
        return str(self.id)
    
    def json_data(self):
        try:
            return json.loads(self.procdata or '{}')
        except ValueError as error:
            raise ValueError("Erraneous JSON, check it. Original error: %s" % error)
    
    # REFACT should this go somewhere else? Overview fields are intrinsically bound to the current step, so maybe it should go there?
    def overview_fields(self):
        if self.currentstatus is None: 
            return []
        return [
            (field, self.json_data().get(field.field_definition.name, None))
             for field in self.currentstatus.step.overview_fields()
        ]
    
    def transition_with_status(self, a_status):
        assert a_status in self.currentstatus.scheme_prestatus.all(), "Invalid transition"
        # TODO: this is probably where the logic of the transition needs to be computed / done
        self.currentstatus = a_status.status
    
    def add_user_for_role(self, user, role):
        return RoleInstance.objects.create(
            role=role,
            procinst=self,
            pycuser=user,
            entrytime=timezone.now(),
        )
    
    def responsible_users(self):
        return [
            instance.pycuser 
            for instance 
            in self.currentstatus.role.role_instance.all()
        ]


class RoleInstance(models.Model):
    """Roles assigned for a process instance, connected to Django-User"""
    
    role      = models.ForeignKey('RoleDefinition', related_name='role_instance')
    procinst  = models.ForeignKey('ProcessInstance', blank=True, null=True)
    pycuser   = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    entrytime = models.DateTimeField()
    exittime  = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "9. Role Instances"
    
    def __str__(self):
        return str(self.id)


# REFACT consider removing this, role is already a group concept that could be used for different processes
# REFACT remove, use django group model instead if required at all
class Usergroup(models.Model):
    """Group of Users that may be used for different processes"""
    name    = models.CharField(max_length=200)
    descript= models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = "A. Usergroups"
    
    def __str__(self):
        return self.name

class UsergroupMember(models.Model):
    """Users assigned to Groups"""
    usergroup = models.ForeignKey('Usergroup', related_name='member_of_group')
    pycuser   = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "B. Usergroup-Members"
    
    def __str__(self):
        return str(self.id)

# REFACT: should be read only and generated by triggers in the database (to ensure clean privilege separation between the two code paths)
class PycessLog(models.Model):
    """Log der Aktionen auf Pycess-Anwendungs-Ebene"""
    
    time    = models.DateTimeField()
    # REFACT This needs to be unlimited length to allow meaningfull logging
    action  = models.CharField(max_length=200)
    # REFACT should also track who did it
    
    def __str__(self):
        return str(self.id)
    

# For python 2/3 compatibility, annotate all models with the right decorator
# see: https://docs.djangoproject.com/en/1.7/topics/python3/#str-and-unicode-methods
def safe_issubclass(a_class, a_superclass):
    try:
        return issubclass(a_class, a_superclass)
    except TypeError as e:
        return False

for name, class_ in locals().copy().items():
    if safe_issubclass(class_, models.Model):
        python_2_unicode_compatible(class_)

