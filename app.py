from flask import Flask,render_template,request,redirect,url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)

@app.route("/",methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        new_data = request.form.to_dict()
        mongo.db.test.insert_one(new_data)
        d = mongo.db.test.find()
        data = [doc for doc in d]
        return render_template('index.html',data=data)
    else:
        return render_template('home.html')

@app.route('/record')
def record():
    d = mongo.db.test.find()
    data = [doc for doc in d]
    return render_template("index.html",data=data)


@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('_id')
        mongo.db.test.delete_one({'_id':ObjectId(id)})
        d = mongo.db.test.find()
        new_data = [doc for doc in d]
        return redirect(url_for('record'))

if __name__ == '__main__':
    app.run(debug=True)