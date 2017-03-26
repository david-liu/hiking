#-*- coding: UTF-8 -*-
'''
create a connection pool
'''
import pymysql.cursors


class DBOperator(object):

    def __init__(self,
                 host,
                 user,
                 password,
                 db,
                 charset='utf8mb4'):

        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          db=db,
                                          charset=charset,
                                          cursorclass=pymysql.cursors.DictCursor)

    def find_by(self, sql, parameters):
        with self.connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql, parameters)
            result = cursor.fetchone()

            return result

    
    def insert_by_dict(self, table, dict):
        if not isinstance(dict, list):
            dicts = [dict]
        else:
            dicts = dict

        fields = dicts[0].keys()

        sql = "INSERT INTO " + table + " (" + ', '.join(fields) + ") VALUES "

        obj_values = []
        cnt = 0
        for d in dicts:
            # if cnt > 2:
            #     break
            values = []
            for field in fields:
                values.append("'%s'" % d[field])
            obj_values.append("(" + ",".join(values) + ")")
            cnt += 1
            


        sql += ",".join(obj_values)

        self.insert(sql, ()) 


    def execute(self, sql):
        try:
            if(self.conn != None):
                cursor = self.conn.cursor()
            else:
                raise MySQLdb.Error('No connection')
             
            n = cursor.execute(sql)
            return n
        except MySQLdb.Error,e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def list_by(self, sql, parameters, size=None):
        with self.connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql, parameters)

            if size is None:
                result = cursor.fetchall()
            else:
                result = fetchmany(size)

            return result

    def insert(self, sql, parameters):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, parameters)

            self.connection.commit()

    def close(self):
        self.connection.close()