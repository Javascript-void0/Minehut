from flask import Blueprint, render_template

faq = Blueprint('faq', __name__)

@faq.route('/')
def form():
    return render_template('faq.html', table_of_contents=1)