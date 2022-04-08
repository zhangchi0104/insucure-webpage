# Insecure-Website

## Install

### Pre-requisite

`python` >= 3.8.10

\*\*\[OPTIONAL\] Create Virtual Env

```
$ python3 -m venv .venv
$ source .\venv\bin\activate
(.venv) $
```

Install dependencies

```
(.venv) $ python3 -m pip install -r requirements.txt
```

### The main site

```
python3 app.py
```

### CSRF-Attacker

Using docker is recommanded

```
(.venv) $ cd csrf_attacker
(.venv) $ python3 app.py
```

## Deployment with docker

### The main webpage

```
$ docker run \
  -p 5000:5000 \
  -e CSRF_ATTACKER_URL=<your_url> \ # OPTIONAL see CUSTOMISATION section
  --rm zhangchi0104/insecure-website
```

### The CSRF Attacker

```
$ docker run \
  -p 8000:8000 \
  -e CSRF_ENDPOINT=<your_main_site_url> \ # OPTIONAL see CUSTOMISATION section
  --rm zhangchi0104/csrf-attacker
```

## CUSTOMISATION

- `CSRF_ENDPOINT`: URL used by CSRF Attacker Site to send the malious request, by default is `http://127.0.0.1:5000/csrf-attack`
- `CSRF_ATTACKER_URL`: the malious URL in CSRF Attack. By default is `https://csrf-attacker.azurewebsites.net`
  - The azurewebsite may not be available, deploy your own is recommanded
