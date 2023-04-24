import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Teacher(SqlAlchemyBase, UserMixin):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now().date())
    
    lessons = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    #mathematics = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    #physics = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    #informatics = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    projects = orm.relationship("Projects", back_populates='teacher')
    

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)