from handlers.base import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        self.render("record.html")
