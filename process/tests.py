# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone

from process.models import *
from pyexpect import expect
import json

# TODO: understand how to do integration tests with django testing - or if it is better to switch to something specialized like rspec

class JSONSchemaTests(TestCase):
    
    def test_should_know_type_and_title_of_fields(self):
        device_description = FieldDefinition.objects.create(
            descript="Model Code",
            fieldtype=1,
        )
        
        expect(device_description.json_schema()) == {
            'title': 'Model Code',
            'type': 'string',
            'format': 'textarea',
        }
        
        error_description = FieldDefinition.objects.create(
            descript="Failure or error description",
            fieldtype=1,
        )
        expect(error_description.json_schema()) == {
            'title': 'Failure or error description',
            'type': 'string',
            'format': 'textarea',
        }
        
    def test_should_respect_ordering_of_fields(self):
        first_step = ProcessStep.objects.create(name="Add_report")
        error_description = FieldDefinition.objects.create(
            name='error_description',
            descript="Failure or error description",
            fieldtype=1,
        )
        device_description = FieldDefinition.objects.create(
            name='device_description',
            descript="Model Code",
            fieldtype=1,
        )
        first_step_error_description = FieldPerstep.objects.create(
            step=first_step,
            field_definition=error_description,
            order=2,
        )
        first_step_device_description = FieldPerstep.objects.create(
            step=first_step,
            field_definition=device_description,
            order=1,
        )
        
        expect(first_step_error_description.json_schema()).has_subdict(propertyOrder=2)
        expect(first_step_device_description.json_schema()).has_subdict(propertyOrder=1)
        
        schema = first_step.json_schema()
        expect(schema).has_subdict(
            properties=dict(
                error_description=first_step_error_description.json_schema(),
                device_description=first_step_device_description.json_schema(),
            ),
            defaultProperties=['error_description', 'device_description']
        )
    
    def test_should_have_process_step_metadata_on_form(self):
        first_step = ProcessStep.objects.create(name="Add_report")
        
        expect(first_step.json_schema()).has_subdict({
            'title': "Add_report",
            'type': 'object',
        })
    

class StateMachineTests(TestCase):
    
    def setUp(self):
        self.process = ProcessDef.objects.create(name='Murksmeldung', status=0)
        
        self.decision = ProcessStep.objects.create(name="decision", process=self.process)
        self.published = ProcessStep.objects.create(name="published")
        self.trashed = ProcessStep.objects.create(name="trashed", index=0, actiontype=0,)
        
        self.start = StatusScheme.objects.create(name="start", prestep=None, selfstep=self.decision)
        self.publish = StatusScheme.objects.create(name="publish", prestep=self.decision, selfstep=self.published)
        self.trash = StatusScheme.objects.create(name="trash", prestep=self.decision, selfstep=self.trashed)
        # Distractor
        self.correct_error = StatusScheme.objects.create(name="correct_error", prestep=self.published, selfstep=self.trashed)
    
    def test_should_get_outgoing_transitions(self):
        transitions = self.decision.possible_transitions()
        expect(transitions).has_length(2)
        # Stupid django returns something array like, but that doesn't implement the __equals__  protocol.
        expect(transitions).to_contain(self.publish, self.trash)
    
    def test_should_transition_to_valid_states(self):
        instance = self.process.create_instance()
        instance.currentstep = self.decision
        instance.transition_with_status(self.publish)
        expect(instance.currentstep) == self.published
    
    def test_should_only_transitioning_valid_states(self):
        instance = self.process.create_instance()
        instance.currentstep = self.trashed
        
        expect(lambda: instance.transition_with_status(self.publish)) \
            .to_raise(AssertionError, r"Invalid transition")
    

