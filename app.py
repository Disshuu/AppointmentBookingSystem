from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    date = db.Column(db.String(50))
    time = db.Column(db.String(20))
    message = db.Column(db.Text)

# Booking Page Route
@app.route('/', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']

        new_appt = Appointment(name=name, email=email, date=date, time=time, message=message)
        db.session.add(new_appt)
        db.session.commit()

        return "✅ Appointment Booked Successfully!"
    return render_template('appointment.html')

# Admin View
@app.route('/appointments')
def view_appointments():
    all_appts = Appointment.query.all()
    return "<br>".join([f"{a.name} | {a.email} | {a.date} | {a.time} | {a.message}" for a in all_appts])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
