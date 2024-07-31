from tkinter import *
import mysql.connector as msc
from tkinter import messagebox
from tkinter import ttk
import random
from dotenv import load_dotenv
import os
from tables import create_tables

create_tables()

# Load environment variables from the .env file
load_dotenv()

# Get the environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to the database using the environment variables
db = msc.connect(
    host=db_host,
    user=db_user,
    passwd=db_password,
    database=db_name
)

c = db.cursor()

root=Tk()
root.title("Welcome to 18"+u"\u00b0"+" Celsius")
root.geometry("300x250+500+300")

def start():
    query="select name,address,mobileno from customers where username=%s and password=%s"
    values=(x,y)
    c.execute(query,values)
    s=c.fetchall()
    root.title("Start Section")

    def bo():
        bow=Tk()
        bow.title("Customisation Section")
        bow.geometry("500x480")
        custom1=Label(bow,text="What kind of AC would you like to purchase?")
        custom2=Label(bow,text="Select the suitable options as per your preferences:")
        custom1.grid(row=0,column=0,sticky=W)
        custom2.grid(row=1,column=0,pady=10)

        pricefl=Label(bow,text="Price: From ")
        pricef=Spinbox(bow,from_=20000,to=60000,increment=10000,wrap=True,state="readonly",bd=3,fg="red")
        pricefl.grid(row=2,column=0,sticky=E,pady=10)
        pricef.grid(row=2,column=1)
        pricetl=Label(bow,text="Price: To ")
        pricet=Spinbox(bow,from_=30000,to=70000,increment=10000,wrap=True,state="readonly",bd=3,fg="blue")
        pricetl.grid(row=3,column=0,sticky=E,pady=10)
        pricet.grid(row=3,column=1)

        blabel=Label(bow,text="Brand: ")
        blabel.grid(row=4,column=0,sticky=E,pady=10)
        brands=["Any Brand","OGeneral","LG","Hitachi","Sharp","Daikin"]
        brandmenu=ttk.Combobox(bow,values=brands,state="readonly")
        brandmenu.current(0)
        brandmenu.grid(row=4,column=1)

        tlabel=Label(bow,text="Type of AC: ")
        tlabel.grid(row=5,column=0,sticky=E,pady=10)
        types=["Window","Split","Centralised"]
        typemenu=ttk.Combobox(bow,values=types,state="readonly")
        typemenu.set("Choose your type")
        typemenu.grid(row=5,column=1)

        syslabel=Label(bow,text="Type of System: ")
        syslabel.grid(row=6,column=0,sticky=E,pady=10)
        systems=["Inverter AC","Non Inverter AC"]
        sysmenu=ttk.Combobox(bow,values=systems,state="readonly")
        sysmenu.set("Choose your system")
        sysmenu.grid(row=6,column=1)

        cpl=Label(bow,text="Cooling Power: ")
        cpl.grid(row=7,column=0,sticky=E,pady=10)
        coolpower=["1 ton","1.5 ton","2 ton","3 ton"]
        cpmenu=ttk.Combobox(bow,values=coolpower,state="readonly")
        cpmenu.set("Choose a power rating")
        cpmenu.grid(row=7,column=1)

        sortl=Label(bow,text="Sort by:")
        sortl.grid(row=8,column=0,sticky=E,pady=10)
        sort=["Price: Low to High","Price: High to Low"]
        sortmenu=ttk.Combobox(bow,values=sort,state="readonly")
        sortmenu.current(0)
        sortmenu.grid(row=8,column=1)

        def apply():
            if  pricef.get()>=pricet.get():
                messagebox.showerror("Wrong price range","Please set a valid price range.")
            elif typemenu.get()=="Choose your type":
                messagebox.showerror("Type not chosen","Choose a valid AC type")
            elif sysmenu.get()=="Choose your system":
                messagebox.showerror("System not chosen","Choose a valid AC system")
            elif cpmenu.get()=="Choose a power rating":
                messagebox.showerror("Power Rating not chosen","Choose a valid power rating")
            elif brandmenu.get()=="Any Brand":
                bow.geometry("560x300")
                bowidgets=[pricef,pricet,brandmenu,typemenu,sysmenu,cpmenu,sortmenu,pricefl,pricetl,blabel,tlabel,syslabel,cpl,sortl,custom1,custom2,applybtn]
                if sortmenu.get()=="Price: High to Low":
                    query="select * from products where ac_type =%s and ac_system=%s and power_rating=%s and price between %s and %s order by price desc"
                else:
                    query="select * from products where ac_type =%s and ac_system=%s and power_rating=%s and price between %s and %s order by price"
                values=(typemenu.get(),sysmenu.get(),cpmenu.get(),pricef.get(),pricet.get())
                c.execute(query,values)
                
                for i in bowidgets:
                    i.destroy()
                r=c.fetchall()
                reslabel=Label(bow,text="We have fetched "+str(len(r))+ " results for you")
                reslabel.grid(row=0,column=0)
                labels=[]
                for rec in r:
                    label=Label(bow,text="Model ID:- "+rec[0]+" Specs: "+rec[1]+", "+str(rec[2])+", "+rec[3]+", "+rec[4]+", "+rec[5])
                    label.grid(row=r.index(rec)+1,column=0,sticky=W)
                    labels.append(label)
                orderl=Label(bow,text="Enter the model ID of the AC you wish to purchase:")
                orderen=Entry(bow)
                orderen.focus()
                orderl.grid(row=len(r)+1,column=0,sticky=E,pady=10)
                orderen.grid(row=len(r)+1,column=1)
                mids=[]
                for i in r:
                    mids.append(i[0])
                def pay():
                   if orderen.get().upper() not in mids:
                    messagebox.showerror("Invalid Model ID","Enter a valid model ID amongst the following options.")
                   else:
                       bow.geometry("300x300")
                       mdl=orderen.get().upper()
                       orderen.destroy()
                       orderl.destroy()
                       reslabel.destroy()
                       paybtn.destroy()
                       
                       for i in labels:
                           i.destroy()
                       codestr="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                       code=random.sample(codestr,6)
                       orderid="".join(code)
                       
                       payl=Label(bow,text="Welcome to Pay Section")
                       payl.grid(row=0,column=0,pady=10)
                       paylist=["UPI","Debit card/Credit card","Cash on delivery"]
                       paymenu=ttk.Combobox(bow,values=paylist,state='readonly')
                       paymenu.set("Choose payment method")
                       paymenu.grid(row=1,column=1)
                       payl=Label(bow,text="Choose payment method:")
                       payl.grid(row=1,column=0)
                       def placeorder():
                           if paymenu.get()=="Choose payment method":
                               messagebox.showerror("Payment method not chosen","Choose a valid payment method")
                           else:
                               placeorder.config(state='disabled')
                               query="insert into orders values(%s,%s,%s,%s,%s)"
                               values=(orderid,mdl,s[0][0],s[0][1],s[0][2])
                               c.execute(query,values)
                               db.commit()
                               
                               yesno=messagebox.askyesno("Order Placed","Your Order has been placed with order ID:"+orderid+"""\nand will be delivered to your registered address.
    A SMS will be sent to your mobile number.\nNote: Please remember your order id in case of cancellation  of order.\nDo you wish to exit?\nClick Yes to exit.
    Click No to go back to the start section.""")
                               if yesno==1:
                                   bow.destroy()
                                   root.destroy()
                               elif yesno==0:
                                   bow.destroy() 
                       
                       placeorder=Button(bow,text="Place order",command=placeorder,bd=3)
                       placeorder.grid(row=2,column=1,pady=5)
                   
                paybtn=Button(bow,text="Proceed to payment section",command=pay)
                paybtn.grid(row=len(r)+2,column=1)
            else:
                bow.geometry("560x300")
                bowidgets=[pricef,pricet,brandmenu,typemenu,sysmenu,cpmenu,sortmenu,pricefl,pricetl,blabel,tlabel,syslabel,cpl,sortl,custom1,custom2,applybtn]
                if sortmenu.get()=="Price: High to Low":
                    query="select * from products where brand =%s and ac_type =%s and ac_system=%s and power_rating=%s and price between %s and %s order by price desc"
                else:
                    query="select * from products where brand =%s and ac_type =%s and ac_system=%s and power_rating=%s and price between %s and %s order by price"
                values=(brandmenu.get(),typemenu.get(),sysmenu.get(),cpmenu.get(),pricef.get(),pricet.get())
                c.execute(query,values)
                
                for i in bowidgets:
                    i.destroy()
                    
                r=c.fetchall()
                reslabel=Label(bow,text="We have fetched "+str(len(r))+ " results for you")
                reslabel.grid(row=0,column=0)
                labels=[]
                for rec in r:
                    label=Label(bow,text="Model ID:- "+rec[0]+" Specs: "+rec[1]+", "+str(rec[2])+", "+rec[3]+", "+rec[4]+", "+rec[5])
                    label.grid(row=r.index(rec)+1,column=0,sticky=W)
                    labels.append(label)
                orderl=Label(bow,text="Enter the Model ID of the AC you wish to purchase:")
                orderen=Entry(bow)
                orderen.focus()
                mids=[]
                for i in r:
                    mids.append(i[0])
                
                orderl.grid(row=len(r)+1,column=0,pady=20,sticky=E)
                orderen.grid(row=len(r)+1,column=1,pady=10)
                def pay():
                   if orderen.get().upper() not in mids:
                    messagebox.showerror("Invalid Model ID","Enter a valid model ID amongst the following options.")
                   else:
                       bow.geometry("300x300")
                       mdl=orderen.get().upper()
                       orderen.destroy()
                       orderl.destroy()
                       reslabel.destroy()
                       paybtn.destroy()
                       
                       for i in labels:
                           i.destroy()
                       codestr="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                       code=random.sample(codestr,6)
                       orderid="".join(code)
                       
                       payl=Label(bow,text="Welcome to Pay Section")
                       payl.grid(row=0,column=0,pady=10)
                       paylist=["UPI","Debit card/Credit card","Cash on delivery"]
                       paymenu=ttk.Combobox(bow,values=paylist,state='readonly')
                       paymenu.set("Choose payment method")
                       paymenu.grid(row=1,column=1)
                       payl=Label(bow,text="Choose payment method:")
                       payl.grid(row=1,column=0)
                       def placeorder():
                           if paymenu.get()=="Choose payment method":
                               messagebox.showerror("Payment method not chosen","Choose a valid payment method")
                           else:
                               placeorder.config(state='disabled')
                               query="insert into orders values(%s,%s,%s,%s,%s)"
                               values=(orderid,mdl,s[0][0],s[0][1],s[0][2])
                               c.execute(query,values)
                               db.commit()
                               
                               yesno=messagebox.askyesno("Order Placed","Your Order has been placed with order ID:"+orderid+"""\nand will be delivered to your registered address.
    A SMS will be sent to your mobile number.\nNote: Please remember your order id in case of cancellation  of order.\nDo you wish to exit?\nClick Yes to exit.
    Click No to go back to the start section.""")
                               if yesno==1:
                                   bow.destroy()
                                   root.destroy()
                               elif yesno==0:
                                   bow.destroy() 
                       
                       placeorder=Button(bow,text="Place order",command=placeorder,bd=3)
                       placeorder.grid(row=2,column=1,pady=5)
                         
                paybtn=Button(bow,text="Proceed to payment section",command=pay)
                paybtn.grid(row=len(r)+2,column=1,pady=3)
                
        applybtn=Button(bow,text="Apply Customisation",command=apply,bd=3)
        applybtn.grid(row=10,column=1,sticky=W)

    def co():
        cquery1="select order_id,model_id from orders where name=%s and address=%s and mobile_no=%s"
        c.execute(cquery1,(s[0][0],s[0][1],s[0][2]))
        cores=c.fetchall()
        if cores==[]:
            messagebox.showinfo("No Previous Orders","You don\'t have any previous orders.\nTo book an order, click Book Orders in the start section.")
        else:
            cow=Tk()
            cow.title("Order Cancellation")
            cow.geometry("625x180")
            col=Label(cow,text="Which order do you wish to cancel ?")
            col.grid(row=0,column=0)
            details=[]
            for i in cores:
                cquery2="select brand,price,ac_type,ac_system,power_rating from products where model_id=%s"
                c.execute(cquery2,(i[1],))
                specs=c.fetchall()
                for j in specs:
                    i=i+j
                    details.append(i)
                    col1=Label(cow,text="Order ID:- "+i[0]+" Model ID:- "+i[1]+" Specs: "+i[2]+", "+str(i[3])+", "+i[4]+", "+i[5]+", "+i[6])
                    col1.grid(row=details.index(i)+1,column=0)

            coenl=Label(cow,text="Enter the order id:")
            coen=Entry(cow)
            coen.focus()
            coenl.grid(row=len(details)+1,column=0,sticky=E,pady=10)
            coen.grid(row=len(details)+1,column=1,sticky=W)
            oids=[]
            for i in details:
                oids.append(i[0])
            def cancel():
                if coen.get().upper() not in oids:
                        messagebox.showerror("Invalid Order ID","Enter a valid Order ID from amongst the following options.")
                else:
                    value=coen.get().upper()
                    c.execute("delete from orders where order_id=%s",(value,))
                    db.commit()
                    cancelresponse=messagebox.askyesno("Exit/Return to Start","The order has been cancelled.\nDo you wish to exit?")
                    if cancelresponse==1:
                        cow.destroy()
                        root.destroy()
                    elif cancelresponse==0:
                        cow.destroy()
                        
            cancelbtn=Button(cow,text="Cancel order",command=cancel)
            cancelbtn.grid(row=len(details)+2,column=0,sticky=E)
      
    def bs():
        bsw=Tk()
        bsw.geometry("350x120")
        bsw.title("Service Booking")
        bsl=Label(bsw,text="What services do you require ?")
        bsl.grid(row=0,column=0)
        typel=Label(bsw,text="Type of AC:")
        typel.grid(row=1,column=0,sticky=E,pady=5)
        servl=Label(bsw,text="Select Service:")
        servl.grid(row=2,column=0,sticky=E,pady=5)
        
        typevalues=["Window","Split","Centralised"]
        typemenu=ttk.Combobox(bsw,values=typevalues,state='readonly')
        typemenu.set("Choose type of AC")
        typemenu.grid(row=1,column=1)
        servicevalues=["Servicing","Repair","Installation","Uninstallation"]
        servicemenu=ttk.Combobox(bsw,values=servicevalues,state='readonly')
        servicemenu.set("Choose service")
        servicemenu.grid(row=2,column=1)

        def pay1():
            if typemenu.get()=="Choose type of AC":
                messagebox.showerror("Invalid AC type","Choose valid type of AC")
            elif servicemenu.get()=="Choose service":
                messagebox.showerror("Invalid Service","Choose valid service")
            else:
                h=typemenu.get()
                g=servicemenu.get()
                bsl.destroy()
                typel.destroy()
                servl.destroy()
                typemenu.destroy()
                servicemenu.destroy()
                servbtn.destroy()
                
                servlabel=Label(bsw,text="Welcome to Payment Section")
                servlabel.grid(row=0,column=0)
                methl=Label(bsw,text="Method of Payment:")
                methl.grid(row=1,column=0,sticky=E,pady=10)
                methodvalues=["UPI","Debit card/Credit card","Cash on delivery"]
                methodmenu=ttk.Combobox(bsw,values=methodvalues,state='readonly')
                methodmenu.set("Choose method of payment")
                methodmenu.grid(row=1,column=1)
                scodestr="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
                scode=random.sample(scodestr,6)
                book_id="".join(scode)
                def place_service():
                    if methodmenu.get()=="Choose method of payment":
                        messagebox.showerror("Invalid Payment Method","Choose a valid method of payment")
                    else:
                        plsbtn.config(state='disabled')
                        squery="insert into services values(%s,%s,%s,%s,%s,%s)"
                        svalues=(book_id,h,g,s[0][0],s[0][1],s[0][2])
                        c.execute(squery,svalues)
                        db.commit()
                        sresponse=messagebox.askyesno("Booking Confirmation","Your service has been booked with booking ID: "+book_id+"""\nNote: Please remember this booking ID
in case of cancellation of service.\nAn SMS will be sent to your registered mobile number.
Do you wish to exit?\nClick Yes to exit.\nClick No to return to the start section.""")
                        if sresponse==1:
                            bsw.destroy()
                            root.destroy()
                        if sresponse==0:
                            bsw.destroy()
                            
                plsbtn=Button(bsw,text="Book Service",command=place_service)
                plsbtn.grid(row=2,column=1)
        servbtn=Button(bsw,text="Proceed to payment section",command=pay1)
        servbtn.grid(row=3,column=1,sticky=W,pady=10)
        
    def cs():
        csquery="select booking_id,type,service from services where name=%s and address=%s and mobileno=%s"
        csvalues=(s[0][0],s[0][1],s[0][2])
        c.execute(csquery,csvalues)
        cs=c.fetchall()
        if cs==[]:
            messagebox.showinfo("No Previous Services Booked","You have not booked any service.\nTo book a service, click Book Services in the start section.")
        else:
            csw=Tk()
            csw.title("Service Cancellation")
            csw.geometry("350x150")
            csl=Label(csw,text="What service would you like to cancel ?")
            csl.grid(row=0,column=0)
            for i in cs:
                label=Label(csw,text="Booking ID:- "+i[0]+": "+i[2]+" of "+i[1]+" AC")
                label.grid(row=cs.index(i)+1,column=0)

            csenl=Label(csw,text="Enter the booking ID:")
            csenl.grid(row=len(cs)+1,column=0,sticky=E,pady=10)
            csen=Entry(csw)
            csen.focus()
            csen.grid(row=len(cs)+1,column=1)
            bids=[]
            for i in cs:
                bids.append(i[0])

            def cb():
                if csen.get().upper() not in bids:
                        messagebox.showerror("Invalid Booking ID","Enter a valid Booking ID from amongst the following options.")
                else:
                    csvalue=csen.get().upper()
                    c.execute("delete from services where booking_id=%s",(csvalue,))
                    db.commit()
                    csresponse=messagebox.askyesno("Exit/Return to Start","The service has been cancelled.\nDo you wish to exit?")
                    if csresponse==1:
                        csw.destroy()
                        root.destroy()
                    elif csresponse==0:
                        csw.destroy()
                
            cbbtn=Button(csw,text="Cancel Booking",command=cb)
            cbbtn.grid(row=len(cs)+2,column=1)
        
          
    root.geometry("600x200+550+300")
    start1=Label(root,text="Welcome to Start Section, "+str(s[0][0]))
    start1.grid(row=0,column=0,padx=20,sticky=W)
    start2=Label(root,text="Choose any one of the following options to proceed")
    start2.grid(row=0,column=1,padx=20,sticky=W)
    
    bobtn=Button(root,text="Book Orders",command=bo)
    bsbtn=Button(root,text="Book Services",command=bs)
    cobtn=Button(root,text="Cancel Orders",command=co)
    csbtn=Button(root,text="Cancel Services",command=cs)
    
    bobtn.grid(row=1,column=0,pady=10)
    bsbtn.grid(row=1,column=1,pady=10)
    cobtn.grid(row=2,column=0,pady=10)
    csbtn.grid(row=2,column=1,pady=10)
    
    

