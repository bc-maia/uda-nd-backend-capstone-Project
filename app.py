import os
from models import Dungeon, Monster
from database import setup_db
from flask import Flask, jsonify, abort, request, Response
from flask_cors import CORS


def create_app(test_config=None):

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    setup_db(app)
    CORS(app)

    @app.route("/")
    def get_greeting():
        return "Monster-Dungeons API"

    """
    ### Routes: Dungeons
    """

    @app.route("/dungeons", methods=["GET"])
    def get_dungeons():
        if dungeons := Dungeon.all():
            result = {"success": True, "Dungeons": dungeons}
            return jsonify(result)
        else:
            abort(404)

    @app.route("/dungeons/<id>", methods=["GET"])
    def get_dungeon(id):
        if dungeon := Dungeon.find(id):
            result = {"success": True, "Dungeon": dungeon.long()}
            return jsonify(result)
        else:
            abort(404)

    @app.route("/dungeons", methods=["POST"])
    def add_dungeon():
        payload = request.get_json()
        if not payload:
            abort(400)

        level = payload.get("level", None)

        if Dungeon.find_by(level):
            abort(
                Response(
                    response=f"Dungeon level: {level} already created.",
                    status=405,
                )
            )

        level = payload.get("level", None)
        rooms = payload.get("rooms", None)
        treasures = payload.get("treasures", None)
        traps = payload.get("traps", None)
        boss_level = payload.get("boss_level", None)
        xp_drop = payload.get("xp_drop", None)

        dungeon = Dungeon(
            level=level,
            rooms=rooms,
            treasures=treasures,
            traps=traps,
            boss_level=boss_level,
            xp_drop=xp_drop,
        )
        dungeon.insert()
        return jsonify(dungeon.short())

    @app.route("/dungeons/<id>", methods=["PATCH"])
    def update_dungeon(id):
        payload = request.get_json()
        if not payload:
            abort(400)

        if dungeon := Dungeon.find(id):

            if level := payload.get("level", None):
                if checker := Dungeon.find_by(level):
                    if dungeon.id != checker.id:
                        abort(
                            Response(
                                response=f"level id: {level} belongs to another dungeon.",
                                status=405,
                            )
                        )
                dungeon.level = level
            if rooms := payload.get("rooms", None):
                dungeon.rooms = rooms
            if treasures := payload.get("treasures", None):
                dungeon.treasures = treasures
            if traps := payload.get("traps", None):
                dungeon.traps = traps
            if boss_level := payload.get("boss_level", None):
                dungeon.boss_level = boss_level
            if xp_drop := payload.get("xp_drop", None):
                dungeon.xp_drop = xp_drop

            dungeon.update()
            return jsonify(dungeon.long())
        else:
            abort(404)

    @app.route("/dungeons/<id>", methods=["DELETE"])
    def remove_dungeon(id):
        if dungeon := Dungeon.find(id):
            level = dungeon.level
            dungeon.delete()
            result = {"success": True, "removed dungeon level": level}
            return jsonify(result)
        else:
            abort(404)

    @app.route("/dungeons/<id>/monsters", methods=["GET"])
    def get_dungeons_monster(id):
        if dungeon := Dungeon.find(id):
            response = {
                "level": dungeon.level,
                "Boss Level": dungeon.boss_level,
                "monsters": [m.long() for m in dungeon.monsters],
            }
            return jsonify(response)
        else:
            abort(404)

    @app.route("/dungeons/<id>/monsters", methods=["POST"])
    def add_dungeons_monster(id):
        payload = request.get_json()
        monster_id = payload.get("monster_id", None)

        if not monster_id:
            abort(400)

        if dungeon := Dungeon.find(id):
            if monster := Monster.find(monster_id):
                dungeon.monsters.append(monster)
                dungeon.update()
            else:
                abort(400)
            return jsonify(dungeon.short())
        else:
            abort(404)

    @app.route("/dungeons/<id>/monsters", methods=["DELETE"])
    def remove_dungeons_monster(id):
        payload = request.get_json()
        monster_id = payload.get("monster_id", None)

        if not monster_id:
            abort(400)

        if dungeon := Dungeon.find(id):
            if monster := Monster.find(monster_id):
                dungeon.monsters.remove(monster)
                dungeon.update()
            else:
                abort(400)
            return jsonify(dungeon.short())
        else:
            abort(404)

    """
    ### Routes: Monsters
    """

    @app.route("/monsters", methods=["GET"])
    def get_monsters():
        if monsters := Monster.all():
            result = {"success": True, "Monsters": monsters}
            return jsonify(result)
        else:
            abort(404)

    @app.route("/monsters/<id>", methods=["GET"])
    def get_monster(id):
        if monster := Monster.find(id):
            result = {"success": True, "Monster": monster.long()}
            return jsonify(result)
        else:
            abort(404)

    @app.route("/monsters", methods=["POST"])
    def add_monster():
        payload = request.get_json()
        if not payload:
            abort(400)

        name = payload.get("name", None)

        if Monster.find_by(name):
            abort(
                Response(
                    response=f"Monster '{name}' already created.",
                    status=405,
                )
            )

        race = payload.get("race", None)
        health_points = payload.get("health_points", None)
        armor_points = payload.get("armor_points", None)
        attack_damage = payload.get("attack_damage", None)
        xp_drop = payload.get("xp_drop", None)

        monster = Monster(
            name=name,
            race=race,
            health_points=health_points,
            armor_points=armor_points,
            attack_damage=attack_damage,
            xp_drop=xp_drop,
        )
        monster.insert()
        return jsonify(monster.short())

    @app.route("/monsters/<id>", methods=["PATCH"])
    def update_monster(id):
        payload = request.get_json()
        if monster := Monster.find(id):
            if name := payload.get("name", None):
                if checker := Monster.find_by(name):
                    if monster.id != checker.id:
                        abort(
                            Response(
                                response=f"Name: '{name}' belongs to another monster.",
                                status=405,
                            )
                        )
                monster.name = name
            if race := payload.get("race", None):
                monster.race = race
            if health_points := payload.get("health_points", None):
                monster.health_points = health_points
            if armor_points := payload.get("armor_points", None):
                monster.armor_points = armor_points
            if attack_damage := payload.get("attack_damage", None):
                monster.attack_damage = attack_damage
            if xp_drop := payload.get("xp_drop", None):
                monster.xp_drop = xp_drop

            monster.update()

            return jsonify({"success": True, "Monster": monster.long()})
        else:
            abort(404)

    @app.route("/monsters/<id>", methods=["DELETE"])
    def remove_monster(id):
        if monster := Monster.find(id):
            name = monster.name
            monster.delete()
            result = {"success": True, "deleted": name}
            return jsonify(result)
        else:
            abort(404)

    """
    Error Handling
    """

    def format_handler(message: str, status: int) -> any:
        return (
            jsonify(
                {
                    "success": False,
                    "message": message,
                    "error": status,
                }
            ),
            status,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return format_handler("bad request", 400)

    """
    TODO-DONE: implement error handler for 404
        error handler should conform to general task above
    """

    @app.errorhandler(404)
    def not_found(error):
        return format_handler(message="resource not found", status=404)

    @app.errorhandler(405)
    def not_allowed(error):
        return format_handler("method not allowed", 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return format_handler("unprocessable", 422)

    """
    TODO-DONE: implement error handler for AuthError
        error handler should conform to general task above
    """

    # @app.errorhandler(AuthError)
    # def authentification_failed(AuthError):
    #     return (
    #         jsonify(
    #             {
    #                 "success": False,
    #                 "error": AuthError.status_code,
    #                 "message": AuthError.error,
    #             }
    #         ),
    #         AuthError.status_code,
    #     )

    @app.errorhandler(401)
    def unauthorized(error):
        return format_handler("unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(error):
        return format_handler("forbidden", 403)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()