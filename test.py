#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""SQF Minifier tests."""
import unittest
from unittest import TestCase

from sqf.analyzer import analyze, Analyzer
from sqf.exceptions import SQFWarning
from sqf.parser import parse
from minify import minify_file

TEST_FILE = 'test.sqf'

def test(code, status='success'):
    if len(code) < 255 and ('/' in code or '\\' in code):
        try:
            with open(code) as f:
                code = f.read()
        except FileNotFoundError:
            pass

    analyzer = Analyzer()
    analyze(parse(code), analyzer)

    errors = [e for e in analyzer.exceptions if not isinstance(e, SQFWarning)]
    stat_out = 'fail' if errors else 'success'

    return status == stat_out

test_files = {TEST_FILE: 'success'}

class TestMinifier(TestCase):

    def test_demo_files(self):
        for file, status in test_files.items():
            with open(file) as f:
                code = f.read()
            self.assertTrue(test(code, status))
            minified = minify_file(file)
            self.assertTrue(test(minified, status))