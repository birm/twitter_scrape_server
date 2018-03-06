import TwitterAPI
import flask
import json
import os.path

app=flask.Flask(__name__)

# filename?
fn = 'config.json.example'
if os.path.isfile('config.json'):
    fn = 'config.json'


print("opening fn: " + fn)
with open(fn) as json_data_file:
    config = json.load(json_data_file)

tweet_limit = config["tweet_limit"]

#AUTH
api = TwitterAPI.TwitterAPI(config["consumer_key"], config["consumer_secret"], config["access_token_key"], config["access_token_secret"])

# HELPERS
def statuses(username):
    r = api.request("statuses/user_timeline", {"count": tweet_limit, "screen_name": username})
    return r.get_iterator()

#def statuses(username):
#    return [{'egg': 'yes', 'ham': 'yes', 'spam': 'no'}, {'egg': 'yes', 'ham': 'yes', 'spam': 'no'}, {'egg': 'yes', 'ham': 'yes', 'spam': 'no'}]


# ROUTES

@app.route("/")
def about_route():
    docstr = """--WELCOME--
    See:
    /json/user/<username>
    /csv/user/<username>

    -rb
    """
    return docstr

@app.route("/json/user/<username>")
def json_route(username):
    s = [t for t in statuses(username)]
    rsp = flask.make_response(json.dumps(s))
    rsp.mimetype='application/json'
    return rsp

@app.route("/csv/user/<username>")
def csv_route(username):
    s = [",".join([username, t["text"], str(t["id"]), str(t["favorite_count"]), str(t["retweet_count"]) ]) for t in statuses(username)]
    hdr = "username, text, id, fav_count, rt_count\n"
    rsp = flask.make_response(hdr + "\n".join(s))
    cd = 'attachment; filename=mycsv.csv'
    rsp.headers['Content-Disposition'] = cd
    rsp.mimetype='text/csv'
    return rsp

if __name__ == "__main__":
    app.run()
