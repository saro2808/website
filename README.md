# website

This is my personal website source code.

This website is deployed [here](https://saroyr-com-d9a4be4812ff.herokuapp.com/).

For redeployment refer to [here](https://dashboard.heroku.com/apps/saroyr-com/deploy/github).

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

TODO: add
* contacts,
* references,
* art,
* black mode,
* Armenian language,
* ggb support,
* problem search by tag
* humor search by only humorists or tags.
