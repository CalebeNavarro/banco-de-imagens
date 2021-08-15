from flask import Flask, request, send_from_directory

from environs import Env
import os

env = Env()
env.read_env()

app = Flask(__name__)

FILES_DIRECTORY = os.environ['FILES_DIRECTORY']
MAX_CONTENT_LENGTH = int(os.environ['MAX_CONTENT_LENGTH'])

@app.post('/upload')
def save_file():
    files = request.files
    file = files['file']
    file_name = file.filename
    file_size = len(file.read())
    file_type = file_name[-4:]
    files_type_format_aprove = ['.png', '.jpg', '.gif']

    if file_type not in files_type_format_aprove:
        return f'Format {file_type} is not allowed.', 415

    if (file_size / 1000) > MAX_CONTENT_LENGTH:
        return f'''File very large, not allowed. Your size file {file_size/1000}kB,
        max upload size file {MAX_CONTENT_LENGTH}kB.''', 413

    ls = os.popen(f'ls {FILES_DIRECTORY}')

    for current_file in ls:
        if current_file[:-1] == file_name:
            return f'File {file_name} alredy exist in system!', 409

    file.save(f'{FILES_DIRECTORY}/{file_name}')

    return f'Arquivo {file_name} foi salvado com sucesso!', 201


@app.get('/files/<tipo>')
@app.get('/files')
def list_files(tipo=None):
    if tipo:
        ls = os.popen(f'ls {FILES_DIRECTORY} | grep {tipo}')
    else:
        ls = os.popen("ls {FILES_DIRECTORY}")

    result = []

    for item in ls:
        result.append(item[:-1])

    return {'all_files': result}, 200


@app.get('/download-zip')
@app.get('/download/<file_name>')
def download_files(file_name=None):
    if file_name:
        try:
            return send_from_directory(
                directory=FILES_DIRECTORY,
                path=f'{file_name}',
                as_attachment=True
            ), 200
        except:
            return 'File name not found in system.', 404

    query = request.args
    compression_rate = query.get('compression_rate')
    file_type = query.get('file_type')

    if not compression_rate:
        compression_rate = 3
    if not file_type:
        file_type = ''

    repo_name = f'{compression_rate}_{file_type}.gz{compression_rate}'

    os.system(f'tar -rv -f /tmp/{repo_name} {FILES_DIRECTORY}/*{file_type}')

    ls = os.popen(f'ls {FILES_DIRECTORY}/*{file_type}')

    for item in ls:
        if item:
            return send_from_directory(
                directory='/tmp',
                path=f'{repo_name}',
                as_attachment=True
            ), 200

    return 'Not Found any file', 404
