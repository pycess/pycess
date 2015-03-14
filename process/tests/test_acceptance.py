# coding: utf-8
from __future__ import unicode_literals

from django.test import LiveServerTestCase

from django.contrib.auth.models import User
from process.models import *

from splinter import Browser
from pyexpect import expect
import json

class Monkey(object):
    def patch(self):
        import sys
        if not sys.platform.startswith('darwin'):
            return
        def find_firefox_path_anywhere_mac(self):
            from subprocess import check_output
            import os
            firefox_path = check_output(["mdfind", "kMDItemFSName = Firefox.app"]).decode('utf-8').strip()
            return os.path.join(firefox_path, "Contents/MacOS/firefox-bin")
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
        FirefoxBinary._get_firefox_start_cmd = find_firefox_path_anywhere_mac

class Smoke(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super(Smoke, cls).setUpClass()
        Monkey().patch()
        cls.browser = Browser()
    
    @classmethod
    def tearDownClass(cls):
        super(Smoke, cls).tearDownClass()
        cls.browser.quit()
    
    def test_smoke(self):
        self.browser.visit(self.live_server_url)
