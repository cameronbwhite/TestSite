from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template
from flask_oauth import OAuth

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import secrets

# configuration
DEBUG = False

# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = secrets.SECRET_KEY
oauth = OAuth()

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1.1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key=secrets.CONSUMER_KEY,
    consumer_secret=secrets.CONSUMER_SECRET,
)

@twitter.tokengetter
def get_twitter_token():
    return (secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)

@app.route("/")
@app.route("/<username>")
def home(username=None):
    if not username:
        resp = twitter.get('statuses/user_timeline.json')
    else:
        resp = twitter.get('statuses/user_timeline/{}.json'.format(username))
    return render_template('layout.html', tweets=resp.data)



if __name__ == '__main__':
    app.run()
