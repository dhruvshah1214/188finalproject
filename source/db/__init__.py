import os

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(None)

def get_db_uri():
    return "postgresql://" + \
            os.getenv('DB_USERNAME') + ":" + os.getenv('DB_PASSWORD') + "@" + \
            os.getenv('POSTGRES_HOST_URL') + "/" + os.getenv("POSTGRES_DB_NAME")

bcrypt = bcrypt


import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker

Model = sqlalchemy.orm.declarative_base()

engine = sqlalchemy.create_engine(get_db_uri(), echo=True)
db = sessionmaker(bind = engine)()

from source.db.models.user import User
from source.db.models.monitor import Monitor
from source.db.models.target import Target

print("DB IMPORTED")

Model.metadata.create_all(engine)

usaco = Target(
    id="usaco-git",
    url="https://github.com/dhruvshah1214/usaco/tree/master",
    selector="article"
)
mset = Target(
    id="mset-git",
    url="https://github.com/SaratogaMSET/Nigiri2019",
    selector="article"
)
mpc = Target(
    id="mpc-git",
    url="https://github.com/dhruvshah1214/CarND-MPC-Project",
    selector="article"
)
bartender = Target(
    id="bartender-git",
    url="https://github.com/dhruvshah1214/bartender_ros/tree/master",
    selector="article"
)
db.add(bartender)
db.add(usaco)
db.add(mpc)
db.add(mset)
try:
    db.commit()
except Exception as e:
    print(e)
    db.rollback()