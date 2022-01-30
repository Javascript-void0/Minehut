from flask import Blueprint, render_template

wiki = Blueprint('wiki', __name__)

@wiki.route('/')
def form():
    return render_template('wiki/wiki.html', table_of_contents=0)