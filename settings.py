import tornado
import tornado.template
import os
from tornado.options import define, options

# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="debug mode")

tornado.options.parse_command_line()

TEMPLATE_ROOT = path(ROOT, 'templates')


settings = dict()
settings['debug'] = options.debug
settings['port'] = options.port
settings['cookie_secret'] = "as890fasd90f8asdf9a0-s982rhh"
settings['xsrf_cookies'] = False
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)
