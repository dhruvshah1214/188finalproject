# db/models/target.py

from  source.db import Model
import sqlalchemy as sqa
import sqlalchemy.orm as orm

class Target(Model):
    """ Target Model for storing monitor targets """
    __tablename__ = "targets"

    id = sqa.Column(sqa.String(255), primary_key=True, nullable=False, unique=True)
    url = sqa.Column(sqa.String(255), unique=False, nullable=False)
    selector = sqa.Column(sqa.String(255), unique=False, nullable=False)
    monitors = orm.relationship("Monitor", back_populates = "target")

    def __init__(self, id, url, selector):
        self.id = id
        self.url = url
        self.selector = selector
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    
