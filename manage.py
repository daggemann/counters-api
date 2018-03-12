import unittest

from flask.cli import FlaskGroup

from api import create_app, db

app = create_app()

cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    """ Recreate database."""
    db.drop_all()
    db.create_all()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('api/tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
