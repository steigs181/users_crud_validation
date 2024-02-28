from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    DB = 'users_schema'

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, user_id):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s"""
        data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def create_user(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW())
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
        
    
    @classmethod
    def update_user(cls, data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW()
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def delete_user(cls, id):
        query = """
                DELETE FROM users 
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})
        return results
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 3:
            flash ("First Name must be at least 3 characters")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if len(user["email"]) < 3:
            flash("Email must be at least 3 character")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
