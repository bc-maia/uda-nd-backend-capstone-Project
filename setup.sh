#!/bin/sh
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL="postgres://postgres:passwd123@localhost:5432/dungeon"
export AUTH0_DOMAIN="uda-cafe.us.auth0.com"
export ALGORITHMS=['RS256']
export API_AUDIENCE="https://dungeon-monster.herokuapp.com"