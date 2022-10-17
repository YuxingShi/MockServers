#!/bin/bash
/usr/local/python3.6/bin/gunicorn app:app -w 1 -b 0.0.0.0:8857 -D