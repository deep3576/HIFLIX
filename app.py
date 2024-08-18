from flask import Flask, request, jsonify, send_from_directory, render_template
from flask import Flask, request, send_file, abort
import os
from werkzeug.utils import secure_filename
import gzip
import io

##Added IO Module 


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 3000 * 1024 * 1024
MOVIES_FOLDER = 'E:/MoviesDatabase'
#MOVIES_FOLDER = '/Users/inderdeepsingh/Documents/'
THUMBNAILS_FOLDER = './thumbnails'
UPLOAD_FOLDER = 'E:/MoviesDatabase'
#UPLOAD_FOLDER = '/Users/inderdeepsingh/Documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Endpoint to get list of movies
@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = os.listdir(MOVIES_FOLDER)
    return jsonify(movies)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    start = int(request.form.get('start', 0))
    filename = file.filename

    # Define the path for the file
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Open the file in append mode
    with open(file_path, 'ab') as f:
        file.seek(0)
        f.write(file.read())
    
    # Respond with a success message
    return jsonify({'message': 'Chunk uploaded successfully'})




@app.route('/media/<filename>')
def stream_file(filename):
    file_path = os.path.join(MOVIES_FOLDER, filename)
    
    if not os.path.exists(file_path):
        abort(404)
    
    # Handle range requests for streaming
    range_header = request.headers.get('Range', None)
    if range_header:
        size = os.path.getsize(file_path)
        byte1, byte2 = 0, None
        range_match = range_header.split('=')[-1]
        if '-' in range_match:
            byte1, byte2 = range_match.split('-')
            byte1 = int(byte1)
            if byte2:
                byte2 = int(byte2)
            else:
                byte2 = size - 1

        length = byte2 - byte1 + 1
        with open(file_path, 'rb') as f:
            f.seek(byte1)
            data = f.read(length)
        
        response = send_file(
            file_path,
            as_attachment=False,
            conditional=True
        )
        response.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{size}')
        response.headers.add('Accept-Ranges', 'bytes')
        response.headers.add('Content-Length', str(length))
        response.headers.add('Content-Type', 'video/mp4')  # Adjust content type as needed
        return response
    
    return send_file(file_path)







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
