from sqlalchemy.engine import URL

class Config:
    SECRET_KEY = 'panchayat_secret_key_123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # By using URL.create, you can type your password exactly as it is 
    # (with the @ symbol) and Python will connect without any errors!
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="Sakshi@yash2005",
        host="localhost",
        database="PANCHAYAT"
    )
