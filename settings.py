import os

ROOT = os.path.dirname(__file__)

settings = {
    'template_path': os.path.join(ROOT, "req"),
    'static_path': os.path.join(ROOT, "static"),
    'static_url_prefix': '/static/',
}
