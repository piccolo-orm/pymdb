# PyMDb

Welcome to the Python Movie Database!

Built using Piccolo, Piccolo Admin, and FastAPI.

Created for a presentation given at PyData Global 2021.

## Running it

Create a Postgres database called 'pymdb' (see `piccolo_conf.py` for the details).

```bash
pip install -r requirements.txt
piccolo migrations forwards all
piccolo movies load_data
piccolo user create
```

To run the server:

```bash
python main.py
```

Then load `localhost:8000` in your browser. `localhost:8000/admin` shows the admin interface, and `localhost:8000/docs` shows the Swagger docs.

## Creating something similar

To create your own app like this from scratch, start with the following:

```bash
pip install piccolo['all']
piccolo asgi new
```
