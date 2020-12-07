import os
import unittest
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Dungeon, Monster


class DungeonMonstersTestCase(unittest.TestCase):
    """This class represents the DM test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # binds the app to the current context
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
