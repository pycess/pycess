# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase

from process.models import *
from pyexpect import expect


class FirstProcess(TestCase):
    
    def setUp(self):
        super(FirstProcess, self).setUp()
        self._create_murksmeldung()
    
    def _create_murksmeldung(self):
        self.murksmeldung = ProcessDef.objects.create(
            name="Murksmeldung",
            descript="Meldungen über Geräte an denen geplante Obsoleszenz sichtbar wird.",
            status=0,
            version=1,
            # REFACT: consider to move first step into a relation on this
        )
        self.first_step = ProcessStep.objects.create(
            name="Erstmeldung",
            descript="Jemand meldet sich mit einer Fehlermeldung",
            actiontype=0,
            index=1,  # first step
            process=self.murksmeldung,
        )
        self.initial_status = StatusScheme.objects.create(
            remark="Initialer Zustand",
            name='Init',
            selfstep=self.first_step,
        )
        self.data_provider = RoleDef.objects.create(
            name="Murksmelder",
            descript="Meldet einen Murks.",
            process=self.murksmeldung,
        )
        self.data_processor = RoleDef.objects.create(
            name="Redaktör",
            descript="Nimmt Murksmeldungen entgegen, bearbeitet diese und entscheidet ob Sie veröffentlicht werden sollen.",
            process=self.murksmeldung,
        )
        self.decision = ProcessStep.objects.create(
            name="Veröffentlichungsentscheidung",
            descript="Der Redaktör entscheidet was mit der Meldung passieren soll.",
            actiontype=0,
            index=1,
            process=self.murksmeldung,
        )
        self.enter_data = StatusScheme.objects.create(
            name="Daten eingegeben",
            prestep=self.first_step,
            selfstep=self.decision,
        )
        self.published = ProcessStep.objects.create(
            name="Daten veröffentlicht",
            descript="Murksmeldung Veröffentlicht",
            actiontype=0,
            index=2,
            process=self.murksmeldung,
        )
        self.publish = StatusScheme.objects.create(
            name='Veröffentlichen',
            remark="Murksmeldung veröffentlichen",
            prestep=self.decision,
            selfstep=self.published,
        )
        self.trashed = ProcessStep.objects.create(
            name="Abgelehnt / Verworfen",
            descript="Murksmeldung verworfen",
            actiontype=0,
            index=3,
            process=self.murksmeldung,
        )
        self.thrash = StatusScheme.objects.create(
            name='Verwerfen',
            remark="Murksmeldung verwerfen",
            prestep=self.decision,
            selfstep=self.trashed,
        )
        
        self.device_description = FieldDefinition.objects.create(
            name='device_description',
            descript="Gerätebeschreibung",
            fieldhelp="Typennummern, Hersteller, alles was man braucht",
            fieldtype=1,
            type=1,
        )
        self.error_description = FieldDefinition.objects.create(
            name='error_description',
            descript="Murksbeschreibung",
            fieldhelp="Ausführliche beschreibung was defekt ist und wieso das ein Murks ist.",
            fieldtype=1,
            type=1,
        )
        FieldPerstep.objects.create(
            step=self.first_step, 
            field_definition=self.device_description, 
            interaction=2
        )
        FieldPerstep.objects.create(
            step=self.first_step, 
            field_definition=self.error_description, 
            interaction=2
        )
        
        FieldPerstep.objects.create(
            step=self.decision, 
            field_definition=self.device_description, 
            interaction=1
        )
        FieldPerstep.objects.create(
            step=self.decision, 
            field_definition=self.error_description, 
            interaction=1
        )
        return self.murksmeldung
    
    def test_should_know_format_of_fields(self):
        expect(self.device_description.json_schema()) == {
            'title': 'Gerätebeschreibung',
            'type': 'string',
            'format': 'textarea',
        }
        
        expect(self.error_description.json_schema()) == {
            'title': 'Murksbeschreibung',
            'type': 'string',
            'format': 'textarea',
        }
    
    def test_should_know_fields_in_process_step(self):
        schema = self.first_step.json_schema()
        expect(schema).has_subdict(
            properties=dict(
                error_description=self.error_description.json_schema(),
                device_description=self.device_description.json_schema(),
            ),
            defaultProperties=['device_description', 'error_description']
        )
    
    def test_should_sort_fields(self):
        expect(self.device_description.json_schema()) == {
            'title': 'Gerätebeschreibung',
            'type': 'string',
            'format': 'textarea',
        }
        
        expect(self.error_description.json_schema()) == {
            'title': 'Murksbeschreibung',
            'type': 'string',
            'format': 'textarea',
        }
    
    def test_should_have_process_step_metadata_on_form(self):
        expect(self.first_step.json_schema()).has_subdict({
            'title': "Erstmeldung",
            'type': 'object',
        })
    
