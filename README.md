# PocketForce

An awesome efficient http/https multithreaded bruteforcer

## Usage:

Below are the list of command line options (some are required some are optional)

```bash

-o #target url to POST to
-p #path to password file
--param #a form parameter to pass e.g --param user=admin
-b #failure reponse string (optional) defaults to 'Bad login'
-t #number of threads (optional) defaults to 1
-c #cookie data to send in header (optional)

```

## Example

The below example posts to example.com/login and loops through all passwords in pass.txt by using 5 threads for more efficient I/O processing. It sends the form data email=test@live.com&password=<the looped password>. It then checks the response string for any occurences of "Invalid password" if it doesn't exist then the program finishes with the printed password, if not it continues the loop

```bash

python pocketforce.py -o https://example.com/login -p pass.txt --param email=test@live.com -b "Invalid password" --param password=%PASS% -t 5

```

Note that you must place '%PASS%' without the quotation on the --param option you would like to inject the passwords from the text file


#### Disclaimer
This software is made for penetration testing and ethical white hat hacking only, please do not use it for illegal purposes as I take no responsibility in the way it is used