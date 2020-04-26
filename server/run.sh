#!/bin/bash
../.env/bin/gunicorn --bind 0.0.0.0:5000 wsgi
