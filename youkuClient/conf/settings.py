import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

UPLOAD_MOVIE_PATH = os.path.join(BASE_PATH, 'upload_movies')

DOWNLOAD_MOVIE_PATH = os.path.join(
    BASE_PATH, 'download_movies')
