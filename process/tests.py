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
            version=1,
            # REFACT: consider to move first step into a relation on this
        )
        self.murksmeldung.save()
        self.first_step = ProcessStep(
            name="Erstmeldung",
            descript="Jemand meldet sich mit einer Fehlermeldung",
            actiontype=0,
            index=1, # first step
            process=self.murksmeldung,
        )
        self.first_step.save()
        self.initial_status = StatusScheme(
            remark="Initialer Zustand",
            name='Init',
            selfstep=self.first_step,
        )
        self.initial_status.save()
        self.data_provider = RoleDef(
            name="Murksmelder",
            descript="Meldet einen Murks.",
            process=self.murksmeldung,
        )
        self.data_provider.save()
        self.data_processor = RoleDef(
            name="Redaktör",
            descript="Nimmt Murksmeldungen entgegen, bearbeitet diese und entscheidet ob Sie veröffentlicht werden sollen.",
            process=self.murksmeldung,
        )
        self.data_processor.save()
        self.decision = ProcessStep(
            name="Veröffentlichungsentscheidung",
            descript="Der Redaktör entscheidet was mit der Meldung passieren soll.",
            actiontype=0,
            index=1,
            process=self.murksmeldung,
        )
        self.decision.save()
        self.data_entered = StatusScheme(
            name="Daten eingegeben",
            prestep=self.first_step,
            selfstep=self.decision,
        )
        self.data_entered.save()
        self.data_published = StatusScheme(
            name='Report_Published',
            remark="Murksmeldung veröffentlicht",
            prestep=self.decision,
        )
        self.data_published.save()
        self.trashed = StatusScheme(
            name='Declined',
            remark="Murksmeldung verworfen",
            prestep=self.decision,
        )
        self.trashed.save()
        
        self.device_description = FieldDef(
            name='device_description',
            descript="Gerätebeschreibung",
            fieldhelp="Typennummern, Hersteller, alles was man braucht",
            fieldtype=1,
            type=1,
        )
        self.device_description.save()
        self.error_description = FieldDef(
            name='error_description',
            descript="Murksbeschreibung",
            fieldhelp="Ausführliche beschreibung was defekt ist und wieso das ein Murks ist.",
            fieldtype=1,
            type=1,
        )
        self.error_description.save()
        FieldPerstep(step=self.first_step, field=self.device_description, interaction=2).save()
        FieldPerstep(step=self.first_step, field=self.error_description, interaction=2).save()
        
        FieldPerstep(step=self.decision, field=self.device_description, interaction=1).save()
        FieldPerstep(step=self.decision, field=self.error_description, interaction=1).save()
        return self.murksmeldung
    
    def test_can_define_murksmeldung(self):
        self._create_murksmeldung()
    
    def test_serialize_step_to_json_form_schema(self):
        self._create_murksmeldung()
        expect(self.device_description.json_schema()) == {
            'type': 'string',
            'format': 'textarea',
        }
        
        expect(self.error_description.json_schema()) == {
            'type': 'string',
            'format': 'textarea',
        }
        
        expect(self.first_step.json_schema()) == {
            'type': 'object',
            'properties': {
                'Gerätebeschreibung': {
                    'type': 'string',
                    'format': 'textarea',
                },
                'Murksbeschreibung': {
                    'type': 'string',
                    'format': 'textarea',
                },
            },
        }
        
    
        
