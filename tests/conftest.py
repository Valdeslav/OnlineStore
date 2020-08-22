import pytest
from flask import Flask

from app import make_api

@pytest.fixture(scope="module")
def init_test_client():
	app = Flask(__name__)
	make_api(app)
	app.testing = True
	return app.test_client()
