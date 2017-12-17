#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tsk_mgr` package."""

import uuid
import unittest
import mock

from tsk_mgr import tsk_mgr


class TestTask(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize things before ALL tests in this class get executed
        pass

    def setUp(self):
        # use a new manager in each test (just for the sake of example, TBH)
        self.manager = tsk_mgr.Manager()

    def tearDown(self):
        # remove every persisted item after each test
        self.manager.persistence.clear()

    @classmethod
    def tearDownClass(cls):
        # Clean up after ALL tests in this class got executed
        pass

    def test_create_minimal(self):
        t = self.manager.create("title1")
        self.assertEqual("title1", t.title)
        self.assertIsInstance(t.id, uuid.UUID)  # new in Python 2.7

    def test_list(self):
        t = self.manager.create("title2")
        tasks = self.manager.list_tasks()
        self.assertEqual(1, len(tasks))
        self.assertIn(t, tasks, "The new task should be in the list")

    @mock.patch.object(tsk_mgr.Persistence, 'update', return_value=True)
    def test_update(self, mock_update):
        t = self.manager.create("title3")
        t.title = "new title"
        is_updated = self.manager.update(t)
        self.assertTrue(is_updated)
        mock_update.assert_called_once_with(t)

    @unittest.skip("This test itself is somehow wrong. Skip it for now.")
    def test_list_negative(self):
        self.manager.create("title3")
        self.assertEqual(11, len(self.manager.list_tasks()))
