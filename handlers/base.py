import tornado.web
import tornado.websocket

import logging
logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    pass


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        logger.info("WebSocket opened")

    def on_close(self):
        logger.info("WebSocket closed")
