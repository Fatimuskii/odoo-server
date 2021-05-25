import xmlrpc.client as xmlrpclib

# ------------------------------------------------ Odoo Database ------------------------------------------------

# Configuration
url = "http://localhost:8069"
db = 'TimeLoop13'
username = 'anaalava@ucm.es'
password = '0d00sg3'


# Logging in
def login():
    print("Connecting to Odoo...")
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()
    uid = common.authenticate(db, username, password, {})

    print("Connection was successful with version: ", version)
    #print('\n-------------------------')

    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return models, uid
modelos, uid=login()

# #List records
# # ********************************************** List Customers **********************************************
# def listCustomersCompanies(models, uid):
#     retorno="---CUSTOMERS---\n"
#     retorno+="ID      NAME"+'\n'
#     count = 0
#     # print("List of customers in TimeLoop: \n")
#     listOfCustomers = models.execute_kw(db, uid, password,
#         'res.partner', 'search',
#         [[['customer', '=', True]]])

#         # Options
#         # ['is_company', '=', True], ['customer', '=', True] -> Si es customer o company
#         # {'offset': 10, 'limit': 5} -> filtra el número de resultados
#         # search_count -> número de clientes

#     customer_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [listOfCustomers],
#     {'fields': ['id', 'name']})


#     for partner in customer_info:
#         #print(partner['name'])
#         retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
#         count+=1
#     #print('\n-------------------------')
#     #************************************************************************************************************

#     #********************************************** List Companies **********************************************
#     # print("List of companies in TimeLoop: \n")
#     retorno+="---COMPANIES---\n"
#     retorno+="ID      NAME"+'\n'

#     listOfCustomers = models.execute_kw(db, uid, password,
#         'res.partner', 'search',
#         [[['is_company', '=', True]]])

#     customer_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [listOfCustomers],
#     {'fields': ['id', 'name']})


#     for partner in customer_info:
#         retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
#         count+=1
    
#     #print(retorno)
#     # print('\n-------------------------')
#     # print("Total contacts: ", count)
#     # print('\n-------------------------')
#     return retorno


# a=listCustomersCompanies(modelos, uid)
# print(a)
# # #***********************************************************************************************************
# # #********************************************** List Products **********************************************

# def listProducts(models, uid):
#     retorno="---PRODUCTS---\n"
#     retorno+="ID     PRODUCT     PRICE"+'\n'
#     listOfProducts = models.execute_kw(db, uid, password,
#         'product.template', 'search',
#         [[['categ_id','=',4]]])


#     products_info = models.execute_kw(db, uid, password, 'product.template', 'read', [listOfProducts],
#     {'fields': ['id', 'name', 'list_price']})

#     for product in products_info:
#         retorno+=str(product['id'])+" ==> "+product['name']+" == " +str(product['list_price'])+'\n'

#     #*********************************************************************************************************
#     #********************************************** List Events **********************************************
#     retorno+="---COMPANIES---\n"
#     retorno+="ID     PRODUCT     PRICE"+'\n'
#     listOfEvents = models.execute_kw(db, uid, password,
#         'product.template', 'search',
#         [[['categ_id','=',5]]])


#     events_info = models.execute_kw(db, uid, password, 'product.template', 'read', [listOfEvents],
#     {'fields': ['id', 'name', 'list_price']})

#     for event in events_info:
#         retorno+=str(event['id'])+" ==> "+event['name']+" == " +str(event['list_price'])+'\n'

#     return retorno

# print(listProducts(modelos, uid))
# # #*********************************************************************************************************
# #********************************************** List Events **********************************************

# # print("Sale orders: \n")

# def listSales(models, uid):
#     retorno="---PRODUCTS---\n"
#     retorno+="NAME     PRODUCT ID     DATE     WAREHOUSE ID     STATE     CART QUANTITY     AMOUNT"+'\n'
#     listOfSales = models.execute_kw(db, uid, password,
#        'sale.order', 'search',
#        [[]])

#     sales_info = models.execute_kw(db, uid, password, 'sale.order', 'read', [listOfSales],
#     {'fields': ['id','name','date_order','warehouse_id','state','cart_quantity','amount_total']})



#     for sale in sales_info:
#        retorno+=str(sale['id'])+"  "+str(sale['name'])+"  " +str(sale['amount_total'])+'\n'

    
#     return retorno

# print(listSales(modelos, uid))


# #*********************************************************************************************************

 

# # # Read records
# # partner_records = models.execute_kw(db, uid, password, 'res.partner', 'read', [listOfContacts],
# #  {'fields': ['name', 'country_id', 'comment']})

# # print("partner_records...")
# # for partner in partner_records:
# #     print(partner)


# # # Search and read
# # sr = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
# #     [[]],
# #     {'fields': ['id', 'name'], 'limit': 10})

# # print("Search Read Result...")
# # for partnersr in sr:
# #     print(partnersr)


#  # Create records
# def createRecord(models, uid, name, isCompany):
#     newContact = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
#         'name': name, 'is_company' : isCompany
#     }])
#     print("Newly Created ID is:", newContact)
#     return newContact

# # # Delete records
def deleteContact(models, uid, id):
    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
    # check if the deleted record is still in the database
    models.execute_kw(db, uid, password,
        'res.partner', 'search', [[['id', '=', id]]])
    return

deleteContact(modelos, uid, 21)

# # # Update records
def updateContact(models, uid, id, list_price):
    models.execute_kw(db, uid, password, 'product.template', 'write', [[id], {
        'list_price': list_price
    }])
    # get record name after having changed it
    models.execute_kw(db, uid, password, 'product.template', 'name_get', [[id]])
    return


# ------------------------------------------------ XAMP Database ------------------------------------------------
# https://www.youtube.com/watch?v=brlgfZkR-LM&list=PLqRRLx0cl0hpaeRhYeNEk7xQgOxv16VF-&index=5
# Configuration
# url_x = "http://localhost/phpmyadmin/db_structure.php?server=1&db=odoo"
# db_x = 'odoo'
# username_x = 'root'
# password_x = ''

# common_x = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url_x))
# models_x = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url_x))
# version_x = common_x.version()

# print("details_x...", version_x)
