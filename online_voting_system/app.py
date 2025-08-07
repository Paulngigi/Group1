from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'voting_secret_key'

CANDIDATES_FILE = "candidates.json"
VOTERS_FILE = "voters.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# JSON Utility
def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Voter Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        password = request.form['password']
        voters = load_json(VOTERS_FILE)

        if voter_id in voters:
            flash("Voter ID already exists!")
        else:
            voters[voter_id] = {
                "password": generate_password_hash(password),
                "voted": False
            }
            save_json(VOTERS_FILE, voters)
            flash("Registration successful! Please log in.")
            return redirect(url_for('voter_login'))
    return render_template('register.html')


# Voter Login
@app.route('/voter_login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        password = request.form['password']
        voters = load_json(VOTERS_FILE)

        if voter_id in voters and check_password_hash(voters[voter_id]['password'], password):
            session['voter_id'] = voter_id
            return redirect(url_for('vote'))
        else:
            flash("Invalid voter ID or password.")
    return render_template('voter_login.html')


# Admin Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if (request.form['username'] == ADMIN_USERNAME and
                request.form['password'] == ADMIN_PASSWORD):
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

# Admin Dashboard
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    candidates = load_json(CANDIDATES_FILE)

    if request.method == 'POST':
        name = request.form['name']
        if name not in candidates:
            candidates[name] = 0
            save_json(CANDIDATES_FILE, candidates)
            flash(f"Candidate {name} added.")
        else:
            flash("Candidate already exists!")

    return render_template('admin.html', candidates=candidates)

# Vote Page
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'voter_id' not in session:
        return redirect(url_for('voter_login'))

    voter_id = session['voter_id']
    voters = load_json(VOTERS_FILE)

    if voters[voter_id]['voted']:
        flash("You have already voted.")
        return redirect(url_for('index'))

    candidates = load_json(CANDIDATES_FILE)

    if request.method == 'POST':
        choice = request.form['candidate']
        if choice in candidates:
            candidates[choice] += 1
            voters[voter_id]['voted'] = True
            save_json(CANDIDATES_FILE, candidates)
            save_json(VOTERS_FILE, voters)
            flash("Vote cast successfully!")
            return redirect(url_for('index'))
        else:
            flash("Invalid candidate.")

    return render_template('vote.html', candidates=candidates)

# View Results
@app.route('/results')
def results():
    candidates = load_json(CANDIDATES_FILE)
    names = list(candidates.keys())
    votes = list(candidates.values())
    return render_template('results.html', candidates=candidates, names=names, votes=votes)


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
