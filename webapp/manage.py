#! /usr/bin/env python

import os
from app.utils import scopus
from app.utils.research import funding
from app import create_app, db
from app.models import (User, SystemRole, Department, FacultyInfo,
                            RoomDirectory, Building, Job, Contact,
                            Education, Degree, ForumRole, AcademicPosition)
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User,
                    Department=Department,
                    SystemRole=SystemRole,
                    ForumRole=ForumRole,
                    FacultyInfo=FacultyInfo,
                    RoomDirectory=RoomDirectory,
                    Building=Building,
                    Job=Job,
                    Contact=Contact,
                    Education=Education,
                    Degree=Degree,
                    AcademicPosition=AcademicPosition,
                )

@manager.command
def update_scopus(year):
    '''
    Update the Scopus research publication database.
    '''
    scopus.update(year)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(use_debugger=True))


if __name__=='__main__':
    manager.run()
