from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
MOVIES_FOLDER = 'path/to/movies/folder'

# Endpoint to get list of movies
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = os.listdir(MOVIES_FOLDER)
    return jsonify(movies)

# Endpoint to stream a movie
@app.route('/movies/<movie_name>', methods=['GET'])
def stream_movie(movie_name):
    return send_from_directory(MOVIES_FOLDER, movie_name)

if __name__ == '__main__':
    app.run(debug=True)
