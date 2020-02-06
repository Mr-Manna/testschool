from config import db,app

from apps.super_admin.models.model import SuperAdmin

# importing routes from app folders
from apps.super_admin import routes as super_admin
from apps.student import routes as student

app.register_blueprint(super_admin.module)
app.register_blueprint(student.module)


@app.cli.command('create_super_admin')
def super_admin():
    """ Flask Command For creating Super Admin"""
    username = input("Enter Your Username: ")
    name = input("Enter Your Name: ")
    email = input("Enter Your Email: ")
    password = input("Enter A Password: ")

    if username is None:
        print("Please enter a username")

    super_admin = SuperAdmin(username,name,email,password)

    try:
        db.session.add(super_admin)
        db.session.commit()
    except:
        print("Admin Creation Failed. Please Try Again")
    else:
        print("Admin Created Successfully. You May Login Now.")


db.init_app(app)
db.create_all()
db.session.commit()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
