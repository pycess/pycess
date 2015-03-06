# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone

from process.models import *
from pyexpect import expect
import json

# TODO: understand how to do integration tests with django testing - or if it is better to switch to something specialized like rspec

class FirstProcess(TestCase):
    
    def setUp(self):
        super(FirstProcess, self).setUp()
        self._create_murksmeldung()
    
    def _create_murksmeldung(self):
        # REFACT: investigate how django default data works, some json / yaml file perhaps?
        # Would be very usefull if this can be preloaded into the gui easily as play data
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
            prestep=self.first_step,
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
        self.trash = StatusScheme.objects.create(
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
        self.first_step_device_description = FieldPerstep.objects.create(
            step=self.first_step, 
            field_definition=self.device_description, 
            order=1,
            interaction=2,
        )
        self.first_step_error_description = FieldPerstep.objects.create(
            step=self.first_step, 
            field_definition=self.error_description, 
            order=2,
            interaction=2,
        )
        
        FieldPerstep.objects.create(
            step=self.decision, 
            field_definition=self.device_description, 
            order=1,
            interaction=1,
        )
        FieldPerstep.objects.create(
            step=self.decision, 
            field_definition=self.error_description, 
            order=2,
            interaction=1,
        )
        
        self.instance = ProcInstance.objects.create(
            process=self.murksmeldung,
            currentstep=self.murksmeldung.first_step(),
            procdata=json.dumps({}), # FIXME: set initial data from somewhere
            starttime=timezone.now(),
            stoptime=timezone.now(),
            status=3)
    
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
                error_description=self.first_step_error_description.json_schema(),
                device_description=self.first_step_device_description.json_schema(),
            ),
            defaultProperties=['device_description', 'error_description']
        )
    
    def test_should_sort_fields(self):
        schema = self.first_step.json_schema()
        device_description = self.first_step_device_description.json_schema()
        error_description = self.first_step_error_description.json_schema()
        expect(device_description) == {
            'title': 'Gerätebeschreibung',
            'type': 'string',
            'format': 'textarea',
            'propertyOrder': 1,
        }
        
        expect(error_description) == {
            'title': 'Murksbeschreibung',
            'type': 'string',
            'format': 'textarea',
            'propertyOrder': 2
        }
    
    def test_should_have_process_step_metadata_on_form(self):
        expect(self.first_step.json_schema()).has_subdict({
            'title': "Erstmeldung",
            'type': 'object',
        })
    
    def test_get_outgoing_transitions(self):
        transitions = self.decision.possible_transitions()
        expect(transitions).has_length(2)
        # Stupid django returns something array like, but that doesn't implement the __equals__ protocol.
        expect(transitions).to_contain(self.publish, self.trash)
    
    def test_should_transition_to_valid_states(self):
        self.instance.transition_with_status(self.enter_data)
        expect(self.instance.currentstep) == self.decision
    
    def test_should_fail_when_transitioning_to_invalid_states(self):
        expect(lambda: self.instance.transition_with_status(self.publish)) \
            .to_raise(AssertionError, r"Invalid transition")
    
