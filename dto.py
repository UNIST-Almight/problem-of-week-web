from flask import json, jsonify


class ProblemDTO:
    def __init__(self, pid, description, difficulty, category, username, timestamp):
        self.pid = pid
        self.description = description
        self.difficulty = difficulty
        self.category = category
        self.username = username
        self.timestamp = timestamp

    def get_tuple(self):
        return (self.pid, self.description, self.difficulty, self.category, self.username, self.timestamp)

    def get_dict(self):
        return {
            "pid": self.pid,
            "description": self.description,
            "difficulty": self.difficulty,
            "category": self.category,
            "username": self.username,
            "timestamp": self.timestamp
        }
