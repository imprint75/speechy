import os
import random
import string
import wave
import logging

from handlers.base import BaseHandler

logger = logging.getLogger(__name__)


def get_path(filename):
    from settings import UPLOAD_ROOT
    return os.path.join(UPLOAD_ROOT, filename)


class UploadHandler(BaseHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        chars = string.ascii_lowercase + string.digits
        fname = ''.join(random.choice(chars) for x in range(6)) + extension
        file_path = get_path(fname)

        with open(file_path, 'wb') as f:
            f.write(file1['body'])

        with wave.open(file_path, 'r') as w:
            logger.info("***** WAV INFO *****")
            logger.info(w.getparams())

        self.finish("file" + fname + " is uploaded")
