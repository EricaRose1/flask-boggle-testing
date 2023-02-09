
from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'

boggle_game = Boggle()

@app.route('/')
def show_board():
    '''display board, score, highscore, and times played'''
    board = boggle_game.make_board()
    session["board"] = board
    num_plays = session.get('num_plays', 0)
    highscore = session.get("highscore", 0)

    # '''track words typed'''
    # session['track_words'] = []

    return render_template('base.html', board=board,
                                        highscore=highscore, 
                                        num_plays=num_plays)


@app.route("/check-word")
def word_input():
    '''check input of word is in dictionary'''

    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({"result": response})

@app.route("/post-score", methods=['POST'])
def post_score():
    '''received score, update num of plays and highscore if applicable'''
    score = request.json['score']
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score,highscore)

    return jsonify(brokeRecord=score > highscore)
