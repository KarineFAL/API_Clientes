from app import app
from flaskext.mysql import MySQL

#Banco de dados Cliente/Endereço

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'cadastro1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

