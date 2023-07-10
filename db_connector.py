import pymysql
from pypika import Query, Table, Parameter
import datetime as dt


class DBfunc:
    def __init__(self, user, db, password, host):
        self.host = host
        self.port = 3306
        self.user = user
        self.password = password
        self.db = db
        self.conn = None
        self.u = None

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.password, db=self.db,
                                    autocommit=True)
        self.u = Table(f"{self.db}.users2")

    def add_user(self, user_id, user_name):
        """Add a user to the database.

         Parameters:
             user_id: The unique user id of the row in the DB to insert the data into.
             user_name: The username that will be inserted into the DB.
        """
        self.connect()
        self.conn.ping()
        cursor = self.conn.cursor()

        now = dt.datetime.now()

        q = Query.into(self.u).columns('user_id', 'user_name', 'creation_date').insert(Parameter('%s'), Parameter('%s'),
                                                                                  Parameter('%s'))
        cursor.execute(q.get_sql(quote_char=None), (user_id, user_name, now))

    #     # Create the user under the next free id if the specified is taken
    #     while True:
    #         user_id += 1
    #         try:
    #             q = Query.into(self.u).columns('user_id', 'user_name', 'creation_date')\
    #                 .insert(Parameter('%s'), Parameter('%s'), Parameter('%s'))
    #             cursor.execute(q.get_sql(quote_char=None), (user_id, user_name, now))
    #             return user_id
    #         except pymysql.err.IntegrityError:
    #             continue

        cursor.close()
        self.conn.close()

    def get_user(self, user_id):
        """Get a user from the database.

        Parameters:
            user_id: The unique user id of the row in the DB to get the data from.
        Returns:
            username: The data from the user_name column, in the user_id's row.
        """
        self.connect()
        self.conn.ping()
        cursor = self.conn.cursor()

        q = Query.from_(self.u).select("user_name").where(self.u.user_id == f"{user_id}")
        cursor.execute(q.get_sql(quote_char=None))
        username = cursor.fetchone()
        cursor.close()
        self.conn.close()
        if username is None:
            return username
        else:
            return username[0]

    def update_user(self, user_id, user_name):
        """Update a user to the database.

         Parameters:
             user_id: The unique user id of the row in the DB to update the data in.
             user_name: The username that will be updated in the DB.
        """
        self.connect()
        self.conn.ping()
        cursor = self.conn.cursor()

        q = self.u.update().set(self.u.user_name, f'{user_name}').where(self.u.user_id == f'{user_id}')
        cursor.execute(q.get_sql(quote_char=None))

        cursor.close()
        self.conn.close()

    def delete_user(self, user_id):
        """Delete a user from the database.

        Parameters:
            user_id: The unique user id of the row in the DB that will be deleted.
        """
        self.connect()
        self.conn.ping()
        cursor = self.conn.cursor()

        q = Query.from_(self.u).delete().where(self.u.user_id == f"{user_id}")
        cursor.execute(q.get_sql(quote_char=None))

        cursor.close()
        self.conn.close()

    def config(self):
        """Get the configuration from the database

        Returns:
            conf: The configuration data from the database.
        """
        self.connect()
        cursor = self.conn.cursor()

        c = Table(f"{self.db}.config")
        q = Query.from_(c).select("*")
        cursor.execute(q.get_sql(quote_char=None))
        conf = cursor.fetchone()

        cursor.close()
        self.conn.close()
        return conf
