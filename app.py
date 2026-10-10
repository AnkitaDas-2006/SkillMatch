from flask import Flask,render_template
import mysql.connector
app=Flask(__name__)
def get_db_connection():
	return mysql.connector.connect(host="localhost",user="skillmatch_user",password="SkillMatch@123",database="skillmatch")
@app.route("/")
def home():
	return render_template("index.html")
@app.route("/register")
def register():
	return render_template("register.html")
if __name__=="__main__":
	app.run(debug=True)
