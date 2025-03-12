#!/bin/bash

python src/main.py migrate

exec gunicorn -c "gunicorn_config.py" core.wsgi
