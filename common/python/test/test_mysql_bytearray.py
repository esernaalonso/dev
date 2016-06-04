import pymysql
import esa.common.python.lib.db.mysql.mysql as mysql

sql = "SELECT content FROM `t_resource` WHERE id=1"

result = mysql.connection(host='mysql.insideanim.com',
            user='ins_db_manager',
            password='_1ns_db_m4n4g3r_',
            db='insideanim_school_db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            sql=sql)

print result
