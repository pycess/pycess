# coding: utf8
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import json

from . import utils

# pycess models - gem. Workshop 27. June 2013
#   Version 0.14 - 
#   V 0.1 Bernd Brincken - 12. Sept 2014

# REFACT consider to extract name, description and help fields into abstract superclass

# REFACT: consider rename, collides with StatusScheme and Statuslist
class StatusChoices(object):
    PLANNED, IN_DEVELOPMENT, USABLE, ACTIVE, DEPRECATED, DISABLED = range(6)

## I - Prozess-Definition
class ProcessDefinition(models.Model):
    """Represents one of many different processes. Can be derived from another process."""
    name = models.CharField(max_length=200)
    descript = models.CharField(max_length=200, blank=True)
    
    status = models.PositiveSmallIntegerField(choices=utils.choices(StatusChoices))
    
    version = models.PositiveSmallIntegerField(default=1)
    "TODO: Simple counter, should be increased for each new version"
    
    refering = models.ForeignKey('ProcessDefinition', null=True, blank=True)
    "TODO: Should refer to the original this process was forked from."
    
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
        if not self.first_transition().role.role_instance.filter(pycuser=creator).exists():
            RoleInstance.objects.create(
                role=self.first_transition().role,
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
        return StatusScheme.objects.get(process=self, prestatus=None)
    


class ProcessStep(models.Model):
    """Ties a role to a specific set of fields (and later actions). 
    
    Tells the state machine who can trigger and execute this state machine and what kind of interface he will see for it."""
    
    process = models.ForeignKey('ProcessDefinition', related_name='steps', null=True)
    # role-Verweis wurde per 19.03.15 nach StatusScheme verschoben
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
    
    class Meta:
        verbose_name_plural = "2. Process Steps"
    
    def overview_fields(self):
        return [
            field 
            for field in self.field_perstep.order_by('order').all()
            if field.should_show_in_overview
        ]
    
    def possible_transitions(self):
        return StatusScheme.objects.filter(prestatus=self).all()
    
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
    
# REFACT consider rename to Status
class Statuslist(models.Model):
    """Node in the process state machine / Liste der verfuegbaren Status zur Prozess-Definiton"""
    # Neu hinzu per 14.03.15, da StatusScheme nun 1..n Tupel pro Status haben kann
    process = models.ForeignKey('ProcessDefinition', null=True)
    name    = models.CharField(max_length=20)
    role    = models.ForeignKey('RoleDefinition', null=True)
    
    # REFACT: consider adding description and help fields
    
    class Meta:
        verbose_name_plural = "3. Status"
        unique_together = ('process', 'name',)
    
    def __str__(self):
        return self.name
    
    def is_editable_by_user(self, user):
        return self.scheme_status.filter(role__role_instance__pycuser=user).exists()
    

# REFACT: consider rename to StatusTransition, for better self documentation --dwt
class StatusScheme(models.Model):
    """Edges in the process state machine / Status-Verknuepfungen zum Prozess und deren Bedeutung """
    
    # pre_status == NULL for entry step into the process
    # Use case: process which can be started at many places - by different roles? 
    # Use case: allowing steps that loop on the same state, but with logic. E.g.: remind me after x days.
    
    process   = models.ForeignKey('ProcessDefinition', related_name='schemes', null=True)
    name      = models.CharField(max_length=20) # REFACT: too short
    prestatus = models.ForeignKey('Statuslist' , related_name='scheme_prestatus', null=True, blank=True)
    status    = models.ForeignKey('Statuslist' , related_name='scheme_status', null=True)
    
    # REFACT: consider moving to Statuslist too, for consistency / ease of programming?
    step      = models.ForeignKey('ProcessStep', related_name='status_step', null=True)
    
    remark = models.CharField(max_length=200, blank=True)
    
    logic  = models.CharField(max_length=200, blank=True)
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift
    #  und bei >1 moeglichen Folge-Steps den konkreten ermittelt
    # Could also be used to auto transition a process to a new state if the process has lingered in a specific state for some time.¡
    
    class Meta:
        verbose_name_plural = "4. Status Scheme"
    
    def __str__(self):
        return self.name
    

class FieldPerstep(models.Model):
    """Describes how a fields is tied to a specific step / Fields, die pro Schritt angezeigt/abgefragt werden"""
    
    step  = models.ForeignKey('ProcessStep', related_name='field_perstep')
    field_definition = models.ForeignKey('FieldDefinition')
    interaction = models.PositiveSmallIntegerField(default=0)
    # 0: Show  2: Editable - 3: Not-NULL forced
    # REFACT: consider splitting this into several bools for 1. Ease of manipulation in django admin, 2. ease of debugging (no more json errors because somebody can't type perfect json in the django admin), ... --dwt
    # REFACT consider moving interaction into parameters?
    
    parameter   = models.TextField(default='{}')
    # JSON-Parameter, etwa  Anzeigeoptionen bei overview-Liste
    # REFACT consider adding python level properties for the parameters?
    
    editdefault = models.CharField(max_length=200, blank=True)
    # wird bei interaction>0 und leerem Feld eingesetzt
    #   Typ ist ggf. umzusetzen, z.B. text>integer
    order = models.PositiveSmallIntegerField(default=1)
    #   Abfolge des Felds im Formular. Evt. in 10er Stufen, 
    #     damit bei Umstellungen nicht alle order-s zu aendern sind.
    
    class Meta:
        unique_together = ('step', 'field_definition', )
    
    def __str__(self):
        return str(self.id)
    
    # REFACT: research if there is a way to route accesses to parameters through this method
    def json_parameter(self):
        try:
            return json.loads(self.parameter or '{}')
        except ValueError as error:
            raise ValueError("Erraneous JSON, check it. Original error: %s" % error)
        # REFACT: remove or '{}'? --dwt
    
    @property
    def should_show_in_overview(self):
        return self.json_parameter().get('should_show_in_overview', False)
    
    def json_schema(self):
        schema = self.field_definition.json_schema()
        schema['propertyOrder'] = self.order
        return schema
    

class FieldDefinition(models.Model):
    """Defines a field in a process / Im Process insgesamt verfuegbare Felder"""
    
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
    
    # REFACT: consider rename to field_type / type
    fieldtype = models.PositiveSmallIntegerField(choices=utils.choices(FieldtypeChoices))
    
    # TODO: what is this field actually meant for? -mh
    length = models.PositiveSmallIntegerField(default=1)
    # Length 1 bei Typen mit impliziter Laenge, etwa Date
    
    parent = models.ForeignKey('FieldDefinition', null=True, blank=True)
    # Field-Struktur ermoeglicht 1:n Datenbeziehungen auf Instanz-Ebene
    
    # REFACT: consider renaming to resolve naming collision with type() and fieldtype
    class TypeChoices(object):
        NORMAL, INTERNAL, JAVASCRIPT_INTERNAL = range(3)
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
    

class RoleDefinition(models.Model):
    """Roles available for a process"""
    
    process = models.ForeignKey('ProcessDefinition')
    name    = models.CharField(max_length=200)
    descript= models.CharField(max_length=200, blank=True)
    
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
    currentstatus = models.ForeignKey('Statuslist', blank=True, null=True)
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
    
    def overview_fields(self):
        if self.currentstep is None: 
            return []
        return [
            (field, self.json_data().get(field.field_definition.name, None))
             for field in self.currentstep.overview_fields()
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
    


# REFACT: should be read only and generated by triggers in the database (to ensure clean privilege separation between the two code paths)
# REFACT PycessLog
class PycLog(models.Model):
    """Log der Aktionen auf Pycess-Anwendungs-Ebene"""
    
    time    = models.DateTimeField()
    action  = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.id)
    

# - Ende models.py -

# For python 2/3 compatibility
def annotate_models_as_python_2_unicode_compatible():
    # see: https://docs.djangoproject.com/en/1.7/topics/python3/#str-and-unicode-methods
    
    def safe_issubclass(a_class, a_superclass):
        try:
            return issubclass(a_class, a_superclass)
        except TypeError as e:
            return False
    
    for name, class_ in locals().copy().items():
        if safe_issubclass(class_, models.Model):
            locals()[name] = python_2_unicode_compatible(class_)

annotate_models_as_python_2_unicode_compatible()