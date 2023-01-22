import logging
from http.cookies import SimpleCookie

def gen(domain, expiration, cookie_name, value):
    cookie = SimpleCookie()
    cookie[cookie_name] = value
    cookie[cookie_name]['httponly'] = "yes"
    cookie[cookie_name]['domain'] = domain
    cookie[cookie_name]['expires'] = expiration
    cookie[cookie_name]['path'] = "/"

    morsel = str(cookie).split(": ")
    return {morsel[0]: morsel[1]}


def read(req, name):
    cookies_string = req.headers.get('Cookie')
    if cookies_string:
        cookies_dict = parse_cookies(cookies_string)
        return cookies_dict.get(name)
    else:
        return None


def parse_cookies(c_string):
    c_dict = {}
    c_list = c_string.split("; ")
    for cookie in c_list:
        [cookie_name, cookie_val] = cookie.split("=")
        c_dict[cookie_name] = cookie_val

    return c_dict
