from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="skillmatch_user",
        password="SkillMatch@123",
        database="skillmatch"
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        branch = request.form["branch"]
        year = request.form["year"]

        db = get_db_connection()

        cursor = db.cursor()

        query = """
        INSERT INTO users (name, email, password, branch, year)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (name, email, password, branch, year))

        db.commit()

        cursor.close()
        db.close()

        return "Registration successful!"

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
