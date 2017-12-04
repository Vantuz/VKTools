#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
import mechanicalsoup
import re

from urllib.parse import urlencode

oauth_url = "https://oauth.vk.com/authorize?display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v=5.60&"

def parseargs():
    parser = argparse.ArgumentParser(description="Tool for acquiring VK API tokens")
    parser.add_argument('login')
    parser.add_argument('password')
    parser.add_argument('--client_id', default=2685278, help="id of app, default is Kate Mobile")
    parser.add_argument('--scope', default='268435455', help="permissions, default is all")

    return parser.parse_args()

if __name__ == '__main__':
    args = parseargs()

    browser = mechanicalsoup.StatefulBrowser()
    login_page = browser.open(oauth_url + urlencode({
        'client_id': args.client_id,
        'scope': args.scope
        }))
    login_form = mechanicalsoup.Form(login_page.soup.select_one('form'))
    login_form.input({"email": args.login, "pass": args.password})
    page2 = browser.submit(login_form, login_page.url)
    if page2.soup.select_one('.service_msg_warning') == None:
        login_form2 = mechanicalsoup.Form(page2.soup.select_one('form'))
        page3 = browser.submit(login_form2, page2.url)

        token = re.search(r"token=([a-zA-Z0-9]+)&", page3.url).group(1)
        print(token)
    else:
        print("Password is not correct or other shit happened, dunno")