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

#List records
# ********************************************** List Customers **********************************************
def listCustomersCompanies(models, uid):
    retorno="---CUSTOMERS---\n"
    retorno+="ID      NAME"+'\n'
    count = 0
    # print("List of customers in TimeLoop: \n")
    listOfCustomers = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['customer', '=', True]]])

        # Options
        # ['is_company', '=', True], ['customer', '=', True] -> Si es customer o company
        # {'offset': 10, 'limit': 5} -> filtra el número de resultados
        # search_count -> número de clientes

    customer_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [listOfCustomers],
    {'fields': ['id', 'name']})


    for partner in customer_info:
        #print(partner['name'])
        retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
        count+=1
    #print('\n-------------------------')
    #************************************************************************************************************

    #********************************************** List Companies **********************************************
    # print("List of companies in TimeLoop: \n")
    retorno+="---COMPANIES---\n"
    retorno+="ID      NAME"+'\n'

    listOfCustomers = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True]]])

    customer_info = models.execute_kw(db, uid, password, 'res.partner', 'read', [listOfCustomers],
    {'fields': ['id', 'name']})


    for partner in customer_info:
        retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
        count+=1
    
    #print(retorno)
    # print('\n-------------------------')
    # print("Total contacts: ", count)
    # print('\n-------------------------')
    return retorno


a=listCustomersCompanies(modelos, uid)
print(a)
# #***********************************************************************************************************
# #********************************************** List Products **********************************************
# print("List of products in TimeLoop: \n")

# listOfProducts = models.execute_kw(db, uid, password,
#     'product.template', 'search',
#     [[['categ_id','=',4]]])


# products_info = models.execute_kw(db, uid, password, 'product.template', 'read', [listOfProducts],
#  {'fields': ['id', 'name', 'list_price']})

# for product in products_info:
#     print(product)

# print('\n-------------------------')
# #*********************************************************************************************************
# #********************************************** List Events **********************************************

# print("List of tournaments in TimeLoop: \n")

# listOfEvents = models.execute_kw(db, uid, password,
#     'product.template', 'search',
#     [[['categ_id','=',5]]])


# events_info = models.execute_kw(db, uid, password, 'product.template', 'read', [listOfEvents],
#  {'fields': ['id', 'name', 'list_price']})

# for event in events_info:
#     print(event)

# print('\n-------------------------')


# count_p = models.execute_kw(db, uid, password,
#     'product.template', 'search_count',
#     [[]])
# print('\n-------------------------')
# print("Total products and events: ", count_p)
# print('\n-------------------------')
# #*********************************************************************************************************
#********************************************** List Events **********************************************

# print("Sale orders: \n")

#listOfSales = models.execute_kw(db, uid, password,
#    'sale.order', 'search',
#    [[]])

#sales_info = models.execute_kw(db, uid, password, 'sale.order', 'read', [listOfSales],
#{'fields': ['name','product_id','date_order','warehouse_id','state','cart_quantity','amount_total']})



#for sale in sales_info:
#    print(sale)
#print('\n-------------------------')


#*********************************************************************************************************

 

# # Read records
# partner_records = models.execute_kw(db, uid, password, 'res.partner', 'read', [listOfContacts],
#  {'fields': ['name', 'country_id', 'comment']})

# print("partner_records...")
# for partner in partner_records:
#     print(partner)


# # Search and read
# sr = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
#     [[]],
#     {'fields': ['id', 'name'], 'limit': 10})

# print("Search Read Result...")
# for partnersr in sr:
#     print(partnersr)


 # Create records
#newContact = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
#     'name': "Walter Melon",
# }])
#print("Newly Created ID is:", newContact)

# # # Delete records
# models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[25]])
# # check if the deleted record is still in the database
# models.execute_kw(db, uid, password,
#     'res.partner', 'search', [[['id', '=', 25]]])


# # # Update records
# models.execute_kw(db, uid, password, 'product.template', 'write', [[18], {
#     'list_price': "15"
# }])
# # get record name after having changed it
# models.execute_kw(db, uid, password, 'product.template', 'name_get', [[18]])


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
