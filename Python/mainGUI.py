from os import write
from tkinter import Button, DoubleVar, Scrollbar, StringVar, Tk, Text, Label, Entry, END, Checkbutton, IntVar, scrolledtext
from tkinter.constants import RIGHT
from decimal import Decimal
import xmlrpc.client as xmlrpclib
import mysql.connector
from mysql.connector import Error

# ------------------------------------------------ Odoo Database ------------------------------------------------

# Configuration
url = "http://localhost:8069"
db = 'TimeLoop'
username = 'anaalava@ucm.es'
password = '0d00sg3'

NUM_QUERIES =["Contacts", "Products","Sales"]
TITTLE= "Oddo Management"





class Interface:

    # Logging in
    def login(self):
        print("Connecting to Odoo...")
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        version = common.version()
        self.uid = common.authenticate(db, username, password, {})

        print("Connection was successful with version: ", version)
        #print('\n-------------------------')

        self.models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        return

    def __init__(self, window):
        #Init window
        self.login()

        self.window= window
        self.window.title(TITTLE)
        self.window.geometry("450x550")

        #Title
        Label(self.window, text="- Time-Loop -", font="ar 16 bold").grid(row=0, column=3)

        #Buttons sections
        buttons=[]
        for i in range(0,len(NUM_QUERIES)):
            btn = self.createButton(NUM_QUERIES[i])
            buttons.append(btn)

        for i in range(0,len(buttons)):
            buttons[i].grid(row=i+1, column=2, padx=10, pady=10)
        
        #Result text box
        self.resultText=scrolledtext.ScrolledText(self.window, state="disabled", width=30, height=10)
        self.resultText.grid(row=1, column=3, columnspan=2, rowspan=4, padx=5, pady=5)
        self.stringResQuery=""

        actualRow = len(NUM_QUERIES)+2
        
        #Label to put res of backups
        self.statusLabel = Label(self.window, text="Status: ", font="ar 10 bold")
        self.statusLabel.grid(row=actualRow, column=3)

        actualRow=actualRow+1
        #SubQueries
        #CREATE CONTACT
        Label(self.window, text="Create Contact", font="ar 12 bold").grid(row=actualRow, column=2)
        actualRow=actualRow+1
        name=Label(self.window, text="Name:")
        name.grid(row=actualRow, column=2)
        
        nameValue=StringVar()
        isCompanyValue= IntVar()

        self.entryname= Entry(self.window, textvariable=nameValue)
        self.entryname.grid(row=actualRow,column=3)
        actualRow=actualRow+1
        self.checkIsCompany= Checkbutton(self.window, text="Is company", variable=isCompanyValue)
        self.checkIsCompany.grid(row=actualRow, column=2)
        actualRow=actualRow+1

        btnCreateRecord = Button(text="Create contact", font=('Sans','9','bold'), command=lambda:self.createUser(nameValue.get(),isCompanyValue.get()))
        btnCreateRecord.grid(row=actualRow, column=3)
        actualRow=actualRow+1

        #DELETE CONTACT
        Label(self.window, text="Delete contact", font="ar 12 bold").grid(row=actualRow, column=2)
        actualRow=actualRow+1

        idContact=Label(self.window, text="Contact id:")
        idContact.grid(row=actualRow, column=2)

        idContactValue=StringVar()

        self.entryIdContact=Entry(self.window, textvariable=idContactValue)
        self.entryIdContact.grid(row=actualRow, column=3)
        actualRow=actualRow+1

        btnDeleteContact= Button(text="Delete contact", font=('Sans','9','bold'),command=lambda:self.deleteContact(idContactValue.get()))

        btnDeleteContact.grid(row=actualRow, column=3)
        actualRow=actualRow+1


        #UPDATE PRICE OF PRODUCT
        Label(self.window, text="Update Product", font="ar 12 bold").grid(row=actualRow, column=2)
        actualRow=actualRow+1

        idProductValue=StringVar()
        newPriceValue=StringVar()

        idProduct=Label(self.window, text="Product Id:")
        idProduct.grid(row=actualRow, column=2)

        self.entryIdProduct=Entry(self.window, textvariable=idProductValue)
        self.entryIdProduct.grid(row=actualRow, column=3)

        actualRow=actualRow+1
        newPrice=Label(self.window, text="New price:")
        newPrice.grid(row=actualRow, column=2)

        self.entryNewPrice= Entry(self.window, textvariable=newPriceValue)
        self.entryNewPrice.grid(row=actualRow, column=3)
        actualRow= actualRow+1

        btnUpdateProduct= Button(text="Update price", font=('Sans','9','bold'),command=lambda:self.updatePrice(idProductValue.get(), newPriceValue.get()))
        btnUpdateProduct.grid(row=actualRow, column=3)
        actualRow=actualRow+1
        return

    #OPERATIONS 
    def createButton(self, nameBtn,width=15, height=2 ):
        return Button(self.window, text=nameBtn,font=('Sans','10','bold'), width=width, height=height, command=lambda:self.click(nameBtn))
    
    #Result text options
    def writeResult(self, result):
        if result:
            self.resultText.configure(state="normal")
            self.resultText.insert(END, result)
            self.resultText.configure(state="disabled")
        return
    
    def cleanResult(self):
        self.resultText.configure(state="normal")
        self.resultText.delete("1.0", END)
        self.resultText.configure(state="disabled")
        
        return

    def writeStatusResult(self, result):
        if result == True:
            self.statusLabel.config(text="Status: CORRECT BACKUP")
        else:
            self.statusLabel.config(text="Status: ERROR ON BACKUP")
        return

    def cleanStatusResult(self):
        self.statusLabel.config(text="Status: ")
        return
    # Buttons options
    def click(self, query):
        print("Button selected for: ", query)
        result=""
        if query=="Contacts":
            result, listContacts= self.listCustomersCompanies()
            print(listContacts)
            if result and len(listContacts)>0:
                res = self.insertUsersOnXampp(listContacts) 
                    
        elif query=="Products":
            result, listProducts= self.listProducts()
            print(listProducts)
            if result and len(listProducts)>0:
                res = self.insertProductsOnXampp(listProducts)

        elif query=="Sales":
            result, listSales= self.listSales()
            print(listSales)
            if result and len(listSales)>0:
                res = self.insertSalesOnXampp(listSales)

        self.cleanStatusResult()  
        self.writeStatusResult(res)
        self.cleanResult()
        self.writeResult(result)
        return 

    # -- 3 MAIN QUERIES -- ---------------------------------------------------------------------------------------
    def listCustomersCompanies(self):
        retorno="---CUSTOMERS---\n"
        retorno+="ID      NAME"+'\n'
        count = 0
        listOfCustomers = self.models.execute_kw(db, self.uid, password,
            'res.partner', 'search',
            [[['customer', '=', True]]])

        customer_info = self.models.execute_kw(db, self.uid, password, 'res.partner', 'read', [listOfCustomers],
        {'fields': ['id', 'name']})


        for partner in customer_info:

            retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
            count+=1
    
        retorno+="\n---COMPANIES---\n"
        retorno+="ID      NAME"+'\n'

        listOfCustomers = self.models.execute_kw(db, self.uid, password,
            'res.partner', 'search',
            [[['is_company', '=', True]]])

        company_info = self.models.execute_kw(db, self.uid, password, 'res.partner', 'read', [listOfCustomers],
        {'fields': ['id', 'name', 'is_company']})


        for partner in customer_info:
            retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
            count+=1

        return retorno, customer_info+company_info

    def listProducts(self):
        retorno="---PRODUCTS---\n"
        listOfProducts = self.models.execute_kw(db, self.uid, password,
            'product.template', 'search',
            [[['categ_id','=',4]]])


        products_info = self.models.execute_kw(db, self.uid, password, 'product.template', 'read', [listOfProducts],
        {'fields': ['id', 'name', 'list_price']})

        for product in products_info:
            retorno+=str(product['id'])+" - "+product['name']+" : " +str(product['list_price'])+' €'+'\n'

        retorno+="\n---EVENTS---\n"
        listOfEvents = self.models.execute_kw(db, self.uid, password,
            'product.template', 'search',
            [[['categ_id','=',5]]])


        events_info = self.models.execute_kw(db, self.uid, password, 'product.template', 'read', [listOfEvents],
        {'fields': ['id', 'name', 'list_price']})

        for event in events_info:
            retorno+=str(event['id'])+" ==> "+event['name']+" == " +str(event['list_price'])+' €'+'\n'

        return retorno, products_info+events_info

    def listSales(self):
        retorno="---PRODUCTS---\n"
        listOfSales = self.models.execute_kw(db, self.uid, password,
        'sale.order', 'search',
        [[]])

        sales_info = self.models.execute_kw(db, self.uid, password, 'sale.order', 'read', [listOfSales],
        {'fields': ['id','name','date_order','warehouse_id','state','cart_quantity','amount_total']})

        for sale in sales_info:
            retorno+=str(sale['id'])+"  "+str(sale['name'])+"  " +str(sale['amount_total'])+'\n'

        return retorno, sales_info
    ##------------------------------------------------------------------------------------------------------------
    ## BACKUP METHODS ON XAMPP------------------------------------------------------------------------------------
    def insertUsersOnXampp(self, listOfUsers):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='odoo',
                                                user='root',
                                                password='')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("TRUNCATE TABLE contacts")

                print("You're connected to database. ")
                for elem in listOfUsers:
                    data_contact= {
                        'id': int(elem['id']),
                        'name': elem['name'],
                        'type': 1
                    }
                    print("Inserting data: ", data_contact)
                    query="INSERT INTO contacts (id, name, type) VALUES (%(id)s,%(name)s,%(type)s);"
                    cursor.execute(query, data_contact)
                
                connection.commit()
                
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False
        finally:
            if connection.is_connected():
                
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return True

    #Backup Products on Xampp
    def insertProductsOnXampp(self, listOfProducts):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='odoo',
                                                user='root',
                                                password='')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("TRUNCATE TABLE products")

                print("You're connected to database. ")
                for elem in listOfProducts:
                    data_product= {
                        'id': int(elem['id']),
                        'name': elem['name'],
                        'price': float(elem['list_price'])
                    }
                    print("Inserting data: ", data_product)
                    query="INSERT INTO products (id, name, price) VALUES (%(id)s,%(name)s,%(price)s);"
                    cursor.execute(query, data_product)
                
                connection.commit()
                
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False
        finally:
            if connection.is_connected():
                
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return True
   #Backup Sales on Xampp
    def insertSalesOnXampp(self, listOfSales):
        
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='odoo',
                                                user='root',
                                                password='')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("TRUNCATE TABLE sales")

                print("You're connected to database. ")
                for elem in listOfSales:
                    data_sale= {
                        'id': int(elem['id']),
                        'name': elem['name'],
                        'totalprice': float(elem['amount_total'])
                    }
                    print("Inserting data: ", data_sale)
                    query="INSERT INTO sales (id, name, totalprice) VALUES (%(id)s,%(name)s,%(totalprice)s);"
                    cursor.execute(query, data_sale)
                
                connection.commit()
                
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False
        finally:
            if connection.is_connected():
                
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return True

    # --- CRUD Operations--------------------------------------------------------------------
    ## Create Query --------------------------------------------------------------------------
    def createUser(self, name, isCompany):
        res=""
        if name:
            print("New contact with name: ", name, "and is company ",isCompany )
            res = self.createRecord(name, isCompany)
            if res:
                self.writeResult("Newly Created ID is:", res)
            else: 
                self.writeResult("Error creating new Contact")
            self.entryname.delete("0", END)
            self.checkIsCompany.deselect()
            
        else: 
            print("You must write a name for new customer/company")
        return 

    def createRecord(self, name, isCompany):
        newContact = self.models.execute_kw(db, self.uid, password, 'res.partner', 'create', [{
            'name': name, 'is_company' : isCompany
        }])
        return newContact 
        
    ## Delete Record---------------------------------------------------------------------------------
    def deleteContact(self, idContact):
        ok=False
        if idContact.isdigit():
            res = self.deleteRecord(int(idContact))
            if res:
                self.writeResult("Error deleting contact with id: "+ idContact)
            else:
                self.writeResult("Delete contact with id: "+ idContact)

        else:
            print("You must write a id for delete record")

        self.entryIdContact.delete("0", END)
        return

    def deleteRecord(self, id):
        self.models.execute_kw(db, self.uid, password, 'res.partner', 'unlink', [[id]])
        # check if the deleted record is still in the database
        record = self.models.execute_kw(db, self.uid, password,
            'res.partner', 'search', [[['id', '=', id]]])
        return record
    
    ## Update Product with a new Price:--------------------------
    def updatePrice(self, idProduct, newPrice):

        if idProduct.isdigit() and Decimal(newPrice):
            print("Update price of product with id: ", idProduct, " and new price: ",newPrice )
            res = self.updatePriceRecord(int(idProduct), float(newPrice))
            if res and res[0]== idProduct:
                self.writeResult("Updated price of product with id: "+ idProduct) 
            else:
                self.writeResult("Error updating product with id:"+ idProduct)
        else: 
            print("You must write a proper id and/or price for updating a product")

        self.entryIdProduct.delete("0", END)
        self.entryNewPrice.delete("0", END)
        return
    
    def updatePriceRecord(self, id, list_price):
        self.models.execute_kw(db, self.uid, password, 'product.template', 'write', [[id], {
            'list_price': list_price
        }])
        # get record name after having changed it
        record = self.models.execute_kw(db, self.uid, password, 'product.template', 'name_get', [[id]])
        return record

    ##---------------------------------------------------------------------
mainwindow= Tk()
odooServer=Interface(mainwindow)
mainwindow.mainloop()