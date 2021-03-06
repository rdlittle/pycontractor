import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import flask_script
from flask_script import Manager, Server
from ..contractor import app

manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    #host = 'mustang.littleacres.lan',
    host = '0.0.0.0',
    port = int(os.getenv('PORT', 5050))
))

if __name__ == '__main__':
    manager.run()
