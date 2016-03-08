import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from urls import url_patterns
from settings import settings

logger = logging.getLogger(__name__)


class App(tornado.web.Application):
    def __init__(self, url_patterns, **settings):
        self._url_patterns = url_patterns
        self._settings = settings
        tornado.web.Application.__init__(self, self._url_patterns, **self._settings)

    def show_config(self):
        debug = self._settings.get('debug', True)

        if debug:
            logger.info("***** Settings *****\n{}".format(self._settings))
            logger.info("***** URL Patterns *****\n{}".format(self._url_patterns))


def main():
    app = App(url_patterns, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    logger.info("***** START *****")
    app.show_config()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
