from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from config import Config

app.config.from_object(Config)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
