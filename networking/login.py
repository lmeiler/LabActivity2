# import json
# import bottle._
from bottle import *
import bottle
import time
import datetime
import random
import canister
from canister import session
# import sqlite3
import sqlite3

Bottle().config.load_config('<my-config-file-path>')
install(canister.Canister())

connection = sqlite3.connect("players.db")
c = connection.cursor()



@route('/')
def index():

    return'''
    <form action="/join" method="post">
            Username: <input name="username" type="text" />
            <input value="Login" type="submit" />
        </form>
    
</form>
'''


def create_table():

    sql_command = """
        CREATE TABLE IF NOT EXISTS players (
        PlayerID VARCHAR,
        Name VARCHAR(20),
        timeJoined VARCHAR,
        PRIMARY KEY (PlayerID) );
    """
    c.execute(sql_command)
    connection.commit()


@route('/join', method='POST')
def join():
    session.user = request.forms.get('username')
    date = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H: %M: %S"))
    playerid = random.randint(0,1000000000)
    create_table()

    sql_command = """
         INSERT INTO players(
          "PlayerID", 
          "Name",
          timeJoined
          )
          VALUES (
          ?,
          ?,
          ?
          );
    """
    c.execute(sql_command, (playerid, session.user, date))
    connection.commit()

    #players()
    if session.user is not None:
        return """
            <p>{}<p>
            <form action="/leave" method="post">
                <input value="Leave" type="submit" />
            </form>
        """.format(session.user)
    else:
        redirect('/')

@route('/join', method='GET')
def players():
    sql_command = """
         SELECT * FROM players
    """
    c.execute(sql_command)
    data = c.fetchall()
    list = []
    for row in data:
        list += row[1]


@route('/leave', method='POST')
def leave():
    #     sql_command = """
    #          SELECT * FROM players
    #     """
    # #    c.execute(sql_command)
    #     new_sql_command = """
    #         DELETE FROM players WHERE Name = ?
    #     """
    #     c.execute(new_sql_command, session.user)
    session.user = None
    redirect('/')


run(host='localhost', port=8081, debug=True)
c.close()
connection.close()

