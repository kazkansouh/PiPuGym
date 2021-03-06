#! /usr/bin/python3

import requests
import time
import argparse
import spidev
import traceback

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
    if r.status_code == 524 :
        print("timout while authenticating")
        return None
    elif r.status_code != 200 : # expect 302 if not successful
        print("failed to authenticate http response code: " + str(r.status_code))
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

def writespi(people, spi) :
    "convert people to an numeric value between 0 to 8 and write to spi"
    val = 0xFF
    if people < 20 :
        val = 0x00
    elif people <= 35 :
        val = 0x01
    elif people <= 50 :
        val = 0x03
    elif people <= 70 :
        val = 0x07
    elif people <= 90 :
        val = 0x0F
    elif people <= 110 :
        val = 0x1F
    elif people <= 125 :
        val = 0x3F
    elif people <= 135 :
        val = 0x7F
    else :
        val = 0xFF
    spi.xfer([val])

def run(spi) :
    "Main loop"
    params = getparams()
    jar = requests.cookies.RequestsCookieJar()
    last_action_login = 0
    error_counter = 0

    while True :
        r = requests.get(url3, cookies=jar, allow_redirects=False, verify=enable_verify)
        if r.status_code != 200 : # will get 302 if not logged in
            print("Request failed with code: " + str(r.status_code))
            if last_action_login > 3 :
                print("Login loop detected, exiting.")
                break
            time.sleep(15 * last_action_login)
            last_action_login += 1
            jar = login(params.email, params.pin)
        else :
            last_action_login = 0
            loc = r.text.find(match)
            if loc > 0 :
                error_counter = 0
                people = r.text[loc + len(match):loc + len(match) + 30].split(' ')[0]
                print(time.asctime() + ', ' + people)
                if people == "Fewer" :
                    people = "0"
                writespi(int(people), spi)
                time.sleep(120)
            else :
                # should not happen in normal situations
                error_counter = error_counter + 1
                print("could not find match")
                print(r.headers)
                print(r.text)
                if error_counter > 5 :
                    break
                else :
                    print("retrying")
                    time.sleep(10)

if __name__ == "__main__" :
    spi = spidev.SpiDev()
    spi.open(0,0)
    try :
        run(spi)
    except :
        print("An error has occurred")
        traceback.print_exc()
    finally :
        x = 1
        while True :
            spi.xfer([x])
            x = x << 1
            if x > 0x80 :
                x = 1
            time.sleep(0.25)