def login():
    global loginbtn1
    global wel
    global signupbtn
    wel.destroy()
    signupbtn.destroy()
    loginbtn1.destroy()
    root.title("Login Section")
    unl=Label(root,text="Username")
    pwl=Label(root,text="Password")
    
    unl.grid(row=0,column=0,pady=2)
    pwl.grid(row=1,column=0,pady=4)

    un=Entry(root,bd=2,font=("Helvetica",10))
    pw=Entry(root,show="*",bd=2,font=("Helvetica",10))
    un.focus()
    un.grid(row=0,column=1)
    pw.grid(row=1,column=1)

    def check():
        global x
        global y
        query="select username,password from customers where username=%s and password=%s"
        values=(un.get(),pw.get())
        c.execute(query,values)
        result=c.fetchall()
        if result==[]:
            messagebox.showwarning("Login Error","The credentials you entered don't exist\nTry Again")
            un.delete(0,END)
            pw.delete(0,END)
            un.focus()
            
        elif result[0]==(un.get(),pw.get()):
            x=un.get()
            y=pw.get()
            un.destroy()
            pw.destroy()
            unl.destroy()
            pwl.destroy()
            loginbtn2.destroy()
            start()
            
    loginbtn2=Button(root,text="Login",command=check,bd=3)
    loginbtn2.grid(row=2,column=1)
    
