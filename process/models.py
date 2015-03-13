# coding: utf8
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import json

# pycess models - gem. Workshop 27. June 2013
#   Version 0.14 - 
#   V 0.1 Bernd Brincken - 12. Sept 2014

## I - Prozess-Definition

@python_2_unicode_compatible
class ProcessDef(models.Model):
    name = models.CharField(max_length=200)
    descript = models.CharField(max_length=200, blank=True)
    
    # von 1..2^16 hochgezaehlt für jede neue Version
    version = models.PositiveSmallIntegerField(default=1)
    
    #   REFACT: add constants for status
    # etwa 1-geplant 2-Definitionsphase 3-nutzbar 4-aktiv 5-postponed 6-deaktiv
    status = models.PositiveSmallIntegerField()
    
    # optional: Verweis auf Vorgaenger-Version oder Templates, Kopien etc.
    refering = models.ForeignKey('ProcessDef', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "1. Process Definitions"
    
    def __str__(self):
        return self.name
    
    def first_step(self):
        # REFACT: might need to switch this protocoll to consider objects without a prestep
        # initial objects
        return ProcessStep.objects.get(process=self, status_thisstep=models.F('status_prestep'))
        ## Aendern > =NULL statt pre=self
    


@python_2_unicode_compatible
class ProcessStep(models.Model):
    """Prozess-spezifischer Bearbeitungs-Schritt, umfasst definierte Felder (FieldPerstep)"""
    
    process = models.ForeignKey('ProcessDef', related_name='steps', null=True)
    role = models.ForeignKey('RoleDef',    null=True)
    name = models.CharField(max_length=200)
    descript = models.CharField(max_length=200, blank=True)
    index = models.PositiveSmallIntegerField()
    """Id innerhalb der ProcDef"""
    
    # REFACT: could/ should we replace index by a relation from ProcessDeff to
    #  its first ProcessStep?
    actiontype = models.PositiveSmallIntegerField()
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
        return StatusScheme.objects.filter(prestep=self).all()
    
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
        return an_instance.procdata


@python_2_unicode_compatible
class StatusScheme(models.Model):
    """Alle Status des Prozesses, dazu deren moegliche Vorgaenger-Status"""
    
    # prestep == NULL for entry step into the process
    # Use case: process which can be started at many places - by different roles?
    # Use case: allowing steps that loop on the same state, but with logic. E.g.: remind me after x days.
    
    process = models.ForeignKey('ProcessDef', null=True)
    
    # REFACT: consider requiring selfstep and prestep to be non null --dwt 
    #   vdB: Noe, denn Status koennen gern mal _vor_ den Steps definiert sein 
    # REFACT: rename related_name to something more unique > schon geaendert
    selfstep = models.ForeignKey(
        'ProcessStep', related_name='status_thisstep', null=True)
        
    # REFACT: rename related_name to something more unique > schon geaendert
    prestep = models.ForeignKey(
        'ProcessStep', related_name='status_prestep' , blank=True, null=True)
    # Erster Schritt: Prestep = Selfstep
    
    name   = models.CharField(max_length=20)
    remark = models.CharField(max_length=200, blank=True)
    
    logic  = models.CharField(max_length=200, blank=True)
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift
    #  und bei >1 moeglichen Folge-Steps den konkreten ermittelt
    
    class Meta:
        verbose_name_plural = "3. Status Schemes (Process Step Transitions)"
    
    def __str__(self):
        return self.name
    
    # Deprecated:   unique_together = ('process', 'selfstep', 'prestep',)
    #   Denn es kann durchaus mehrere Status fuer die gleiche pre>step Folge geben 


@python_2_unicode_compatible
class FieldPerstep(models.Model):
    """Fields, die pro Schritt angezeigt/abgefragt werden"""
    
    step  = models.ForeignKey('ProcessStep', related_name='field_perstep')
    field_definition = models.ForeignKey('FieldDefinition')
    interaction = models.PositiveSmallIntegerField(default=0)
    # 0: Show  2: Editable - 3: Not-NULL forced
    parameter   = models.TextField(default='{}')
    # JSON-Parameter, etwa  Anzeigeoptionen bei overview-Liste
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


@python_2_unicode_compatible
class FieldDefinition(models.Model):
    """ Im Process insgesamt verfuegbare Felder"""
    
    process   = models.ForeignKey('ProcessDef', null=True)
    name      = models.CharField(max_length=200)
    descript  = models.CharField(max_length=200, blank=True)
    fieldhelp = models.CharField(max_length=200, blank=True)
    # In einem Formular ggf. angezeigte ausfuehrlichere Erklaerung zur Bedeutung des Feldes
    fieldtype = models.PositiveSmallIntegerField()
    # Datentyp: 1-char, 2-int-number, 3-finance-number, 4-float-num, 5-Date,
    #	6-Datetime, 7 blob, 8-Enum (tbd)
    #   REFACT: consider to replace with real enum so that we can write the constructor as
    #     FieldDefinition(fieldType=FieldDefinition.STRING)
    length = models.PositiveSmallIntegerField(default=1)
    # Length 1 bei Typen mit impliziter Laenge, etwa Date
    parent = models.ForeignKey('FieldDefinition', null=True, blank=True)
    # Field-Struktur ermoeglicht 1:n Datenbeziehungen auf Instanz-Ebene
    type = models.PositiveSmallIntegerField(default=1)
    # etwa 1-normal 2-pycess-intern 3-javascript-intern
    
    class Meta:
        verbose_name_plural = "4. Field Definitions"
    
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


@python_2_unicode_compatible
class RoleDef(models.Model):
    """Roles available for a process"""
    
    process = models.ForeignKey('ProcessDef')
    name    = models.CharField(max_length=200)
    descript= models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = "5. Role Definitions"
    
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProcInstance(models.Model):
    """Runtime Instances for a process"""
    
    process   = models.ForeignKey('ProcessDef', related_name="instances")
    # TODO: Need a way to merge in updates to this field
    # TODO: need a standard way to get a meaningfull abbreviation of the current step data to serve as headline
    # procdata= models.JSONdata() .. TODO
    procdata  = models.TextField(default='{}')
    currentstep = models.ForeignKey('ProcessStep', blank=True, null=True)
    starttime = models.DateTimeField()
    stoptime  = models.DateTimeField(null=True)
    status    = models.PositiveSmallIntegerField()
    # Status: 1-geplant 2-Vorbereitung 3-aktiv 4-postponed 5-deaktiv 6-abgeschlossen
    
    class Meta:
        verbose_name_plural = "6. Process Instances"
    
    def json_data(self):
        return json.loads(self.procdata)
    
    def overview_fields(self):
        return [
            (field, self.json_data()[field.field_definition.name]) \
            for field in self.currentstep.overview_fields()
        ]
    
    def __str__(self):
        return str(self.id)
    
    def transition_with_status(self, a_status):
        assert a_status in self.currentstep.possible_transitions(), "Invalid transition"
        # TODO: this is probably where the logic of the transition needs to be computed / done
        self.currentstep = a_status.selfstep


@python_2_unicode_compatible
class RoleInstance(models.Model):
    """Roles assigned for a process instance"""
    
    role      = models.ForeignKey('RoleDef', related_name='role_instance')
    procinst  = models.ForeignKey('ProcInstance', blank=True, null=True)
    pycuser   = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    entrytime = models.DateTimeField()
    exittime  = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "8. Role Instances"
    
    def __str__(self):
        return str(self.id)


@python_2_unicode_compatible
class PycLog(models.Model):
    """Log der Aktionen auf Pycess-Anwendungs-Ebene"""
    
    time    = models.DateTimeField()
    action  = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

# - Ende models.py -
