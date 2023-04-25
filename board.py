from flask import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import time

#########################################################
# Flask 선언, mongodb와 연결
web_bulletin = Flask(__name__, template_folder="templates")
web_bulletin.config["MONGO_URI"] = "mongodb://localhost:27017/bulletin" 
web_bulletin.config['SECRET_KEY'] = 'psswrd'

mongo = PyMongo(web_bulletin)
#########################################################

@web_bulletin.route("/bulletin_wr", methods=["GET", "POST"])
def bulletin_write():
    if request.method == "POST":
        cur_time = time.strftime("%y%m%d_%H%M%S")
        title = request.form.get("title")
        contents = request.form.get("contents")

        bulletin = mongo.db.bulletin

        to_db = {
            "title": title,
            "contents": contents,
            "view_cnt": 0,
            "pubdate": cur_time,
        }
        to_db_post = bulletin.insert_one(to_db)
        print("to_db_post :",to_db_post)

        return redirect(url_for("bulletin_rd", idx = to_db_post.inserted_id))
    else:
        return render_template("bulletin_wr.html")

@web_bulletin.route("/bulletin_rd")
def bulletin_rd():
    if request.args.get("idx") :
        idx = request.args.get("idx")
        bulletin = mongo.db.bulletin
        if bulletin.find_one({"_id": ObjectId(idx)}):
            bulletin_data = bulletin.find_one({"_id": ObjectId(idx)})
            #db에서 찾을때 _id 값은 string이 아닌 ObjectId로 바꿔야함
            if bulletin_data != "":
                db_data = {
                    "id": bulletin_data.get("_id"),
                    "title": bulletin_data.get("title"),
                    "contents": bulletin_data.get("contents"),
                    "pubdate": bulletin_data.get("pubdate")
                }

                return render_template("bulletin_rd.html", db_data = db_data)
        return abort(404)
    return abort(404)


if __name__ == "__main__":
    web_bulletin.run(host='0.0.0.0', debug=True, port=9999)
