from source.web import app, redis
from source.db import db
from source.db.models.user import User
from source.db.models.monitor import Monitor
from source.db.models.target import Target

from source.web.auth import auth

from flask import request

allowed_monitors = []
try:
    with open("/app/config/allowedmonitors") as file:
        print("READING FILE")
        lines = [line.rstrip() for line in file]
        print(lines)
        allowed_monitors.extend(lines)
except Exception as e:
    print(e)

@app.route('/monitors/', methods=["GET", "POST"]) # get: list my monitors, post: create new
@auth.login_required
def monitors():
    if request.method == "GET":
        my_monitors = db.query(Monitor).filter(Monitor.user_id == auth.current_user().id).all()
        monitors_json = [m.as_dict() for m in my_monitors]
        return ({"monitors": monitors_json}, 200)
    elif request.method == "POST":
        post_data = request.get_json()
        try:
            tgt_id = post_data.get("target", None)
            target = db.query(Target).filter(Target.id == tgt_id).first()

            if target == None:
                return {"success": False, "message": f"Monitor target {tgt_id} doesn't exist"}, 404
            if tgt_id not in allowed_monitors:
                return {"success": False, "message": f"Monitor target {tgt_id} is not allowed."}, 405
            
            monitor = Monitor(
                user=auth.current_user(),
                name=post_data.get("name"),
                target=target
            )
            db.add(monitor)
            db.commit()
            return {"success": True, "monitor": monitor.as_dict()}, 200
        except Exception as e:
            print(e)
            return str(e), 500

@app.route('/monitors/<monitor_id>', methods=["GET", "POST"]) # get: get details of monitor, post: update monitor
@auth.login_required
def get_monitor(monitor_id=None):
    return "Hello, {}!".format(auth.current_user())

@app.route('/monitors/<monitor_id>/enable', methods=["POST"]) # turn on monitor
@auth.login_required
def enable_monitor(monitor_id=None):
    return "Hello, {}!".format(auth.current_user())

@app.route('/monitors/<monitor_id>/disable', methods=["POST"]) # turn off monitor
@auth.login_required
def disable_monitor(monitor_id=None):
    return "Hello, {}!".format(auth.current_user())
