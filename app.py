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

app = Flask(__name__)


def get_queue_db_cursor():
    '''
    Return DB cursor of queue.
    '''
    conn = sqlite3.connect("problem_queue.db", isolation_level=None)
    return conn.cursor()


def check_date():
    '''
    Check there is the table correspons to today.
    if not, create the table.
    '''
    today = datetime.now().strftime("%Y-%m-%d")
    get_queue_db_cursor().execute("CREATE TABLE IF NOT EXISTS '"+today +
                                  "'(pid int primary key, description text, difficulty integer, category text, username text)")


def add_problem(date, problem):
    '''
    Insert problem to the target date table.
    If the work is complete, return True.
    '''
    check_date()
    try:
        get_queue_db_cursor().execute(
            "INSERT INTO '"+date.strftime("%Y-%m-%d")+"' VALUES(?, ?, ?, ?, ?)", problem.get_tuple())
        return True
    except:
        return False


def get_all_problems(date):
    '''
    Return all problems queued at date.
    If there is no table for the date, it returns None.
    '''
    try:
        cursor = get_queue_db_cursor()
        cursor.execute("SELECT * FROM '"+date.strftime("%Y-%m-%d")+"'")
        problem_tuples = cursor.fetchall()
        problems = []
        for problem_tuple in problem_tuples:
            problems.append(ProblemDTO(
                problem_tuple[0], problem_tuple[1], problem_tuple[2], problem_tuple[3], problem_tuple[4]))

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


@ app.route("/")
def home():
    return "This is Almight"


@ app.route("/problem/add", methods=["POST"])
def add_problem_request():
    arguments = request.get_json()

    if not is_required_validated(["pid", "description", "difficulty", "category", "username", "token"], arguments.keys()):
        return "400 BAD REQUEST: missing arguments.", 400
    if not arguments["token"] == SLACK_BOT_TOKEN:
        return "403 FORBIDDEN: token mismatch.", 403

    try:
        problem = ProblemDTO(int(arguments["pid"]), str(arguments["description"]),
                             int(arguments["difficulty"]), str(arguments["category"]), str(arguments["username"]))
    except:
        return "400 BAD REQUEST: arguments type mismatch.", 400

    if add_problem(datetime.now(), problem):
        return "201 CREATED: the problem completely added.", 201
    else:
        return "400 BAD REQUEST: There's a problem with the request.", 400


@ app.route("/problem/list",  methods=["GET"])
def get_problem_list():
    problems = get_all_problems(datetime.now())

    if problems == None:
        return "404 NOT FOUND: there is no problems in DB", 404

    problems = {"results": list(map(lambda p: p.get_dict(), problems))}
    return problems, 200
