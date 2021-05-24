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
        self.cleanResult()
        self.writeResult(query)
        return 

    def createUser(self):
        print("New contact: ")
        return 



mainwindow= Tk()
odooServer=Interface(mainwindow)
mainwindow.mainloop()