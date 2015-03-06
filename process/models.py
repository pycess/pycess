# coding: utf8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# pycess models - gem. Workshop 27 June 2013
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

    def __str__(self):
        return self.name

    def first_step(self):
        # consider: StatusScheme.objects.raw('SELECT * FROM
        #     process_statusscheme WHERE selfstep_id = prestep_id')
        return ProcessStep.objects.get(process=self, status_thisstep=models.F('status_prestep'))


@python_2_unicode_compatible
class ProcessStep(models.Model):
    """Prozess-spezifischer Bearbeitungs-Schritt, umfasst definierte Felder (FieldPerstep)"""
    
    process = models.ForeignKey('ProcessDef', null=True)
    role = models.ForeignKey('RoleDef',    null=True)
    name = models.CharField(max_length=200)
    descript = models.CharField(max_length=200, blank=True)
    index = models.PositiveSmallIntegerField()
    """Id innerhalb der ProcDef"""
    
    #   REFACT: could/ should we replace index by a relation from ProcessDeff to
    # its first ProcessStep?
    actiontype = models.PositiveSmallIntegerField()
    """Etwa 'Entscheidung', 'Freigabe', 'Kalkulation' > Logik dahinter"""
    
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
    
    def json_data(self, an_instance):
        # FIXME: need to filter out only the values interesting for the current step
        return an_instance.procdata


@python_2_unicode_compatible
class StatusScheme(models.Model):
    """Alle Status des Prozesses, dazu deren moegliche Vorgaenger-Status"""
    
    # REFACT: could it be sensible to consider all steps prestep == NULL entry possible entry steps into the process?
    # Use case: process which can be started at many places - by different roles?
    
    process = models.ForeignKey('ProcessDef', null=True)
    
    # REFACT: consider requiring selfstep and prestep to be non null --dwt
    # REFACT: rename related_name to something more unique
    selfstep = models.ForeignKey(
        'ProcessStep', related_name='status_thisstep', null=True)
        
    # REFACT: rename related_name to something more unique
    prestep = models.ForeignKey(
        'ProcessStep', related_name='status_prestep' , null=True)
    # Erster Schritt: Prestep = Selfstep
    
    name   = models.CharField(max_length=20)
    remark = models.CharField(max_length=200, blank=True)
    
    logic  = models.CharField(max_length=200, blank=True)
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift
    #  und bei >1 moeglichen Folge-Steps den konkreten ermittelt

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
    # 0 (oder NULL): Show - 1: Editable - 2: Not-NULL forced
    editdefault = models.CharField(max_length=200, blank=True)
    # wird bei interaction>0 und leerem Feld eingesetzt
    #   Typ ist ggf. umzusetzen, z.B. text>integer
    order = models.PositiveSmallIntegerField(default=1)
    #   Abfolge des Felds im Formular. Evt. in 10er Stufen, 
    #     damit bei Umstellungen nicht alle order-s zu aendern sind.
    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('step', 'field_definition', )

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
    #   REFACT: consider to replace with real enum so that we can write the constructor as
    #     FieldDefinition(fieldType=FieldDefinition.STRING)
    fieldtype = models.PositiveSmallIntegerField()
    # Datentyp: 1-char, 2-int-number, 3-finance-number, 4-float-num, 5-Date,
    #	6-Datetime, 7 blob, 8-Enum (tbd)
    length = models.PositiveSmallIntegerField(default=1)
    # Length 1 bei Typen mit impliziter Laenge, etwa Date
    parent = models.ForeignKey('FieldDefinition', null=True, blank=True)
    # Field-Struktur ermoeglicht 1:n Datenbeziehungen auf Instanz-Ebene
    type = models.PositiveSmallIntegerField(default=1)
    # etwa 1-normal 2-pycess-intern 3-javascript-intern
    
    # REFACT: I think we need a way to order FieldDefinition --dwt

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

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProcInstance(models.Model):
    """Runtime Instances for a process"""
    
    process   = models.ForeignKey('ProcessDef', related_name="instances")
    
    # TODO: Need a way to merge in updates to this field
    # procdata= models.JSONdata() .. TODO
    procdata  = models.TextField(default='')
    currentstep = models.ForeignKey('ProcessStep', blank=True, null=True)
    starttime = models.DateTimeField()
    stoptime  = models.DateTimeField(null=True)
    status    = models.PositiveSmallIntegerField()
    # Status: 1-geplant 2-Vorbereitung 3-aktiv 4-postponed 5-deaktiv 6-abgeschlossen
    
    def __str__(self):
        return str(self.id)


@python_2_unicode_compatible
class RoleInstance(models.Model):
    """Roles assigned for a process instance"""
    
    role      = models.ForeignKey('RoleDef')
    procinst  = models.ForeignKey('ProcInstance', blank=True, null=True)
    # user  = models.ForeignKey(erweitertes Django User-Modell)
    entrytime = models.DateTimeField()
    exittime  = models.DateTimeField(null=True)
    
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
