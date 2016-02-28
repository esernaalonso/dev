"""Summary"""
#######################################
# imports

import esa.common.python.lib.db.mysql.mysql as mysql

reload(mysql)

#######################################
# functionality


def check_connection():
    host='mysql.insideanim.com'
    user='ins_db_manager'
    password='_1ns_db_m4n4g3r_'
    db='insideanim_school_db'
    charset='utf8mb4'

    return mysql.check_connection(host=host, user=user, password=password, db=db, charset=charset)


def connection(sql):
    host='mysql.insideanim.com'
    user='ins_db_manager'
    password='_1ns_db_m4n4g3r_'
    db='insideanim_school_db'
    charset='utf8mb4'

    if sql:
        return mysql.connection(host=host, user=user, password=password, db=db, charset=charset, sql=sql)


def check_user(user_name):
    sql="SELECT `username`, `email` FROM `t_user`"
    result = connection(sql)

    for row in result:
        if user_name == row["username"] or user_name == row["email"]:
            return True

    return False


def check_user_password(user_name, user_password):
    if check_user(user_name):
        sql="SELECT `username`, `email`, `password` FROM `t_user`"
        result = connection(sql)

        for row in result:
            if user_name == row["username"] or user_name == row["email"]:
                if user_password == row["password"]:
                    return True

    return False


#######################################
# execution

if __name__ == "__main__":
    print check_user_password("eserna","AlSerEd01")
