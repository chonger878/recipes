from flask import Flask, render_template
import os
app = Flask(__name__)
app.secret_key= {{ os.environ["SECRET_KEY"] }}