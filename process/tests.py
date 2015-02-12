# coding: utf-8

from django.test import TestCase

from process.models import *
from pyexpect import expect

class FirstProcess(TestCase):
    
    def _create_murksmeldung(self):
        self.murksmeldung = ProcessDef(
            name="Murksmeldung",
            descript="Meldungen über Geräte an denen geplante Obsoleszenz sichtbar wird.",
            status=0,
        )
        self.first_step = ProcessStep(
            name="Erstmeldung",
            descript="Jemand meldet sich mit einer Fehlermeldung",
            # actiontype=?, #
            index=1, # first step
            process=self.murksmeldung,
        )
        self.initial_status = StatusScheme(
            name="Initialer Zustand",
            selfstep=self.first_step,
        )
        self.data_provider = RoleDef(
            name="Murksmelder",
            descript="Meldet einen Murks.",
            process=self.murksmeldung,
        )
        self.data_processor = RoleDef(
            name="Redaktör",
            descript="Nimmt Murksmeldungen entgegen, bearbeitet diese und entscheidet ob Sie veröffentlicht werden sollen.",
            process=self.murksmeldung,
        )
        self.decision = ProcessStep(
            name="Veröffentlichungsentscheidung",
            descript="Der Redaktör entscheidet was mit der Meldung passieren soll.",
            process=self.murksmeldung,
        )
        self.data_entered = StatusScheme(
            name="Daten eingegeben",
            prestep=self.first_step,
            selfstep=self.decision,
        )
        self.data_published = StatusScheme(
            name="Murksmeldung veröffentlicht",
            prestep=self.decision,
        )
        self.trashed = StatusScheme(
            name="Murksmeldung verworfen",
            prestep=self.decision,
        )
        
        self.device_description = FieldDef(
            name="Gerätebeschreibung",
            descript="Typennummern, Hersteller, alles was man braucht",
            editable=True,
            must=True,
            type=1,
        )
        self.error_description = FieldDef(
            name="Murksbeschreibung",
            descript="Ausführliche beschreibung was defekt ist und wieso das ein Murks ist.",
            editable=True,
            must=True,
            type=1,
        )
        FieldPerstep(step=self.first_step, field=self.device_description)
        FieldPerstep(step=self.first_step, field=self.error_description)
        
        FieldPerstep(step=self.decision, field=self.device_description)
        FieldPerstep(step=self.decision, field=self.error_description)
        
    
    def test_can_define_murksmeldung(self):
        self._create_murksmeldung()
    
    def test_serialize_form_to_json(self):
        form_json = self.data_entered.form_json()
        expect(form_json.)
    
