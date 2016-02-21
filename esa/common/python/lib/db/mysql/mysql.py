"""Summary"""
#######################################
# imports

import pymysql

#######################################
# functionality


def connection(host=None, user=None, password=None, db=None, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, sql=None):
    if host and user and password and db and charset and cursorclass and sql:
        # Connect to the database
        connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset, cursorclass=cursorclass)
        result= None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
            return result

#######################################
# execution

if __name__ == "__main__":
    result = connection(host='mysql.insideanim.com',
                user='ins_db_manager',
                password='_1ns_db_m4n4g3r_',
                db='insideanim_school_db',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                sql="SELECT * FROM `user`")

    print result
