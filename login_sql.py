''' py'''
from hashlib import md5

import pymysql.cursors
F_NAME = 'f_name'
L_NAME = 'l_name'
USERNAME = 'username'
EMAIl = 'email'
PASSWORD = 'password'

class LoginPage(object):

    def open_connection(self):
        '''ewfew'''
        #creating connection
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     db='login_twitter',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection


    def sign_up(self, f_name, l_name, username, email, password):
        '''create user'''
        username_lookup = self.look_up(username=username)
        email_lookup = self.look_up(email=email)

        if username_lookup is not None:
            return 'Sorry username taken'
        elif email_lookup is not None:
            return 'Your email address is already register.'
       # Connect to the database
        connection = self.open_connection()
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `login` VALUES (%s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql, (f_name, l_name, username, email, password))
            except Exception as e:
                connection.close()
                return e
            connection.commit()
            connection.close()
        return True

    def look_up(self, username='', email=''):
        '''looking for username'''
        # Connect to the database
        connection = self.open_connection()
        if email:
            check = email
            condition = "email = %s"
        else:
            check = username
            condition = "USERNAME = %s"
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT USERNAME, Email, PASSWORD FROM `LOGIN` WHERE " + condition
            cursor.execute(sql, (check))
            result = cursor.fetchone()
            connection.close()
            return result

    def sign_in(self, username, password):
        '''validating credentials'''
        db_lookup = self.look_up(username=username)
        if db_lookup is not None:
            if db_lookup['PASSWORD'] == password:
                return True
            else:
                return 'Please check your username, password'
        else:
            return 'Please check your username, password'

c = LoginPage()
#print c.look_up('','sendmanu@yahoo.co.in')
#print c.sign_up('sindhoor','mandava', 'sindhoor', 'msindhoor@yahoo.co.in', 'iamtoogood')
#print c.sign_in('barewolf','iamtoogood')
