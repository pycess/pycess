# coding: utf-8
from __future__ import unicode_literals

from ..models import *

import json

from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from pyexpect import expect
import sys
is_python2 = sys.version_info.major < 3

# TODO: understand how to do integration tests with django testing - or if it is better to switch to something specialized like rspec
class UnicodeHanldingTest(TestCase):
    def test_str_is_annotated_in_python2(self):
        expect(ProcessDefinition).has_attr('__str__')
        if is_python2:
            expect(ProcessDefinition).has_attr('__unicode__')
    

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
        super(StateMachineTests, cls).setUpClass()
        
        cls.process = ProcessDefinition.objects.create(name='murksmeldung', status=0)
        
        cls.reporters = RoleDefinition.objects.create(name='reporters', process=cls.process, is_self_assignable=True)
        cls.publishers = RoleDefinition.objects.create(name='publishers', process=cls.process)
        
        cls.edit_data = ProcessStep.objects.create(name="edit_data", process=cls.process)
        
        cls.enter_data = Status.objects.create(name="enter_data", process=cls.process, step=cls.edit_data, role=cls.reporters)
        cls.decide = Status.objects.create(name="decide", process=cls.process, step=cls.edit_data, role=cls.publishers)
        
        # REFACT: consider to drop process reference in some of the objects, as we can also access it via a relation --dwt
        cls.start = StatusTransition.objects.create(name="start", prestatus=None, status=cls.enter_data, process=cls.process)
        cls.ask_for_approval = StatusTransition.objects.create(name="ask_for_approval", prestatus=cls.enter_data, status=cls.decide)
        cls.ask_for_more_data = StatusTransition.objects.create(name="ask_for_more_data", prestatus=cls.decide, status=cls.enter_data)
        
        cls.published = Status.objects.create(name="published", process=cls.process, role=cls.publishers, step=cls.edit_data)
        
        cls.publish = StatusTransition.objects.create(name="publish", prestatus=cls.decide, status=cls.published)
        
        cls.trashed = Status.objects.create(name="trashed", process=cls.process, role=cls.publishers, step=cls.edit_data)
        cls.trash = StatusTransition.objects.create(name="trash", prestatus=cls.decide, status=cls.trashed)
        
    
    def setUp(self):
        super(StateMachineTests, self).setUp()
        
        self.reporter = User.objects.create(username='Joe User')
        self.publisher = User.objects.create(username='Jane Admin')
        self.report = self.process.create_instance(creator=self.reporter)
        self.report.add_user_for_role(self.publisher, self.publishers)
    
    def test_should_get_outgoing_transitions(self):
        transitions = self.decide.scheme_prestatus.all()
        expect(transitions).has_length(3)
        # Stupid django returns something array like, but that doesn't implement the __equals__  protocol.
        expect(transitions).to_contain(self.ask_for_more_data, self.publish, self.trash)
    
    def test_should_transition_to_valid_states(self):
        instance = self.process.create_instance(creator=self.reporter)
        expect(instance.currentstatus) == self.enter_data
        instance.transition_with_status(self.ask_for_approval)
        expect(instance.currentstatus) == self.decide
    
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
    

class SelfAssignedRolesTest(TestCase):
    
    def setUp(self):
        self.process = ProcessDefinition.objects.create(name='process', status=StatusChoices.IN_DEVELOPMENT)
        self.starter = RoleDefinition.objects.create(name='starter', process=self.process, is_self_assignable=True)
        self.edit = ProcessStep.objects.create(name='edit', process=self.process)
        self.started = Status.objects.create(name='started', process=self.process, role=self.starter, step=self.edit)
        self.start = StatusTransition.objects.create(name='start', process=self.process, prestatus=None, status=self.started)
    
    def test_should_know_if_anyone_can_start_the_process(self):
        expect(self.process.is_startable_by_anyone()).is_true()
        
        self.starter.is_self_assignable = False
        self.starter.save()
        expect(self.process.is_startable_by_anyone()).is_false()
    
    def test_should_assign_role_to_user_when_he_starts_the_process(self):
        creator = User.objects.create()
        instance = self.process.create_instance(creator=creator)
        expect(instance.currentstatus.role.role_instance.filter(pycuser=creator).exists()).is_true()
    
    def test_should_raise_if_user_tries_to_start_process_in_role_which_is_not_self_assignable(self):
        self.starter.is_self_assignable = False
        self.starter.save()
        
        creator = User.objects.create()
        from django.core.exceptions import PermissionDenied
        expect(lambda: self.process.create_instance(creator=creator)).to_raise(PermissionDenied)
    
    def test_should_know_if_specific_user_can_start_process(self):
        prospective_creator = User.objects.create()
        expect(self.process.is_startable_by_user(prospective_creator)).is_true()
        
        self.starter.is_self_assignable = False
        self.starter.save()
        expect(self.process.is_startable_by_user(prospective_creator)).is_false()
    
    def test_should_not_explode_if_process_cannot_be_started_at_all(self):
        # should only happen for unfinished processes
        self.start.delete()
        prospective_creator = User.objects.create()
        expect(self.process.is_startable_by_user(prospective_creator)).is_false()

