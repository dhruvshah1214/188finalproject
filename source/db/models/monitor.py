# server/models/monitor.py
import jwt
import datetime


from  source.db import Model
import sqlalchemy as sqa
import sqlalchemy.orm as orm

class Monitor(Model):
    """ Monitor Model for storing user related details """
    __tablename__ = "monitors"

    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    user_id = sqa.Column(sqa.Integer, sqa.ForeignKey("users.id"))
    user = orm.relationship("User", back_populates = "monitors")
    target_id = sqa.Column(sqa.String(255), sqa.ForeignKey("targets.id"))
    target = orm.relationship("Target", back_populates = "monitors")
    name = sqa.Column(sqa.String(255), unique=False, nullable=False)
    enabled = sqa.Column(sqa.Boolean, nullable=False)

    def __init__(self, user, target, name):
        self.user = user
        self.user_id = user.id
        self.target = target
        self.target_id = target.id
        self.enabled = True
        self.name = name
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    
