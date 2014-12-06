# coding: utf-8

from django.test import TestCase

from process.models import *

class FirstProcess(TestCase):
    
    def _create_murksmeldung(self):
        murksmeldung = ProcessDef(
            name="Murksmeldung",
            descript="Meldungen über Geräte an denen geplante Obsoleszenz sichtbar wird.",
            status=0,
        )
        first_step = ProcessStep(
            name="Erstmeldung",
            descript="Jemand meldet sich mit einer Fehlermeldung",
            # actiontype=?, #
            index=1, # first step
            process=murksmeldung,
        )
        initial_status = StatusScheme(
            name="Initialer Zustand",
            selfstep=first_step,
        )
        data_provider = RoleDef(
            name="Murksmelder",
            descript="Meldet einen Murks.",
            process=murksmeldung,
        )
        data_processor = RoleDef(
            name="Redaktör",
            descript="Nimmt Murksmeldungen entgegen, bearbeitet diese und entscheidet ob Sie veröffentlicht werden sollen.",
            process=murksmeldung,
        )
        decision = ProcessStep(
            name="Veröffentlichungsentscheidung",
            descript="Der Redaktör entscheidet was mit der Meldung passieren soll.",
            process=murksmeldung,
        )
        data_entered = StatusScheme(
            name="Daten eingegeben",
            prestep=first_step,
            selfstep=decision,
        )
        data_published = StatusScheme(
            name="Murksmeldung veröffentlicht",
            prestep=decision,
        )
        trashed = StatusScheme(
            name="Murksmeldung verworfen",
            prestep=decision,
        )
        
        device_description = FieldDef(
            name="Gerätebeschreibung",
            descript="Typennummern, Hersteller, alles was man braucht",
            editable=True,
            must=True,
            type=1,
        )
        error_description = FieldDef(
            name="Murksbeschreibung",
            descript="Ausführliche beschreibung was defekt ist und wieso das ein Murks ist.",
            editable=True,
            must=True,
            type=1,
        )
        FieldPerstep(step=first_step, field=device_description)
        FieldPerstep(step=first_step, field=error_description)
        
        FieldPerstep(step=decision, field=device_description)
        FieldPerstep(step=decision, field=error_description)
        
    
    def test_can_define_murksmeldung(self):
        self._create_murksmeldung()