import Tkinter
import os

from api import *


class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    

    def initialize(self):

        top1=Tkinter.Label(self,text="RITI",fg="red",font=("Times New Roman",12))
        top1.grid(row=0,column=2)
        top2=Tkinter.Label(self,text="By Cluster Innovation Centre",fg="black",font=("Times New Roman",8))
        top2.grid(row=1,column=2)
        top3=Tkinter.Label(self)
        top3.grid(row=2,pady=8)
        
        label1=Tkinter.Label(self,text="Encryption:-")
        label1.grid(row=3)

        toplabel=Tkinter.Label(self,text="Enter text to be encrypted:-")
        toplabel.grid(row=4)
        
        self.entryvar1=Tkinter.StringVar()
        entry1=Tkinter.Entry(self,textvariable=self.entryvar1)
        entry1.grid(row=4,column=2)
        

        toplabel2=Tkinter.Label(self,text="Enter Multiplier(a):-")
        toplabel2.grid(row=5)

        self.entryvar2=Tkinter.IntVar()
        entry2=Tkinter.Entry(self,textvariable=self.entryvar2)
        entry2.grid(row=5,column=2)
        

        toplabel2=Tkinter.Label(self,text="Enter Magnitude shift(b):-")
        toplabel2.grid(row=6)

        self.entryvar3=Tkinter.IntVar()
        entry3=Tkinter.Entry(self,textvariable=self.entryvar3)
        entry3.grid(row=6,column=2)
        

        label9=Tkinter.Label(self,text="Encrypted text:-")
        label9.grid(row=7,column=4)

        

        btn1=Tkinter.Button(self,text="Encrypt",command=self.enc)
        btn1.grid(row=7,column=2)

        pdlabel=Tkinter.Label(self,pady=5)
        pdlabel.grid(row=8)
        self.testvar=Tkinter.StringVar()
        testbox1=Tkinter.Entry(self,textvariable=self.testvar)
        testbox1.grid(row=7,column=5)
        

        pdlabel3=Tkinter.Label(self,pady=8)
        pdlabel.grid(row=10)

        label2=Tkinter.Label(self,text="Decryption:-")
        label2.grid(row=11)


        toplabel3=Tkinter.Label(self,text="Enter cipher text:-")
        toplabel3.grid(row=12)
        
        self.entryvar4=Tkinter.StringVar()
        entry4=Tkinter.Entry(self,textvariable=self.entryvar4)
        entry4.grid(row=12,column=2)
      

        toplabel4=Tkinter.Label(self,text="Enter Multiplier(a):-")
        toplabel4.grid(row=13)

        self.entryvar5=Tkinter.IntVar()
        entry5=Tkinter.Entry(self,textvariable=self.entryvar5)
        entry5.grid(row=13,column=2)
        

        toplabel5=Tkinter.Label(self,text="Enter Magnitude shift(b):-")
        toplabel5.grid(row=14)

        self.entryvar6=Tkinter.IntVar()
        entry6=Tkinter.Entry(self,textvariable=self.entryvar6)
        entry6.grid(row=14,column=2)
       
        btn2=Tkinter.Button(self,text="Decrypt",command=self.enc2)
        btn2.grid(row=15,column=2)
        
        label10=Tkinter.Label(self,text="Decrypted text:-")
        label10.grid(row=15,column=4)


        self.testvar2=Tkinter.StringVar()
        testbox2=Tkinter.Entry(self,textvariable=self.testvar2)
        testbox2.grid(row=15,column=5)
        
        pdlabel3=Tkinter.Label(self,pady=5)
        pdlabel3.grid(row=16)

        label4=Tkinter.Label(self,text="Frequency analysis:-")
        label4.grid(row=17)

        toplabel5=Tkinter.Label(self,text="Enter text to break:-")
        toplabel5.grid(row=18)

        self.entryvar10=Tkinter.StringVar()
        entry8=Tkinter.Entry(self,textvariable=self.entryvar10)
        entry8.grid(row=18,column=2)

        btn4=Tkinter.Button(self,text="Crack",command=self.enc4)
        btn4.grid(row=19,column=2)

        label13=Tkinter.Label(self,text="Cracked text:-")
        label13.grid(row=19,column=4)


        self.entryvar11=Tkinter.StringVar()
        entry11=Tkinter.Entry(self,textvariable=self.entryvar11)
        entry11.grid(row=19,column=5)
        


        pdlabel2=Tkinter.Label(self,pady=5)
        pdlabel2.grid(row=23)

        label3=Tkinter.Label(self,text="Brute force break:-")
        label3.grid(row=24)

        toplabel4=Tkinter.Label(self,text="Enter text to break:-")
        toplabel4.grid(row=25)

        toplabel15=Tkinter.Label(self,text="Enter accuracy(integer):-")
        toplabel15.grid(row=26)

        self.anothervar=Tkinter.IntVar()
        lb=Tkinter.Entry(self,textvariable=self.anothervar)
        lb.grid(row=26,column=2)

        self.entryvar7=Tkinter.StringVar()
        entry7=Tkinter.Entry(self,textvariable=self.entryvar7)
        entry7.grid(row=25,column=2)
        

        btn3=Tkinter.Button(self,text="Break",command=self.enc3)
        btn3.grid(row=27,column=2)

        label11=Tkinter.Label(self,text="Cracked text:-")
        label11.grid(row=27,column=4)

        label12=Tkinter.Label(self,text="a:-")
        label12.grid(row=28,column=4)

        self.something=Tkinter.IntVar()
        label14=Tkinter.Label(self,textvariable=self.something)
        label14.grid(row=28,column=5)

        

        label13=Tkinter.Label(self,text="b:-")
        label13.grid(row=29,column=4)

        self.var2=Tkinter.IntVar()
        label15=Tkinter.Label(self,textvariable=self.var2)
        label15.grid(row=29,column=5)

        bottomlbl=Tkinter.Label(self,text="                    Brute force may take some time")
        bottomlbl.grid(row=29)


        self.entryvar8=Tkinter.StringVar()
        label3=Tkinter.Entry(self,textvariable=self.entryvar8)
        label3.grid(row=26,column=5)
        
        
        self.geometry('640x600')


    def enc(self):
        obs=self.entryvar1.get()
        a=self.entryvar2.get()
        b=self.entryvar3.get()
        try:
            ans=g_encrypt(obs,a,b).read()
        except:
            ans="Multiplier not valid"
        self.testvar.set(ans)

    def enc2(self):
        
        obs=self.entryvar4.get()
        a=self.entryvar5.get()
        b=self.entryvar6.get()
        ans=g_decrypt(obs,a,b).read()
        self.testvar2.set(ans)
        
        

    def enc3(self):
        self.entryvar8.set("Please wait.")
        obs=self.entryvar7.get()
        obs2=self.anothervar.get()
        ans=g_break(obs,obs2)
        print ans
        if ans != None:
            cracked=ans[0].read()
        else:
            cracked="fail"
        self.entryvar8.set(cracked)
        
        self.something.set(ans[1])
        self.var2.set(ans[2])

    def enc4(self):
        obs=self.entryvar10.get()
        ans=g_break_f(obs).read()
        self.entryvar11.set(ans)




if __name__ =="__main__":
    app=simpleapp_tk(None)
    app.title('Affine Cipher')
    app.mainloop()
