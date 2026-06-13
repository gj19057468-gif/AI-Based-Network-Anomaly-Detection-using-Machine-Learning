from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import os

app = Flask(__name__)

app.secret_key = "network_anomaly_secret"

USERNAME = "admin"
PASSWORD = "admin123"


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    dataset_path = "../dataset/ml_dataset.csv"

    if not os.path.exists(dataset_path):

        return """
        Dataset not found.
        Please create:
        dataset/ml_dataset.csv
        """

    df = pd.read_csv(dataset_path)

    total_packets = len(df)

    tcp_packets = len(df[df["Protocol"] == 0])

    udp_packets = len(df[df["Protocol"] == 1])

    attack_packets = len(df[df["Label"] == 1])

    normal_packets = len(df[df["Label"] == 0])

    recent_packets = df.tail(20).to_dict(
        orient="records"
    )

    return render_template(
        "index.html",
        total_packets=total_packets,
        tcp_packets=tcp_packets,
        udp_packets=udp_packets,
        attack_packets=attack_packets,
        normal_packets=normal_packets,
        recent_packets=recent_packets
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)