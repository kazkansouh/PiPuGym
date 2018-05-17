#! /usr/bin/python3

import requests
import time
import argparse

# these are the urls used for logging in/accessing the members area.
url1 = "https://www.puregym.com/login/"
url2 = "https://www.puregym.com/api/members/login/"
url3 = "https://www.puregym.com/members/"

# string that prefixes the verification token embedded in login page
tokenmatch = 'input name="__RequestVerificationToken" type="hidden" value='
# string that prefixes the number of active people in gym
match = ', there are <span class="heading heading--level3 secondary-color margin-none">'

# can be used to disable tls certificate checks, useful for debugging
enable_verify=True

def login(email, pin) :
    "Login to website, and return a cookie jar if succesfull, None otherwise."
    print("Attempting login for " + email)

    # get a new session
    r = requests.get(url1, verify=enable_verify)

    # save the cookies
    jar = r.cookies

    # dirty hack to extract the verification token, better to parse into dom
    token = r.text[r.text.find(tokenmatch) + len(tokenmatch):].split('"')[1]

    # try to login
    data = {
        "email": email,
        "pin": pin,
        "associateAccount": "false"
    }
    headers = {'__RequestVerificationToken': token}
    r = requests.post(url2, json = data, headers = headers, cookies=jar, allow_redirects=False, verify=enable_verify)
    if r.status_code != 200 : # expect 302 if not successful
        print("failed to authenticate")
        print(r.text)
        return None

    #print(r.cookies)
    jar.update(r.cookies)

    return jar

def getparams() :
    "Extract command line arguments for email and pin"
    parser = argparse.ArgumentParser(description='Get number of people in gym from PureGym members page.')
    parser.add_argument('email', help='email address used to login to website')
    parser.add_argument('pin', help='pin used to login to website')
    return parser.parse_args()

def run() :
    "Main loop"
    params = getparams()
    jar = requests.cookies.RequestsCookieJar()
    last_action_login = False

    while True :
        r = requests.get(url3, cookies=jar, allow_redirects=False, verify=enable_verify)
        if r.status_code != 200 : # will get 302 if not logged in
            if last_action_login :
                print("Login loop detected, exiting.")
                break
            last_action_login = True
            jar = login(params.email, params.pin)
            if jar is None :
                break
        else :
            last_action_login = False
            loc = r.text.find(match)
            if loc > 0 :
                people = r.text[loc + len(match):loc + len(match) + 30].split(' ')[0]
                print(time.asctime() + ', ' + people)
                time.sleep(120)
            else :
                # should not happen in normal situations
                print("could not find match")
                print(r.text)
                break

if __name__ == "__main__" :
    run()
