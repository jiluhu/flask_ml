DB_USER = 'root'
DB_PASSWORD = '123456'
DB_HOST = '118.190.132.107'
DB_DB = 'linkdata20171030'
DB_PORT = 3306
DB_CHAR = "utf8"

DEBUG = True
PORT = 3333
HOST = "118.190.132.107"
SECRET_KEY = "adsfialle323klsflADASF"

ES_HOST = '118.190.132.107'
ES_PORT = 9200

KAFKA_HOST_PORT = '118.190.132.107:9092'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
