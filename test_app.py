from database import db, setup_db
import os
import json
import unittest
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Dungeon, Monster


class DungeonMonstersTestCase(unittest.TestCase):
    """This class represents the DM test case"""

    @classmethod
    def setUp(self):
        """Define test variables and initialize app."""
        # binds the app to the current context
        self.app = create_app()
        setup_db(self.app)
        self.client = self.app.test_client
        self.headers = {"Authorization": "bearer " + os.environ["VALID_TEST_TOKEN"]}

        Monster(
            name="monster_name",
            race="monster_race",
            health_points="100",
            armor_points="100",
            attack_damage="100",
            xp_drop="100",
        ).insert()

        Dungeon(
            level="1",
            rooms="1",
            treasures="1",
            traps="1",
            boss_level=False,
            xp_drop="1000",
        ).insert()

    @classmethod
    def tearDown(cls):
        if monster := Monster.find_by("monster_name"):
            monster.delete()

        if dungeon := Dungeon.find_by(1):
            dungeon.delete()

    @classmethod
    def tearDownClass(cls):
        print("\nruns once in the end")

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    """
    ### Test - Monster routes
    """

    def test_error_unauthorized_get_monsters(self):
        response = self.client().get(
            "/monsters",
        )
        self.assertEqual(response.status_code, 401)

    def test_ok_authorized_get_monsters(self):
        response = self.client().get(
            "/monsters",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_not_found_monster(self):
        response = self.client().get(
            "/monsters/9999",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_found_monster(self):
        monster = Monster.find_by("monster_name")
        id = monster.id
        response = self.client().get(
            f"/monsters/{id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_create_monster(self):
        payload = {
            "name": "monster_name",
            "race": "monster_race",
        }
        response = self.client().post(
            "/monsters",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 405)

    def test_ok_create_monster(self):
        payload = {
            "name": "new_name",
            "race": "monster_race",
        }
        response = self.client().post(
            "/monsters",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 200)
        monster = Monster.find_by("new_name")
        monster.delete()

    def test_error_update_monster(self):
        payload = {
            "name": "monster_name",
            "xp_drop": "999",
        }
        response = self.client().patch(
            "/monsters/9999",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_update_monster(self):
        monster = Monster.find_by("monster_name")
        id = monster.id
        payload = {
            "name": "monster_name",
            "attack_damage": "3",
            "xp_drop": "100",
        }
        response = self.client().patch(
            f"/monsters/{id}",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_delete_monster(self):
        response = self.client().delete(
            "/monsters/9999",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_delete_monster(self):
        monster = Monster.find_by("monster_name")
        id = monster.id
        response = self.client().delete(
            f"/monsters/{id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    """
    ### Test - Dungeon routes
    """

    def test_error_unauthorized_get_dungeons(self):
        response = self.client().get(
            "/dungeons",
        )
        self.assertEqual(response.status_code, 401)

    def test_ok_authorized_get_dungeons(self):
        response = self.client().get(
            "/dungeons",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_not_found_dungeon(self):
        response = self.client().get(
            "/dungeons/9999",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_found_dungeon(self):
        dungeon = Dungeon.find_by(1)
        id = dungeon.id
        response = self.client().get(
            f"/dungeons/{id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_create_dungeon(self):
        payload = {
            "level": "1",
            "rooms": "1",
        }
        response = self.client().post(
            "/dungeons",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 405)

    def test_ok_create_dungeon(self):
        payload = {
            "level": "2",
            "rooms": "1",
        }
        response = self.client().post(
            "/dungeons",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 200)
        dungeon = Dungeon.find_by(2)
        dungeon.delete()

    def test_error_update_dungeon(self):
        payload = {
            "name": "dungeon_name",
            "xp_drop": "999",
        }
        response = self.client().patch(
            "/dungeons/9999",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_update_dungeon(self):
        dungeon = Dungeon.find_by(1)
        id = dungeon.id
        payload = {
            "name": "dungeon_name",
            "attack_damage": "3",
            "xp_drop": "100",
        }
        response = self.client().patch(
            f"/dungeons/{id}",
            headers=self.headers,
            json=payload,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_delete_dungeon(self):
        response = self.client().delete(
            "/dungeons/9999",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_delete_dungeon(self):
        dungeon = Dungeon.find_by(1)
        id = dungeon.id
        response = self.client().delete(
            f"/dungeons/{id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_error_add_monster_to_dungeon(self):
        response = self.client().post(
            "/dungeons/9999/monsters",
            headers=self.headers,
            json={"monster_id": "12345"},
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_add_monster_to_dungeon(self):
        monster = Monster.find_by("monster_name")
        monster_id = monster.id
        dungeon = Dungeon.find_by(1)
        dungeon_id = dungeon.id
        response = self.client().post(
            f"/dungeons/{dungeon_id}/monsters",
            headers=self.headers,
            json={"monster_id": monster_id},
        )
        self.assertEqual(response.status_code, 200)

    def test_error_remove_monster_to_dungeon(self):
        response = self.client().delete(
            "/dungeons/9999/monsters",
            headers=self.headers,
            json={"monster_id": "12345"},
        )
        self.assertEqual(response.status_code, 404)

    def test_ok_remove_monster_to_dungeon(self):
        monster = Monster.find_by("monster_name")
        monster_id = monster.id
        dungeon = Dungeon.find_by(1)
        dungeon_id = dungeon.id
        dungeon.monsters.append(monster)
        response = self.client().delete(
            f"/dungeons/{dungeon_id}/monsters",
            headers=self.headers,
            json={"monster_id": monster_id},
        )
        self.assertEqual(response.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