def signup():
    global loginbtn1
    global wel
    global signupbtn
    root.geometry("250x150+500+300")
    root.title("Signup Section")
    wel.destroy()
    signupbtn.destroy()
    loginbtn1.destroy()
    
    nl=Label(root,text="Full Name",pady=2)
    unl=Label(root,text="Username",pady=2)
    pwl=Label(root,text="Password",pady=2)
    mnl=Label(root,text="Mobile Number",pady=2)
    adl=Label(root,text="Address",pady=4)

    nl.grid(row=0,column=0)
    unl.grid(row=1,column=0)
    pwl.grid(row=2,column=0)
    mnl.grid(row=3,column=0)
    adl.grid(row=4,column=0)

    n=Entry(root,bd=2)
    un=Entry(root,bd=2)
    pw=Entry(root,show="*",bd=2)
    mn=Entry(root,bd=2)
    ad=Entry(root,bd=2)
    n.focus()

    n.grid(row=0,column=1)
    un.grid(row=1,column=1)
    pw.grid(row=2,column=1)
    mn.grid(row=3,column=1)
    ad.grid(row=4,column=1)

    def add():
        global x
        global y
        db=msc.connect(host="localhost",user="root",passwd="abcd1234",database="project")
        c=db.cursor()
        x=un.get()
        y=pw.get()
        query="insert into customers values(%s,%s,%s,%s,%s)"
        values=(n.get(),un.get(),pw.get(),int(mn.get()),ad.get())
        c.execute(query,values)
        db.commit()
        n.destroy()
        un.destroy()
        pw.destroy()
        mn.destroy()
        ad.destroy()
        nl.destroy()
        unl.destroy()
        pwl.destroy()
        mnl.destroy()
        adl.destroy()
        signbtn.destroy()
        start()
    signbtn=Button(root,text="Sign up",command=add,bd=3)
    signbtn.grid(row=5,column=1)
      
wel=Label(root,text="Welcome to 18" +u"\u00b0"+" celsius\n\nSignup if you are a new customer\nLogin if you are already registered")
wel.pack()
loginbtn1=Button(root,text="Login",command=login,bd=3)
loginbtn1.pack(pady=5)
signupbtn=Button(root,text="Sign up",command=signup,bd=3)
signupbtn.pack(pady=5)

root.mainloop()
