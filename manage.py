import sys
import os
import coverage
from app import create_app
from app.models.user import User
COV = coverage.coverage(branch=True, include='app/*')
COV.start()

app = create_app("dev")

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    exit_code = unittest.TextTestRunner().run(tests).wasSuccessful()
    COV.stop()
    COV.save()
    COV.report()
    sys.exit(0 if exit_code else 1)