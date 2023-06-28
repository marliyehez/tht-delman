SQLALCHEMY_DATABASE_URI =  'sqlite:///db.sqlite3' #'postgresql://myuser:mypassword@db/mydatabase'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'this is secret'
JOBS = [
    {
        "id": "job1",
        "func": "__main__:update_vaccine_info",
        "trigger": "interval",
        "seconds": 5
        }
]
