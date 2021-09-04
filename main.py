from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        site = request.form['sitename']
        if not site.startswith("http"):
            site = "http://" + site
        try:
            r = requests.get(site)
            if r.status_code == 200:
                status = "up"
            else:
                status = "down"
            if site.startswith("http"):
                if site.startswith("https://"):
                    site = site[7:]
                else:
                    site = site[6:]
            site = site + " " + status
        except:
            site = f"Error! Invalid URL"
        site = site.replace("/", "")
        return redirect(url_for('sitecheck', site=site))
    else:
        return render_template('index.html')


@app.route('/<site>')
def sitecheck(site):
    if site == "Error! Invalid URL":
        return render_template("error.html")
    else:
        data = site.split(" ")
        return render_template("siteCheck.html", site=data[0], status=data[1])


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6969)
