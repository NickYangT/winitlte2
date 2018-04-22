#-*-coding:utf-8-*-
import pymysql

def connect_mysql():
    #mac 环境
    conn = pymysql.connect(host='localhost', port=3306, user='root',passwd='123456', db='winitlte', charset='utf8')
    #win 环境
    #conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='winitlte', charset='utf8')
    return conn




def execute_sql_str(str, values=None):
    """
    一般SQL执行: str: select *from xxx_table_name
    存储过程执行的时候 str：call xxxx_proc_name()
    """
    conn = connect_mysql()
    cursor = conn.cursor()
    try:
        if values != None:
            cursor.execute(str, values)
        else:
            cursor.execute(str)
        if 'SELECT' == str[:6].upper():
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
