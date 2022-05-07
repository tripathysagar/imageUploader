#!/bin/bash
gunicorn -w 2 --bind 127.0.0.1:5000 wsgi:app