import sys
from app import create_app

app = create_app("dev")

@app.cli.command()
# @click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    exit_code = unittest.TextTestRunner().run(tests).wasSuccessful()
    sys.exit(0 if exit_code else 1)