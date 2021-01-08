FROM python:3.6.2-onbuild

ENTRYPOINT ["python3"]

CMD ["/usr/local/bin/gunicorn", "--config=gunicorn.py", "wsgi:application"]
