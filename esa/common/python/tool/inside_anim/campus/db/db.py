"""Summary"""
#######################################
# imports

import esa.common.python.lib.db.mysql.mysql as mysql

#######################################
# functionality


def connection(sql):
    host='mysql.insideanim.com'
    user='ins_db_manager'
    password='_1ns_db_m4n4g3r_'
    db='insideanim_school_db'
    charset='utf8mb4'

    if sql:
        return mysql.connection(host=host, user=user, password=password, db=db, charset=charset, sql=sql)

def check_user(user_name):
    sql="SELECT `username`, `email` FROM `user`"
    result = connection(sql)

    for row in result:
        if user_name == row["username"] or user_name == row["email"]:
            return True

    return False

#######################################
# execution

if __name__ == "__main__":
    print check_user("eserna")
