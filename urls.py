from handlers.index import IndexHandler
from handlers.upload import UploadHandler, StatusHandler

url_patterns = [
    (r"/", IndexHandler),
    (r"/upload", UploadHandler),
    (r"/status", StatusHandler)
]
