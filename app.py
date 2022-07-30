from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({ "game_id": game_id, "board": game.board})

@app.post("/api/score-word")
def check_for_legal_word():
    """accept JSON for game id and word,
        check that the word is in the word list
        check that the word is on the board
        return a dictionary with key 'result' and
        value either 'not-word' 'not-on-board' or 'ok',
        return word_score
        """
    response = request.json
    game = games[response['game_id']]
    word = response['word'].upper()

    is_word = game.is_word_in_word_list(word)
    is_on_board = game.check_word_on_board(word)

    if not is_word:
        return jsonify({"result": "not-word"})
    elif not is_on_board:
        return jsonify({"result": "not-on-board"})
    else:
        return jsonify({"result": "ok"})