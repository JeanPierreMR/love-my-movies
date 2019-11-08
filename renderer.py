#coding=utf-8
from flask import Flask, render_template, request, redirect
import  json, requests, redis
api_key = "bb753f5503816fa1b10cb0488e8016d7"
app = Flask(__name__)
server = redis.Redis(host='redis', port=6379)
server.set("request", requests.get('https://api.themoviedb.org/3/movie/550?api_key='+api_key).content)
server.set("request_trending", (requests.get("https://api.themoviedb.org/3/trending/movie/week?api_key="+api_key ).content))
server.set("request_discover", (requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + api_key + "&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1").content))

for movie in json.loads(server.get("request_trending"))['results']:
    server.set(movie['id'], int(movie['vote_count']))
for movie in json.loads(server.get("request_discover"))['results']:
    server.set(movie['id'], int(movie['vote_count']))
@app.route("/")
def home():
    return render_template("index.html", trending = json.loads(server.get("request_trending")), discover = json.loads(server.get("request_discover")), server = server)

@app.route("/upvote", methods=['POST'])
def downvote():
    if request.method == 'POST':
        try:
            server.incr(request.form.get('vote'))
        except:
            server.set(request.form.get('vote'), 1)
      
    return redirect("/")

@app.route("/downvote", methods=['POST'])
def upvote():
    if request.method == 'POST':
        try:
            server.decr(request.form.get('vote'))
        except:
            server.set(request.form.get('vote'), -1)
        
    return redirect("/")

if __name__ == "__main__":
    debug=True
    app.run(host="0.0.0.0",debug=debug)



