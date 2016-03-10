from handlers.index import IndexHandler
from handlers.upload import UploadHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/upload", UploadHandler),
]
