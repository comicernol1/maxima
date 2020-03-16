import os

ROOT = os.path.dirname(__file__)

settings = {
    'template_path': os.path.join(ROOT, "req"),
    'static_path': os.path.join(ROOT, "static"),
    'static_url_prefix': '/static/',
    "cookie_secret": str(os.environ["COOKIE_SECRET"]),
    "login_url": "/sign_in/",
    "xsrf_cookies": True,
}
