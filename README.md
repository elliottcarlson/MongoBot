# Setup

Clone the code locally.

Create an `.env` file, or set your environment variables for the following
secrets:

* SLACK_TOKEN
* IRC_PASSWORD
* REDIS_URL
* REDDIT_CLIENT_ID
* REDDIT_CLIENT_SECRET

Create a virtual environment.

```
$ virtualenv venv
$ source venv/bin/activate
```

Install the requirements.txt file via pip.

```
$ pip install -r requirements.txt
```

Run the bot.

```
$ ./run.py
```

# Testing

Unit tests can be run via:

```
$ ./run.py --test
```

Code coverage can be calculated with:

```
$ ./run.py --test --coverage
```

Code coverage can generate a visual HTML file:

```
$ ./run.py --test --coverage
...
$ coverage html
$ open htmlcov/index.html
```
