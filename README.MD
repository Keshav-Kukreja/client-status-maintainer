<h1>Client Status Maintainer</h1>

It is a web app created to maintain return status of clients, it relies on Flask for both frontend and backend.

<h2 style="color:red;">Note: Run it in a development environment</h2>

To try it, follow below steps :

first create a virtual environment 

```
python -m venv env
```

Now activate it

windows command

```
env\scripts\activate.ps1
```

linux command

```
env/bin/actvate
```

Install dependencies

```
pip install -r requirements.txt
```

Start flask app using

```
python app.py
```

Todo :
- Export page f.y options needs to be fetched from the database
- make it responsive for small devices
- Consider separating the frontend and backend to enhance maintainability
- find other issues to be fixed

**Open issue, if you encounter bug**