from django.test import TestCase
from ConnectMysql import execute_sql_str

# Create your tests here.
data =execute_sql_str('SELECT id ,methodName, description, createdtime, createdby FROM sg_pms')
print data