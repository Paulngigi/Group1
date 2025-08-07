import json
import os

CANDIDATES_FILE = "candidates.json"
VOTERS_FILE = "voters.json"

admin_username = "admin"
admin_password = "1234"

# Utility Functions to Load/Save JSON
def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Admin Login
def admin_login():
    print("\n--- Admin Login ---")
    username = input("Username: ")
    password = input("Password: ")
    return username == admin_username and password == admin_password

# Add Candidate
def add_candidate():
    candidates = load_json(CANDIDATES_FILE)
    name = input("Enter candidate name: ")
    if name in candidates:
        print("Candidate already exists!")
    else:
        candidates[name] = 0
        save_json(CANDIDATES_FILE, candidates)
        print(f"{name} added as a candidate.")

# Cast Vote
def vote():
    voters = load_json(VOTERS_FILE)
    candidates = load_json(CANDIDATES_FILE)

    voter_id = input("Enter your Voter ID: ")
    if voter_id in voters:
        print("You have already voted.")
        return

    if not candidates:
        print("No candidates available.")
        return

    print("Candidates:")
    for candidate in candidates:
        print(f"- {candidate}")
    
    choice = input("Enter your choice: ")
    if choice in candidates:
        candidates[choice] += 1
        voters[voter_id] = choice
        save_json(CANDIDATES_FILE, candidates)
        save_json(VOTERS_FILE, voters)
        print("Vote cast successfully!")
    else:
        print("Invalid candidate.")

# Show Results
def show_results():
    candidates = load_json(CANDIDATES_FILE)
    print("\n--- Voting Results ---")
    for candidate, votes in candidates.items():
        print(f"{candidate}: {votes} votes")
    print("----------------------")

# Main Loop
def main():
    while True:
        print("\n1. Admin Login")
        print("2. Vote")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            if admin_login():
                while True:
                    print("\n--- Admin Panel ---")
                    print("1. Add Candidate")
                    print("2. Show Results")
                    print("3. Logout")
                    admin_choice = input("Enter your choice: ")

                    if admin_choice == '1':
                        add_candidate()
                    elif admin_choice == '2':
                        show_results()
                    elif admin_choice == '3':
                        break
                    else:
                        print("Invalid option.")
            else:
                print("Invalid login credentials.")
        elif choice == '2':
            vote()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
