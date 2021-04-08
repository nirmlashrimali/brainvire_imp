import xmlrpc.client
import xlrd
from xlrd import open_workbook


HOST = 'localhost'
PORT = 9000
DB = 'hotel3'
USER = 'admin'
PASS = 'admin'

url = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

object_proxy = xmlrpc.client.ServerProxy(url+'object')
common_proxy = xmlrpc.client.ServerProxy(url+'common')

uid = common_proxy.login(DB, USER, PASS)
print("Logged in as %s (uid:%d)" % (USER, uid))

loc = "/home/nirmla_shrimali/source/odoo/sale.xlsx"

wb = xlrd.open_workbook(loc)

for sheet in wb.sheets():
    for row in range(1, sheet.nrows):
        sale_order_id= sheet.cell(row, 0).value
        sale_order_sign = sheet.cell(row, 1).value
        print(sale_order_sign)
        name=object_proxy.execute_kw(DB, uid, PASS, 'sale.order', 'write',
            [[93],{
             'sign':(sale_order_sign)
        }])
        print(name)