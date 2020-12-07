import os
import json
from flask_sqlalchemy import SQLAlchemy
from database import db

monsters = db.Table(
    "monsters",
    db.Column("monster_id", db.Integer, db.ForeignKey("monster.id"), primary_key=True),
    db.Column("dungeon_id", db.Integer, db.ForeignKey("dungeon.id"), primary_key=True),
)

"""
Dungeon
A dungeon is where you fight against enemy, extends the base SQLAlchemy Model
"""


class Dungeon(db.Model):
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True)
    level = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    treasures = db.Column(db.Integer)
    traps = db.Column(db.Integer)
    boss_level = db.Column(db.Boolean)
    xp_drop = db.Column(db.Integer)
    monsters = db.relationship(
        "Monster",
        secondary=monsters,
        lazy="subquery",
        backref=db.backref("dungeons", lazy=True),
    )

    def __repr__(self):
        return json.dumps(self.short())

    """
    short()
        short form representation of the Dungeon model
    """

    def short(self) -> dict:
        return {
            "id": self.id,
            "level": self.level,
            "rooms": self.rooms,
            "monsters": [m.short() for m in self.monsters],
        }

    """
    long()
        long form representation of the Dungeon model
    """

    def long(self) -> dict:
        return {
            "id": self.id,
            "level": self.level,
            "rooms": self.rooms,
            "treasures": self.treasures,
            "traps": self.traps,
            "boss_level": self.boss_level,
            "xp_drop": self.xp_drop,
            "monsters": [m.short() for m in self.monsters],
        }

    """
    all()
        returns all monsters
    """

    @classmethod
    def all(cls, detail=False) -> list:
        if query := cls.query.all():
            return [d.long() if detail else d.short() for d in query]
        else:
            return None

    """
    find(id)
    find_by(level)
        tries to find an entity by id or by level
    """

    @classmethod
    def find(cls, id) -> any:
        return cls.query.filter(cls.id == id).one_or_none()

    @classmethod
    def find_by(cls, level) -> any:
        return cls.query.filter(cls.level == level).one_or_none()

    """
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
    """

    def update(self):
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
Monster
A creature enemy to battle against, extends the base SQLAlchemy Model
"""


class Monster(db.Model):
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    race = db.Column(db.String(80))
    health_points = db.Column(db.Integer)
    armor_points = db.Column(db.Integer)
    attack_damage = db.Column(db.Integer)
    xp_drop = db.Column(db.Integer)

    def __repr__(self):
        return json.dumps(self.short())

    """
    short()
        short form representation of the Monster model
    """

    def short(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "xp_drop": self.xp_drop,
        }

    """
    long()
        long form representation of the Monster model
    """

    def long(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "health_points": self.health_points,
            "armor_points": self.armor_points,
            "attack_damage": self.attack_damage,
            "xp_drop": self.xp_drop,
        }

    """
    all()
        returns all monsters
    """

    @classmethod
    def all(cls, detail=False) -> list:
        if query := cls.query.all():
            return [d.long() if detail else d.short() for d in query]
        else:
            return None

    """
    find(id)
    find_by(name)
        tries to find an entity by id or by title
    """

    @classmethod
    def find(cls, id) -> any:
        return cls.query.filter(cls.id == id).one_or_none()

    @classmethod
    def find_by(cls, name) -> any:
        return cls.query.filter(cls.name == name).one_or_none()

    """
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
    """

    def update(self):
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()
