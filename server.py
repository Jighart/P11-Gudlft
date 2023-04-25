import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
    

def sort_competitions_date(comps):
    past = []
    present = []

    for comp in comps:
        if datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            past.append(comp)
        elif datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S') >= datetime.now():
            present.append(comp)

    return past, present


def initialize_booked_places(comps, clubs_list):
    places = []
    for comp in comps:
        for club in clubs_list:
            places.append({'competition': comp['name'], 'booked': [0, club['name']]})
    return places


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
past_competitions, present_competitions = sort_competitions_date(competitions)
clubs = loadClubs()
places_booked = initialize_booked_places(competitions, clubs)


def update_booked_places(competition, club, places_required):
    for item in places_booked:
        if item['competition'] == competition['name']:
            if item['booked'][1] == club['name'] and places_required > int(competition['numberOfPlaces']):
                raise ValueError("Not enough open places in the competition")
            elif item['booked'][1] == club['name'] and item['booked'][0] + places_required <= 12:
                item['booked'][0] += places_required
                break
            else:
                raise ValueError("You can't book more than 12 places in a competition.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )
    except IndexError:
        if request.form['email'] == '':
            flash("Please enter your email", 'error')
        else:
            flash("No account found with this email", 'error')
        return render_template('index.html'), 401


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        if datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
            flash("This competition is over.", 'error')
            return render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions
            ), 403
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    else:
        flash("Something went wrong-please try again", 'error')
        return render_template(
            'welcome.html',
            club=club,
            past_competitions=past_competitions,
            present_competitions=present_competitions
        ), 403


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    if places_required > int(club['points']):
        flash('You don\'t have enough points.')
        return render_template('booking.html', club=club, competition=competition), 403
    else:
        try:
            update_booked_places(competition, club, places_required)
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
            club['points'] = int(club['points']) - places_required
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)
        except ValueError as error_message:
            flash(error_message)
            return render_template('booking.html', club=club, competition=competition), 403


@app.route('/showPointBoard')
def view_clubs():
    club_list = sorted(clubs, key=lambda club: club['name'])
    return render_template('point_board.html', clubs=club_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))