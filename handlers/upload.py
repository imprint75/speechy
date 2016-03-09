import os
import random
import string
import wave
import logging

from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


class UploadHandler(BaseHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        chars = string.ascii_lowercase + string.digits
        fname = ''.join(random.choice(chars) for x in range(6)) + extension

        output_file = wave.open("uploads/" + fname, 'wb')
        input_file = wave.open(bytes(file1['body']))
        output_file.setnchannels(input_file.getnchannels())
        output_file.setsampwidth(input_file.getsampwidth())
        output_file.setframerate(input_file.getframerate())
        output_file.writeframesraw(input_file)

        self.finish("file" + fname + " is uploaded")
