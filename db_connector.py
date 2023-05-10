import pymysql
from pypika import Query, Table, Parameter
import datetime as dt

schema_name = '***REMOVED***'
u = Table(f"{schema_name}.users2")


def add_user(user_id, user_name):
    """Add a user to the database.

     Parameters:
         user_id: The unique user id of the row in the DB to insert the data into.
         user_name: The username that will be inserted into the DB.
    """
    conn = pymysql.connect(host='sql7.freemysqlhosting.net', port=3306, user='***REMOVED***', password='***REMOVED***',
                           db='***REMOVED***')
    conn.autocommit(True)
    cursor = conn.cursor()

    now = dt.datetime.now()

    q = Query.into(u).columns('user_id', 'user_name', 'creation_date').insert(Parameter('%s'), Parameter('%s'),
                                                                              Parameter('%s'))
    cursor.execute(q.get_sql(quote_char=None), (user_id, user_name, now))

#     # Create the user under the next free id if the specified is taken
#     while True:
#         user_id += 1
#         try:
#             q = Query.into(u).columns('user_id', 'user_name', 'creation_date')\
#                 .insert(Parameter('%s'), Parameter('%s'), Parameter('%s'))
#             cursor.execute(q.get_sql(quote_char=None), (user_id, user_name, now))
#             return user_id
#         except pymysql.err.IntegrityError:
#             continue

    cursor.close()
    conn.close()


def get_user(user_id):
    """Get a user from the database.

    Parameters:
        user_id: The unique user id of the row in the DB to get the data from.
    Returns:
        username: The data from the user_name column, in the user_id's row.
    """
    conn = pymysql.connect(host='sql7.freemysqlhosting.net', port=3306, user='***REMOVED***', password='***REMOVED***',
                           db='***REMOVED***')
    cursor = conn.cursor()

    q = Query.from_(u).select("user_name").where(u.user_id == f"{user_id}")
    cursor.execute(q.get_sql(quote_char=None))
    username = cursor.fetchone()
    cursor.close()
    conn.close()
    try:
        return username[0]
    except TypeError:
        return username


def update_user(user_id, user_name):
    """Update a user to the database.

     Parameters:
         user_id: The unique user id of the row in the DB to update the data in.
         user_name: The username that will be updated in the DB.
    """
    conn = pymysql.connect(host='sql7.freemysqlhosting.net', port=3306, user='***REMOVED***', password='***REMOVED***',
                           db='***REMOVED***')
    conn.autocommit(True)
    cursor = conn.cursor()

    q = u.update().set(u.user_name, f'{user_name}').where(u.user_id == f'{user_id}')
    cursor.execute(q.get_sql(quote_char=None))

    cursor.close()
    conn.close()


def delete_user(user_id):
    """Delete a user from the database.

    Parameters:
        user_id: The unique user id of the row in the DB that will be deleted.
    """
    conn = pymysql.connect(host='sql7.freemysqlhosting.net', port=3306, user='***REMOVED***', password='***REMOVED***',
                           db='***REMOVED***')
    conn.autocommit(True)
    cursor = conn.cursor()

    q = Query.from_(u).delete().where(u.user_id == f"{user_id}")
    cursor.execute(q.get_sql(quote_char=None))

    cursor.close()
    conn.close()


def config():
    """Get the configuration from the database

    Returns:
        conf: The configuration data from the database.
    """
    conn = pymysql.connect(host='sql7.freemysqlhosting.net', port=3306, user='***REMOVED***', password='***REMOVED***',
                           db='***REMOVED***')
    cursor = conn.cursor()

    c = Table(f"{schema_name}.config")
    q = Query.from_(c).select("*")
    cursor.execute(q.get_sql(quote_char=None))
    conf = cursor.fetchone()

    cursor.close()
    conn.close()
    return conf
