# server.py
from gevent import monkey
monkey.patch_all()

from flask import Flask
from testapp import app

if __name__ == "__main__":
    app.run()
