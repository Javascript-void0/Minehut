from flask import Blueprint, render_template

about = Blueprint('about', __name__)

@about.route('/')
def form():
    return render_template('about.html', table_of_contents=1)