from app import create_app,db,mail
from app.models import Users,Posts,Subscriptions,Comments
from flask_script import Manager,Server
from  flask_migrate import Migrate, MigrateCommand
import os

app = create_app('test')

manager = Manager(app)
manager.add_command('server',Server)

manager.add_command('server',Server)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

manager.add_command('server',Server)
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db, mail= mail, Users = Users, Posts = Posts, Subscriptions = Subscriptions, Comments = Comments)

if __name__ == '__main__':
    manager.run()