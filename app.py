from flask import Flask, request, jsonify, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
MOVIES_FOLDER = 'E:/MoviesDatabase'
THUMBNAILS_FOLDER = 'static/thumbnails'

# Endpoint to get list of movies
@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = os.listdir(MOVIES_FOLDER)
    return jsonify(movies)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file :
        filename = file.filename
        file.save(os.path.join(app.config['MOVIES_FOLDER'], filename))
        return redirect(url_for('index'))

# Endpoint to stream a movie
@app.route('/movies/<movie_name>', methods=['GET'])
def stream_movie(movie_name):
    return send_from_directory(MOVIES_FOLDER, movie_name)

# Endpoint to serve the main HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to serve thumbnails
@app.route('/thumbnails/<thumbnail_name>', methods=['GET'])
def get_thumbnail(thumbnail_name):
    return send_from_directory(THUMBNAILS_FOLDER, thumbnail_name)

if __name__ == '__main__':
    app.run()
