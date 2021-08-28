from werkzeug.datastructures import FileStorage

from werkzeug.utils import secure_filename

import os

MAX_CONTENT_LENGTH = int(os.environ['MAX_CONTENT_LENGTH'])

UPLOAD_DIRECTORY = './imagens_de_teste'


class Files:
    # file_name = secure_filename(current_file.filename)

    def __init__(self, current_file):
        self.current_file = current_file

    def teste(self):
        print(self.current_file) 
        return 'a'   

    def format_type_validated(self):

        files_type_format_aprove = ['.png', '.jpg', '.gif']

        file_name = secure_filename(self.current_file.filename)

        file_type = file_name[-4:]

        if file_type not in files_type_format_aprove:

            raise TypeError(f'Format {file_type} is not allowed.')

    def size_file_validated(self):

        file_size = len(self.current_file.read())

        if (file_size / 1000) > MAX_CONTENT_LENGTH:

            raise MemoryError(f'''File very large, not allowed. Your size file {file_size/1000}kB,
            max upload size file {MAX_CONTENT_LENGTH}kB.''')

    def file_exist_system(self):

        file_name = secure_filename(self.current_file.filename)

        if os.path.exists(f'{UPLOAD_DIRECTORY}/{file_name}'):

            raise FileExistsError(f'File {file_name} alredy exist in system!')
