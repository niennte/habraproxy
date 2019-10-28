## A simple http proxy server micro app
serving pages from [https://habr.com](https://habr.com) modified as described here: [https://github.com/ivelum/job/blob/master/code_challenges/python.md](https://github.com/ivelum/job/blob/master/code_challenges/python.md)

### Running locally

```

# Python: assuming 3.7 installed (and activated if multiple versions used)
$ python -V
Python 3.7.0

# SSL: assuming certificates installed
# On Mac OSx, open Applications/'Python 3.7' and double click on 'Install Certificates.command', or run:
$ /Applications/Python\ 3.7/Install\ Certificates.command


# Install dependencies (BeautifulSoup parser)
$ pip install beautifulsoup4

# Clone the repo
$ git clone [repo] [path]
$ cd [path]

# Run the app:
# - when prompted, enter preferred port and press Enter, or press Enter to use the default of 8080, as follows:
$ python server.py
[*] Enter Listening Port Number: [8080] ...[Enter]

Starting httpd server on 127.0.0.1:8080
...

```
The server should now be running on localhost port of your choice, by default: [http://127.0.0.1:8080](http://127.0.0.1:8080)


### Testing
```
$ cd [path]
$ python test.py
```