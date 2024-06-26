import random
from flask import Flask, render_template, request
from database import add_player_to_db, add_player_role_to_db, load_players_from_db, add_game_entry, leaderboard, game_history

app = Flask(__name__)
import random 
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/store_values', methods=['POST'])
def store_values():
    global gameid 
    gameid = random.randint(1000, 9999)  
    entries = {}
    role = request.form['role']
    pos = [1,2,3,4,5]
    count = 0
    # Store player information
    for i in range(1, 11):
        if i % 2 == 1:  # Odd-indexed values
            key = request.form[f'entry{i}']
        else:  # Even-indexed values
            value = request.form[f'entry{i}']
            entries[key] = value
            add_player_to_db(key, value,pos[count],gameid)
            count = count+1
            add_player_role_to_db(role)
    print(entries, role)
    leaderboard()

    # Start a new game
   # global gameid 
   # gameid = random.randint(1000, 9999)  
    game_history(gameid)
    start_new_game(role)

    return 'New game started successfully!'

def start_new_game(role):
    # Generate a random game ID
   
    # Add entries for each player in the game
    for i in range(2, 11, 2):
        playerid = request.form[f'entry{i}']
        role = load_players_from_db(playerid)
        if role:
            add_game_entry(gameid, playerid, role)
        else:
            print(f"Role not found for player ID: {playerid}")
        print(gameid, playerid, role)

if __name__ == "__main__":
    app.run(debug=True)
