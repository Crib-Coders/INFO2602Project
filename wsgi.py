import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import *
from App.main import create_app
from App.controllers.listing import test_listings
from App.controllers.review import test_reviews
from App.controllers import * # Import your controllers here


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


@app.cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)





#Controller Tests
@app.cli.command("test-controllers")
def test_controllers():
    """Run all controller tests"""
    with app.app_context():
        try:
            # Initialize test data
            db.drop_all()
            db.create_all()
            
            print("=== Testing Auth Controller ===")
            if not test_auth():
                print("✗ Auth tests failed") #even tho it runs the test_auth function, it still prints test failed. 
            
            
            print("\n=== Testing Listing Controller ===")
            if not test_listings():
                print("✗ Listing tests failed")    #even tho it runs the test_listings function, it still prints test failed.
                
            
            print("\n=== Testing Review Controller ===")
            if not test_reviews():
                print("✗ Review tests failed") #even tho it runs the test_reviews function, it still prints test failed.
                
            
            print("\n✓ All tests passed successfully!")
        except Exception as e:
            print(f"✗ Test failed with error: {str(e)}")

