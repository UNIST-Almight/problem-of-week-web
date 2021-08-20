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


@ app.route("/")
def home():
    return "This is Almight"
