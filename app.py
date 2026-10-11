from flask import Flask, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "skillmatch_secret_key"


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()

        query = """
        SELECT * FROM users
        WHERE email = %s AND password = %s
        """

        cursor.execute(query, (email, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return "Login successful!"
        else:
            return "Invalid email or password!"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return "Please login first!"

    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return "Logged out successfully!"


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return "Please login first!"

    if request.method == "POST":
        skills = request.form["skills"]
        interests = request.form["interests"]
        availability = request.form["availability"]

        db = get_db_connection()
        cursor = db.cursor()

        query = """
        UPDATE users
        SET skills = %s, interests = %s, availability = %s
        WHERE id = %s
        """

        cursor.execute(
            query,
            (skills, interests, availability, session["user_id"])
        )

        db.commit()

        cursor.close()
        db.close()

        return "Profile saved successfully!"

    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)
