from flask import Blueprint,render_template, flash, get_flashed_messages, request
from flask_login import login_required, current_user
from sqlalchemy import desc
from app.models.hangman import Hangman,Game
from app.models.user import User
from app import db
from app.forms.game import GameForm

gui = Blueprint('gui',__name__)

@gui.route('/')
def home():
    return render_template('home.html')

@gui.route('/halloffame')
def halloffame():
    games = db.session.query(Game, User).filter(User.id == Hangman.user_id, Game.status=='WON').order_by(desc(Game.score)).limit(10)
    return render_template('halloffame.html',games=games)

@gui.route('/play',methods=['GET','POST'])
def play():
    form = GameForm()

    hangman = Hangman.query.filter_by(user_id = current_user.get_id(),status = 'ACTIVE').first()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user_guess_list = hangman.get_user_guess()
            user_guess_list.append(form.guess_character.data)
            hangman.set_user_guess(user_guess_list)
 
            form.guess_character.data=''

            if hangman.status == 'WON':
                flash('{}, you are awesome! You won the game scoring {} points.'.format(current_user.name,hangman.score), 'is-success')
            elif hangman.status == 'LOST':
                flash('{}, you are a loser'.format(current_user.name), 'is-danger')
            
            db.session.add(hangman)
            db.session.commit()
        else:
            flash("Your guess is unaceptable: " + ", ".join(form.guess_character.errors), 'is-danger')

        return render_template('play.html', hangman=hangman, form=form)
        

    if hangman == None:
        flash('Starting new game', 'is-success')
        hangman = Hangman(current_user.id)
    else:
        flash('You had a previous unfinished game', 'is-danger')

    db.session.add(hangman)
    db.session.commit()

    return render_template('play.html',hangman=hangman,form=form)
