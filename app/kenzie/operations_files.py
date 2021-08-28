from flask import send_from_directory

import os

FILES_DIRECTORY = '/home/kimanc11/kenzie/q3/sprint_2/banco_de_imagens/imagens_de_teste'
MAX_CONTENT_LENGTH = 1000


def send_to_directory(file_name: str):
    try:
        return send_from_directory(
            directory=FILES_DIRECTORY,
            path=f'{file_name}',
            as_attachment=True
        ), 200
    except:
        return {'msg': 'File name not found in system.'}, 404


def ls_files(directory: str):
    return os.popen(f'ls {directory}')
