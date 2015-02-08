#coding: utf8
from django.db import models

# pycess models - gem. Workshop 27 June 2013 
#   Version 0.12 - MIT Syntaxpruefung - OHNE Kardinalitaet 
#   Bernd Brincken - 12. Sept 2014 

## I - Prozess-Definition 
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
  def __unicode__(self):
        return self.name
      
class ProcessStep(models.Model):
  # Prozess-spezifischer Schritt, umfasst definierte Felder (FieldPerstep)
  #   kann wiederum mehrfach pro Process vorkommen > StatusScheme
  process  = models.ForeignKey('ProcessDef', null=True)
  role	   = models.ForeignKey('RoleDef',    null=True)
  name     = models.CharField(max_length=200) 
  descript = models.CharField(max_length=200) 
  index    = models.PositiveSmallIntegerField()
    # Id innerhalb der ProcDef
  actiontype = models.PositiveSmallIntegerField()
    # Etwa 'Entscheidung', 'Freigabe', 'Kalkulation' > Logik dahinter
  def __unicode__(self):
        return self.name  

class StatusScheme(models.Model):
  # Zulaessige Folge-Status fuer jeden Status > 1..n prestep-Nodes
  process  = models.ForeignKey('ProcessDef', null=True)  
  selfstep = models.ForeignKey('ProcessStep', related_name='selfstep')
  prestep  = models.ForeignKey('ProcessStep', related_name='prestep')
    # Erster Schritt: Prestep = Selfstep
  name     = models.CharField(max_length=20)
  remark   = models.CharField(max_length=200, blank=True)
  logic    = models.CharField(max_length=200, blank=True)
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift  
    #  und bei >1 moeglichen Folge-Steps den konkreten ermittelt 
  def __unicode__(self):
        return self.name  
  class Meta:
    unique_together = ('process', 'selfstep', 'prestep',)
    
class FieldPerstep(models.Model):
  # Fields, die pro Schritt angezeigt/abgefragt werden
  step     = models.ForeignKey('ProcessStep')
  field    = models.ForeignKey('FieldDef')
  interaction = models.PositiveSmallIntegerField(default=0)
    # 0 (oder NULL): Show - 1: Editable - 2: Not-NULL forced
  def __unicode__(self):
        return unicode(self.id)
  class Meta:
    unique_together = ('step', 'field', )
  
class FieldDef(models.Model):
  process  = models.ForeignKey('ProcessDef', null=True)
  name     = models.CharField(max_length=200) 
  descript = models.CharField(max_length=200)
  fieldhelp  = models.CharField(max_length=200)
    # In einem Formular ggf. angezeigte ausfuehrlichere Erklaerung zur Bedeutung des Feldes
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
  def __unicode__(self):
        return self.name  

class RoleDef(models.Model):
  process  = models.ForeignKey('ProcessDef')
  name     = models.CharField(max_length=200) 
  descript = models.CharField(max_length=200)
  def __unicode__(self):
        return self.name  

## II - Prozess-Instanz 
class ProcInstance(models.Model):
  process  = models.ForeignKey('ProcessDef')
  starttime= models.DateTimeField()
  stoptime = models.DateTimeField()
  status   = models.PositiveSmallIntegerField()
    # etwa 1-geplant 2-Vorbereitung 3-aktiv 4-postponed 5-deaktiv 6-abgeschlossen
  def __unicode__(self):
        return unicode(self.id)

class RoleInstance(models.Model):
  role      = models.ForeignKey('RoleDef')
  procinst  = models.ForeignKey('ProcInstance')
  # user = models.ForeignKey(erweitertes Django User-Modell)
  entrytime = models.DateTimeField()
  exittime  = models.DateTimeField()
  def __unicode__(self):
        return unicode(self.id)

class PycLog(models.Model):
  time      = models.DateTimeField()
  action    = models.CharField(max_length=200)
  def __unicode__(self):
        return unicode(self.id)
  
# - Ende models.py V. 0.13 -