from tkinter import Button, StringVar, Tk, Text, Label, Entry, END
from tkinter.constants import ACTIVE

NUM_QUERIES =["Contacts", "Products","Sales"]
#Contactos (Clientes + Compañias)
#Productos (Productos y eventos)
#Ventas

#Controlar Contacts (CRUD)

#Guardar datos en bbdd propia



TITTLE= "Oddo Management"

class Interface:
    def __init__(self, window):
        #Inicializar la ventanta con un titulo
        self.window= window
        self.window.title(TITTLE)
        self.window.geometry("400x400")

        #Title
        Label(self.window, text="Main queries", font="ar 15 bold").grid(row=0, column=3)

        #Agregamos los botones
        buttons=[]
        for i in range(0,len(NUM_QUERIES)):
            btn = self.createButton(NUM_QUERIES[i])
            buttons.append(btn)

        for i in range(0,len(buttons)):
            buttons[i].grid(row=i+1, column=2, padx=10, pady=10)
        
        #Pantalla de resultados:
        self.resultText=Text(window, state="disabled", width=20, height=10)
        self.resultText.grid(row=1, column=3, columnspan=2, rowspan=4, padx=5, pady=5)
        #variable String con el resultado:
        self.stringResQuery=""

        actualRow = len(NUM_QUERIES)+2
        
         #SubQueries
        Label(self.window, text="Create Contact", font="ar 14").grid(row=actualRow, column=2)
        actualRow=actualRow+1
        name=Label(self.window, text="Name")
        name.grid(row=actualRow, column=2)
        nameValue=StringVar
        entryname= Entry(self.window, textvariable=nameValue)
        entryname.grid(row=actualRow,column=3)
        actualRow=actualRow+1

        btnCreateRecord = Button(text="Create record", command=lambda:self.createUser())
        btnCreateRecord.grid(row=actualRow, column=3)
        return

    def createButton(self, nameBtn,width=15, height=2 ):
        return Button(self.window, text=nameBtn, width=width, height=height, command=lambda:self.click(nameBtn))
    
    #Result text options
    def writeResult(self, result):
        self.resultText.configure(state="normal")
        self.resultText.insert(END, result)
        self.resultText.configure(state="disabled")
        return
    
    def cleanResult(self):
        self.resultText.configure(state="normal")
        self.resultText.delete("1.0", END)
        self.resultText.configure(state="disabled")
        return

    #Buttons options
    def click(self, query):
        print("Button selected for: ", query)
        result=""
        if query=="Contacts":
            result, listContacts= self.listCustomersCompanies()
            print(listContacts)
            if result and len(listContacts)>0:
                res = self.createUsersOnXampp(listContacts)
                if res==True:
                    print("CORRECT BACKUP OF CONTACTS")
                else:
                    print("ERROR BACKUP OF CONTACTS")
                
        elif query=="Products":
            result, listProducts= self.listProducts()
            print(listProducts)
            if result and len(listProducts)>0:
                res = self.createUsersOnXampp(listProducts)
                if res==True:
                    print("CORRECT BACKUP OF PRODUCTS")
                else:
                    print("ERROR BACKUP OF PRODUCTS")
        elif query=="Sales":
            result, listSales= self.listSales()
            print(listSales)
            if result and len(listSales)>0:
                res = self.createUsersOnXampp(listSales)
                if res==True:
                    print("CORRECT BACKUP OF SALES")
                else:
                    print("ERROR BACKUP OF SALES")

        self.cleanResult()
        self.writeResult(result)
        return 

    # -- 3 MAIN QUERIES -- 
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
    
        retorno+="---COMPANIES---\n"
        retorno+="ID      NAME"+'\n'

        listOfCustomers = self.models.execute_kw(db, self.uid, password,
            'res.partner', 'search',
            [[['is_company', '=', True]]])

        customer_info = self.models.execute_kw(db, self.uid, password, 'res.partner', 'read', [listOfCustomers],
        {'fields': ['id', 'name']})


        for partner in customer_info:
            retorno+=str(partner['id'])+" ==> "+partner['name']+'\n'
            count+=1

        return retorno, customer_info

    def listProducts(self):
        retorno="---PRODUCTS---\n"
        retorno+="ID     PRODUCT     PRICE"+'\n'
        listOfProducts = self.models.execute_kw(db, self.uid, password,
            'product.template', 'search',
            [[['categ_id','=',4]]])


        products_info = self.models.execute_kw(db, self.uid, password, 'product.template', 'read', [listOfProducts],
        {'fields': ['id', 'name', 'list_price']})

        for product in products_info:
            retorno+=str(product['id'])+" ==> "+product['name']+" == " +str(product['list_price'])+'\n'

        #*********************************************************************************************************
        #********************************************** List Events **********************************************
        retorno+="---COMPANIES---\n"
        retorno+="ID     PRODUCT     PRICE"+'\n'
        listOfEvents = self.models.execute_kw(db, self.uid, password,
            'product.template', 'search',
            [[['categ_id','=',5]]])


        events_info = self.models.execute_kw(db, self.uid, password, 'product.template', 'read', [listOfEvents],
        {'fields': ['id', 'name', 'list_price']})

        for event in events_info:
            retorno+=str(event['id'])+" ==> "+event['name']+" == " +str(event['list_price'])+'\n'

        return retorno

    def listSales(self):
        retorno="---PRODUCTS---\n"
        retorno+="NAME     PRODUCT ID     DATE     WAREHOUSE ID     STATE     CART QUANTITY     AMOUNT"+'\n'
        listOfSales = self.models.execute_kw(db, self.uid, password,
        'sale.order', 'search',
        [[]])

        sales_info = self.models.execute_kw(db, self.uid, password, 'sale.order', 'read', [listOfSales],
        {'fields': ['id','name','date_order','warehouse_id','state','cart_quantity','amount_total']})



        for sale in sales_info:
            retorno+=str(sale['id'])+"  "+str(sale['name'])+"  " +str(sale['amount_total'])+'\n'

        
        return retorno

    def createUsersOnXampp(self, listOfUsers):
        
        saveOk=False
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
                    'id': elem['id'],
                    'name': elem['name'],
                    'type': True
                }
                print(data_contact)
                insert="(INSERT INTO contacts(id, name, type) VALUES(%s,%s,'%s'))"
                cursor.execute(insert, data_contact)

            saveOk= True

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                return


        return saveOk
    
    # --- CRUD Operations
    def createUser(self, name,isCompany):
        if name.isalpha():
            print("New contact with name: ", name, "and is company ",isCompany )
            #TODO llamada a funcion que crea
            self.entryname.delete("0", END)
            self.checkIsCompany.deselect()
            
        else: 
            print("You must write a proper name for new customer/company")
        return 

    def createUser(self):
        print("New contact: ")
        return 



mainwindow= Tk()
odooServer=Interface(mainwindow)
mainwindow.mainloop()