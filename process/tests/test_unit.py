# coding: utf-8
from __future__ import unicode_literals

from ..models import *

import json

from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from pyexpect import expect

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
        first_transition = ProcessStep.objects.create(name="Add_report")
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
        first_transition_error_description = FieldPerstep.objects.create(
            step=first_transition,
            field_definition=error_description,
            order=2,
        )
        first_transition_device_description = FieldPerstep.objects.create(
            step=first_transition,
            field_definition=device_description,
            order=1,
        )
        
        expect(first_transition_error_description.json_schema()).has_subdict(propertyOrder=2)
        expect(first_transition_device_description.json_schema()).has_subdict(propertyOrder=1)
        
        schema = first_transition.json_schema()
        expect(schema).has_subdict(
            properties=dict(
                error_description=first_transition_error_description.json_schema(),
                device_description=first_transition_device_description.json_schema(),
            ),
            defaultProperties=['error_description', 'device_description']
        )
    
    def test_should_have_process_step_metadata_on_form(self):
        first_transition = ProcessStep.objects.create(name="Add_report")
        
        expect(first_transition.json_schema()).has_subdict({
            'title': "Add_report",
            'type': 'object',
        })
    

class StateMachineTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.process = ProcessDefinition.objects.create(name='murksmeldung', status=0)
        
        cls.reporters = RoleDefinition.objects.create(name='reporters', process=cls.process)
        cls.publishers = RoleDefinition.objects.create(name='publishers', process=cls.process)
        
        cls.edit_data = ProcessStep.objects.create(name="edit_data", process=cls.process)
        
        cls.data_entered = Statuslist.objects.create(name="data_available", process=cls.process)
        
        # REFACT: consider allowing to mark status schemes as entry points directly
        # Really not sure if it's worth it, as there is alreaddy very little duplication --dwt
        # REFACT: consider to drop process reference in some of the objects, as we can also access it via a relation --dwt
        cls.start = StatusScheme.objects.create(name="start", 
            prestatus=None, status=cls.data_entered, process=cls.process, 
            role=cls.reporters, step=cls.edit_data)
        cls.edit_data_reporters = StatusScheme.objects.create(name="edit_data_reporters", 
            prestatus=cls.data_entered, status=cls.data_entered, 
            role=cls.publishers, step=cls.edit_data)
        cls.edit_data_publishers = StatusScheme.objects.create(name="edit_data_publishers", 
            prestatus=cls.data_entered, status=cls.data_entered, 
            role=cls.publishers, step=cls.edit_data)
        
        cls.published = Statuslist.objects.create(name="published", process=cls.process)
        
        cls.publish = StatusScheme.objects.create(name="publish", 
            prestatus=cls.data_entered, status=cls.published, 
            role=cls.publishers, step=cls.edit_data)
        
        cls.trashed = Statuslist.objects.create(name="trashed", process=cls.process)
        cls.trash = StatusScheme.objects.create(name="trash", 
            prestatus=cls.data_entered, status=cls.trashed, 
            role=cls.publishers, step=cls.edit_data)
        
    
    def setUp(self):
        self.reporter = User.objects.create(username='Joe User')
        self.publisher = User.objects.create(username='Jane Admin')
        self.report = self.process.create_instance(creator=self.reporter)
        self.report.add_user_for_role(self.publisher, self.publishers)
    
    def test_should_get_outgoing_transitions(self):
        transitions = self.data_entered.scheme_prestatus.all()
        expect(transitions).has_length(4)
        # Stupid django returns something array like, but that doesn't implement the __equals__  protocol.
        expect(transitions).to_contain(self.edit_data_reporters, self.edit_data_publishers, self.publish, self.trash)
    
    def test_should_transition_to_valid_states(self):
        instance = self.process.create_instance(creator=self.reporter)
        expect(instance.currentstatus) == self.data_entered
        instance.transition_with_status(self.publish)
        expect(instance.currentstatus) == self.published
    
    def test_should_only_transition_to_valid_states(self):
        instance = self.process.create_instance(creator=self.reporter)
        instance.currentstatus = self.trashed
        
        expect(lambda: instance.transition_with_status(self.publish)) \
            .to_raise(AssertionError, r"Invalid transition")
    
    def test_should_add_role_instance_with_self_if_neccessary_on_instance_creation(self):
        RoleInstance.objects.filter(pycuser=self.reporter).delete()
        expect(RoleInstance.objects.filter(pycuser=self.reporter).count()) == 0
        instance = self.process.create_instance(creator=self.reporter)
        expect(RoleInstance.objects.filter(pycuser=self.reporter).count()) == 1
        # doesn't create a second one
        instance = self.process.create_instance(creator=self.reporter)
        expect(RoleInstance.objects.filter(pycuser=self.reporter).count()) == 1
    
    def test_should_know_if_current_status_is_editable_for_user(self):
        RoleInstance.objects.filter(pycuser=self.reporter).delete()
        expect(RoleInstance.objects.filter(pycuser=self.reporter).exists()).is_false()
        instance = self.process.create_instance(creator=self.reporter)
        expect(RoleInstance.objects.filter(pycuser=self.reporter).exists()).is_true()

