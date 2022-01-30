from flask import Flask, render_template
from views.about import about
from views.wiki import wiki

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(about, url_prefix='/about')
app.register_blueprint(wiki, url_prefix='/wiki')

@app.route('/')
def index():
    return render_template('index.html', table_of_contents=1)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', table_of_contents=1), 404

if __name__ == '__main__':
    app.debug = True
    app.run()