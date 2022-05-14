from asyncio.windows_events import NULL
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#three forward slashes is relative path 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///league.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialise DB with setting from the app
db = SQLAlchemy(app) 

class Player(db.Model):
    id = db.Column(db.Integer, index=True, primary_key = True)
    username = db.Column(db.String(15), nullable=False)
    creationDate = db.Column(db.DateTime, default= datetime.utcnow)
    active = db.Column(db.Boolean(), default=True)
    rating = db.Column(db.Integer, nullable=False, default = 1500)
    admin = db.Column(db.Boolean(), default=False)
    positionInGame = db.relationship('Game', backref='player', default = NULL)
    inGameStatus = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self) -> str:
        return '<User: %s>' %self.username

class Game(db.Model):
    gameId = db.Column(db.Integer, primary_key=True, index=True)
    idUsername = db.Column(db.String(15), db.ForeignKey('player.username'))
    position = db.Column(db.String(8), nullable = False)
    gameActiveStatus = db.Column(db.Boolean(), default=True)

    def __repr__(self) -> int:
        return '<Game ID: %i>' %self.gameId



@app.route('/', methods = ['POST','GET'])
def players():
    if request.method == 'POST':
        playerContent = request.form['content']
        newPlayer = Player(content = playerContent)
        try:
            db.session.add(newPlayer)
            db.session.commit()
            return redirect('/')
        except:
            return 'Could not add new Player'
    else:
        players=Player.query.order_by(Player.creationDate).all()
        return render_template('index.html', tasks=players)

if __name__ == "__main__":
    app.run(debug=True)