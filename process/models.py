#coding: utf8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# pycess models - gem. Workshop 27 June 2013 
#   Version 0.12 - MIT Syntaxpruefung - OHNE Kardinalitaet 
#   Bernd Brincken - 12. Sept 2014 

## I - Prozess-Definition
@python_2_unicode_compatible
class ProcessDef(models.Model):
  name     = models.CharField(max_length=200)
  descript = models.CharField(max_length=200) 
  status   = models.PositiveSmallIntegerField()
    # etwa 1-geplant 2-Definitionsphase 3-nutzbar 4-aktiv 5-postponed 6-deaktiv
    # REFACT: add constants for status
  version  = models.PositiveSmallIntegerField()
    # von 1..2^16 hochgezaehlt für jede neue Version
  refering = models.ForeignKey('ProcessDef', null=True, blank=True)
    # optional: Verweis auf Vorgaenger-Version oder Vorlage (Templates, Kopien etc.)
  def __str__(self):
        return self.name
      
@python_2_unicode_compatible
class ProcessStep(models.Model):
	# Prozess-spezifischer Schritt, umfasst definierte Felder (FieldPerstep)
	#   kann wiederum mehrfach pro Process vorkommen > StatusScheme
	process		= models.ForeignKey('ProcessDef', null=True)
	role			= models.ForeignKey('RoleDef',    null=True)
	name			= models.CharField(max_length=200) 
	descript	= models.CharField(max_length=200) 
	index			= models.PositiveSmallIntegerField()
	# Id innerhalb der ProcDef
	# REFACT: could/ should we replace index by a relation from ProcessDeff to its first ProcessStep?
	actiontype = models.PositiveSmallIntegerField()
	# Etwa 'Entscheidung', 'Freigabe', 'Kalkulation' > Logik dahinter
	def __str__(self):
		return self.name
	
	def json_schema(self):
		return {
			'type':'object',
			'properties': dict(
				# REFACT: consider moving key generation into step
				('%s-%s' % (step.field.id, step.field.name), step.json_schema()) for  step in self.steps.all()
			)
		}
	

@python_2_unicode_compatible
class StatusScheme(models.Model):
  # Zulaessige Folge-Status fuer jeden Status > 1..n prestep-Nodes
  process  = models.ForeignKey('ProcessDef', null=True)  
  selfstep = models.ForeignKey('ProcessStep', related_name='selfstep', null=True)
  prestep  = models.ForeignKey('ProcessStep', related_name='prestep', null=True)
    # Erster Schritt: Prestep = Selfstep
  name     = models.CharField(max_length=20)
  remark   = models.CharField(max_length=200, blank=True)
  logic    = models.CharField(max_length=200, blank=True)
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift  
    #  und bei >1 moeglichen Folge-Steps den konkreten ermittelt 
  def __str__(self):
        return self.name  
  class Meta:
    unique_together = ('process', 'selfstep', 'prestep',)
    
@python_2_unicode_compatible
class FieldPerstep(models.Model):
	# Fields, die pro Schritt angezeigt/abgefragt werden
	step     = models.ForeignKey('ProcessStep', related_name='steps')
	field    = models.ForeignKey('FieldDef')
	interaction = models.PositiveSmallIntegerField(default=0)
	# 0 (oder NULL): Show - 1: Editable - 2: Not-NULL forced
	def __str__(self):
		return str(self.id)
	
	class Meta:
		unique_together = ('step', 'field', )
	
	def json_schema(self):
		return self.field.json_schema()
  
@python_2_unicode_compatible
class FieldDef(models.Model):
	process  = models.ForeignKey('ProcessDef', null=True)
	name     = models.CharField(max_length=200) 
	descript = models.CharField(max_length=200)
	fieldhelp  = models.CharField(max_length=200)
	# In einem Formular ggf. angezeigte ausfuehrlichere Erklaerung zur Bedeutung des Feldes
	# REFACT: consider to replace with real enum so that we can write the constructor as
	# FieldDef(fieldType=FieldDef.STRING)
	fieldtype  = models.PositiveSmallIntegerField()
	# Datentyp: 1-char, 2-int-number, 3-finance-number, 4-float-num, 5-Date, 
	#	6-Datetime, 7 blob, 8-Enum (tbd)
	length   = models.PositiveSmallIntegerField(default=1)
	# Lenght 1 bei Typen mit impliziter Laenge, etwa Date
	## editable & must per V 0.13 durch fieldPerstep.interaction ersetzt
	parent   = models.ForeignKey('FieldDef', null=True, blank=True)
	# Field-Struktur ermoeglicht 1:n Datenbeziehungen auf Instanz-Ebene
	type     = models.PositiveSmallIntegerField()
	# etwa 1-normal 2-pycess-intern 3-javascript-intern 
	def __str__(self):
		return self.name
	
	def json_schema(self):
		types = {
			1: 'string',
		}
		
		return {
			'type': types[self.type],
		}
        

@python_2_unicode_compatible
class RoleDef(models.Model):
  process  = models.ForeignKey('ProcessDef')
  name     = models.CharField(max_length=200) 
  descript = models.CharField(max_length=200)
  def __str__(self):
        return self.name  

## II - Prozess-Instanz
@python_2_unicode_compatible
class ProcInstance(models.Model):
  process     = models.ForeignKey('ProcessDef')
  currentstep = models.ForeignKey('ProcessStep', blank=True, null=True)
  starttime= models.DateTimeField()
  stoptime = models.DateTimeField()
  status   = models.PositiveSmallIntegerField()
    # etwa 1-geplant 2-Vorbereitung 3-aktiv 4-postponed 5-deaktiv 6-abgeschlossen
  def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class RoleInstance(models.Model):
  role      = models.ForeignKey('RoleDef')
  procinst  = models.ForeignKey('ProcInstance')
  # user = models.ForeignKey(erweitertes Django User-Modell)
  entrytime = models.DateTimeField()
  exittime  = models.DateTimeField()
  def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class PycLog(models.Model):
  time      = models.DateTimeField()
  action    = models.CharField(max_length=200)
  def __str__(self):
        return str(self.id)
  
# - Ende models.py V. 0.13 -