import os

from flask.wrappers import Request
from dotenv import load_dotenv
from flask import Flask
from flask import request

import sqlite3
from datetime import datetime
from dto import ProblemDTO

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
QUEUE_TABLE_NAME = "problem_queue"
app = Flask(__name__)


def get_queue_db_cursor():
    '''
    Return DB cursor of queue.
    '''
    conn = sqlite3.connect("db.sqlite3", isolation_level=None)
    return conn.cursor()


def check_table():
    '''
    Check there is the table correspons to today.
    if not, create the table.
    '''
    get_queue_db_cursor().execute(
        'CREATE TABLE IF NOT EXISTS "{}"(pid int primary key, description text, difficulty integer, category text, username text, timestamp text)'.format(QUEUE_TABLE_NAME))


def add_problem(problem):
    '''
    Insert problem to the queue.
    If the id is duplicated, sqlite3.IntegrityError occurs.
    '''
    check_table()

    get_queue_db_cursor().execute(
        'INSERT INTO "{}" VALUES(?, ?, ?, ?, ?, ?)'.format(QUEUE_TABLE_NAME), problem.get_tuple())


def get_all_problems():
    '''
    Return all problems queued.
    If there is no problems, it returns None.
    '''
    try:
        cursor = get_queue_db_cursor()

        cursor.execute('SELECT * FROM "{}"'.format(QUEUE_TABLE_NAME))

        problem_tuples = cursor.fetchall()
        problems = []
        for problem_tuple in problem_tuples:
            problems.append(ProblemDTO(
                problem_tuple[0], problem_tuple[1], problem_tuple[2], problem_tuple[3], problem_tuple[4], problem_tuple[5]))

        return problems
    except:
        return None


def is_required_validated(required_keys, request_keys):
    '''
    If at least one of required keys is not in request keys, return false.
    '''
    if set(required_keys)-set(request_keys):
        return False
    return True


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


@ app.route("/")
def home():
    return "This is Almight"


@ app.route("/problems", methods=["POST", "GET"])
def process_problems():
    if request.method == "POST":
        arguments = request.get_json()

        if not is_required_validated(["pid", "description", "difficulty", "category", "username", "token"], arguments.keys()):
            return "400 BAD REQUEST: missing arguments.", 400
        if not arguments["token"] == SLACK_BOT_TOKEN:
            return "403 FORBIDDEN: token mismatch.", 403

        try:
            problem = ProblemDTO(int(arguments["pid"]), str(arguments["description"]),
                                 int(arguments["difficulty"]), str(arguments["category"]), str(arguments["username"]), today_str())
        except:
            return "400 BAD REQUEST: arguments type mismatch.", 400

        try:
            add_problem(problem)
            return "201 CREATED: the problem completely added.", 201
        except sqlite3.IntegrityError:
            return "400 BAD REQUEST: Duplicated problem number.", 400
        except:
            return "400 BAD REQUEST: There's a problem with the request.", 400

    elif request.method == "GET":
        problems = get_all_problems()

        if problems == None:
            return "404 NOT FOUND: there is no problems in DB", 404

        problems = {"results": list(map(lambda p: p.get_dict(), problems))}
        return problems, 200
