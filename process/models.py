from django.db import models

# pycess models - gem. Workshop 27 June 2013 
#   Version 0.1 - ohne Syntaxpruefung und Kardinalität 
#   Bernd Brincken - 12. Sept 2014 

## I - Prozess-Definition 
class ProcessDef(models.Model):
  name     = models.Charfield() 
  descript = models.Charfield() 
  status   = models.PositiveSmallIntegerField()
    # etwa 1-geplant 2-Definitionsphase 3-nutzbar 4-aktiv 5-postponed 6-deaktiv
  version  = models.PositiveSmallIntegerField()
    # von 1..2^16 hochgezählt für jede neue Version
  refering = models.ForeignKey('ProcessDef')
    # optional: Verweis auf Vorgänger-Version oder Vorlage (Templates, Kopien etc.)

class ProcessStep(models.Model):
  # Prozess-spezifischer Schritt, umfasst definierte Felder (FieldPerstep)
  #   kann wiederum mehrfach pro Process vorkommen > StepScheme
  name     = models.Charfield() 
  descript = models.Charfield() 
  index    = models.PositiveSmallIntegerField()
    # Id innerhalb der ProcDef
  actiontype = models.PositiveSmallIntegerField()
    # Etwa 'Entscheidung', 'Freigabe', 'Kalkulation' > Logik dahinter
  process  = models.ForeignKey('ProcessDef')
  
class StepScheme(models.Model):
  # Zulässige Folge-Steps für jeden Step > 1..n prestep-Nodes
  selfstep = models.ForeignKey('ProcessStep')
  prestep  = models.ForeignKey('ProcessStep')
  remark   = models.Charfield()
  logic    = models.Charfield()
    # Kann etwa eine Makrosprache halten, die auf Prozess-Variablen zugreift  
    #  und bei >1 möglichen Folge-Steps den konkreten ermittelt 
    
class FieldPerstep(models.Model):
  # Fields, die pro Schritt angezeigt/abgefragt werden
  step     = models.ForeignKey('ProcessStep')
  field    = models.ForeignKey('FieldDef')

class FieldDef(models.Model):
  name     = models.Charfield() 
  descript = models.Charfield()
  fldhelp  = models.Charfield()
    # In einem Formular ggf. angezeigte ausführlichere Erklärung zur Bedeutung des Feldes
  fldtype  = models.PositiveSmallIntegerField()
    # Datentyp (ggf. Enum ..)
  length   = models.PositiveSmallIntegerField()
  editable = models.NullBooleanField()
    # false > nur Anzeige 
  must 	   = models.NullBooleanField()
    # Bei 'editable' wird Inhalt=not-NULL erzwungen 
  parent   = models.ForeignKey('FieldDef')
    # Field-Struktur ermöglicht 1:n Datenbeziehungen auf Instanz-Ebene
  type     = models.PositiveSmallIntegerField()
    # etwa 1-normal 2-pycess-intern 3-javascript-intern 

class RoleDef(models.Model):
  name     = models.Charfield() 
  descript = models.Charfield()
  process  = models.ForeignKey('ProcessDef')

## II - Prozess-Instanz 
class ProcInstance(models.Model):
  process  = models.ForeignKey('ProcessDef')
  starttime= models.DateTimeField()
  stoptime = models.DateTimeField()
  status   = models.PositiveSmallIntegerField()
    # etwa 1-geplant 2-Vorbereitung 3-aktiv 4-postponed 5-deaktiv 6-abgeschlossen

class RoleInstance(models.Model):
  role      = models.ForeignKey('RoleDef')
  procinst  = models.ForeignKey('ProcInstance')
  # user = models.ForeignKey(erweitertes Django User-Modell)
  entrytime = models.DateTimeField()
  exittime  = models.DateTimeField()

class PycLog(models.Model):
  time      = models.DateTimeField()
  action    = models.Charfield()
  
# - Ende models.py V. 0.1 -