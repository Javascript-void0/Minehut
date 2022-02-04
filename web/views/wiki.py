from flask import Blueprint, render_template

wiki = Blueprint('wiki', __name__)

@wiki.route('/')
def form():
    return render_template('wiki.html', table_of_contents=0)

@wiki.route('/mob-drop-rates')
def mob_drop_rates():
    return render_template('mob-drop-rates.html', table_of_contents=1)