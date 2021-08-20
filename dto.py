from flask import json, jsonify


class ProblemDTO:
    def __init__(self, pid, description, difficulty, category, username):
        self.pid = pid
        self.description = description
        self.difficulty = difficulty
        self.category = category
        self.username = username

    def get_tuple(self):
        return (self.pid, self.description, self.difficulty, self.category, self.username)

    def get_dict(self):
        return {
            "pid": self.pid,
            "description": self.description,
            "difficulty": self.difficulty,
            "category": self.category,
            "username": self.username
        }
