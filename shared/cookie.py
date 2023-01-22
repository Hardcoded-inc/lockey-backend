import logging
from http.cookies import SimpleCookie

def gen(domain, expiration, cookie_name, value):
    cookie = SimpleCookie()
    cookie[cookie_name] = value
    cookie[cookie_name]['httponly'] = "yes"
    cookie[cookie_name]['domain'] = domain
    cookie[cookie_name]['expires'] = expiration
    cookie[cookie_name]['path'] = "/"

    h = str(cookie).split(": ")

    return {h[0]: h[1]}


def read(req):
    cookie = SimpleCookie()
    cookie.load(req.headers['Cookie'])

    logging.warn(cookie)

    return cookie
