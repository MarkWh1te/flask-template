import sys
import coverage
from app import create_app
COV = coverage.coverage(branch=True, include='app/*')

app = create_app("dev")

@app.cli.command()
def test():
    """Run the unit tests."""
    COV.start()
    import unittest
    tests = unittest.TestLoader().discover('tests')
    exit_code = unittest.TextTestRunner().run(tests).wasSuccessful()
    COV.stop()
    COV.save()
    sys.exit(0 if exit_code else 1)