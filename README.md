# website

This is my personal website's source code. I relied on [Digital Ocean's](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)
tutorial when writing this website.

This website is deployed [here](https://saroyr-com-d9a4be4812ff.herokuapp.com/).

For redeployment refer to [Heroku](https://dashboard.heroku.com/apps/saroyr-com/deploy/github).

For domain settings refer to [Network Solutions](https://www.networksolutions.com/my-account/home).

For proxy settings refer to [Cloudflare](https://dash.cloudflare.com/1197453bb02576e0d9c4a5ca6e150eee/saro-harutyunyan.space).

To see logs locally in the terminal (for Windows in Git Bash) run
```commandline
heroku logs --app saroyr-com -n 1500 --force-colors
```

Run locally in Linux terminal as follows:
```
export FLASK_APP=main
export FLASK_ENV=development
flask run
```

Run locally in Windows terminal as follows:
```
$env:FLASK_APP = "main.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
flask run
```

After adding new humors or math problems run the following to repopulate the db:
```commandline
python init_db.py
```

To view a webpage as it looks like on a phone when developing use Responsive Design Mode; for example in Mozilla and Chrome with the shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd>.


TODO: add
* DB visual model,
* Armenian language,
* ggb support,
* creation of Saroy,
* TUMO 3D,
* homework (complex analysis and field theory & multiple integrals)
* secret path that only I will know (maybe); login may also be added; this may be useful for example for adding humors without redeploying the website

for humors
* humor rating capability
* humor dates separately
* filter weak humors

update periodically
* math problems with the new ones,
* favorite music and musicians

consider using KaTeX, LaTeX, MathJax for math