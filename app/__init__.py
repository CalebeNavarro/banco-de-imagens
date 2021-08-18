from flask import Flask, request, send_from_directory, safe_join

from .kenzie.operations_files import send_to_directory, ls_files

from datetime import datetime

from environs import Env

import os

from werkzeug.utils import secure_filename

env = Env()
env.read_env()

app = Flask(__name__)

FILES_DIRECTORY = os.environ['FILES_DIRECTORY']

MAX_CONTENT_LENGTH = int(os.environ['MAX_CONTENT_LENGTH'])

UPLOAD_DIRECTORY = './imagens_de_teste'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)


@app.post('/upload')
def save_file():
    """Function that save a file in system

    Parameters:
    Dont have parameter

    Obs:
    Just accept .png, .jpg and .gif and need be less than 1000kB.

    Returns:
    Dict: Return string message

   """

    files = request.files

    files_names = list(files)

    if len(files_names) == 0:
        return {'msg': 'Envie pelo menos 1 arquivo.'}, 406

    uploaded_list = []

    files_type_format_aprove = ['.png', '.jpg', '.gif']

    for f in files_names:
        current_file = files[f]

        file_name = secure_filename(current_file.filename)

        file_size = len(current_file.read())

        file_type = file_name[-4:]

        if file_type not in files_type_format_aprove:
            return {'msg': f'Format {file_type} is not allowed.'}, 415
        elif (file_size / 1000) > MAX_CONTENT_LENGTH:
            return {'msg': f'''File very large, not allowed. Your size file {file_size/1000}kB,
            max upload size file {MAX_CONTENT_LENGTH}kB.'''}, 413
        elif os.path.exists(f'{UPLOAD_DIRECTORY}/{file_name}'):
            return {'msg': f'File {file_name} alredy exist in system!'}, 409
        else:
            file_path = safe_join(FILES_DIRECTORY, file_name)

            current_file.save(file_path)

            uploaded_list.append(file_name)

    return {'msg': f'File(s) {uploaded_list} saved with success!'}, 201


@app.get('/files/<tipo>')
@app.get('/files')
def list_files(tipo=None):
    """Function that list all files of the system

    Parameters:
    Any or name file or type file

    Returns:
    Dict: Return string message contain all files names or empty array if
    dont find any file

    """

    if tipo:
        ls = os.popen(f'ls {FILES_DIRECTORY} | grep {tipo}')
    else:
        ls = ls_files(FILES_DIRECTORY)

    result = []

    for item in ls:
        result.append(item[:-1])

    return {'all_files': result}, 200


@app.get('/download/<file_name>')
def donwload_file(file_name=None):
    return send_to_directory(file_name)


@app.get('/download-zip')
def download_files():
    """Function to download all files in .gz or a specific type

    Parameters:
    Any or you can specific file_type and compression_rate in url   

    Returns:
    Download: download file(s) in .gz

    """
    query = request.args

    compression_rate = query.get('compression_rate', 1)
    file_type = query.get('file_type', '')

    file_name = f'{datetime.now()}.gz{compression_rate}'.replace(' ', '_')

    os.system(f'tar -rv -f /tmp/{file_name} {UPLOAD_DIRECTORY}/*{file_type}')

    ls = os.popen(f'ls {UPLOAD_DIRECTORY}/*{file_type}')

    for item in ls:
        if item:
            return send_from_directory(
                directory='/tmp',
                path=f'{file_name}',
                as_attachment=True
            ), 200

    return {'msg': 'Not found any file'}, 404
