from Tkinter import *
import PIL
from PIL import ImageTk,Image
import predict
import Player


if __name__ == "__main__":

    ch=0
    flag=0

    root=Tk()
    root.title('MATHEMATICAL MOZART')


    var = StringVar()
    var.set('Piano')


    #screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    heightblue=screen_height/5

    #frames
    frametop=Frame(root,width=screen_width,height=heightblue,bg='#b6e7fb')
    frametop.pack(side=TOP,fill=X)

    framemid=Frame(root,width=screen_width,height=2.3*heightblue,bg='white')
    framemid.pack(side=TOP,fill=X)

    framebot=Frame(root,width=screen_width,height=1.7*heightblue,bg='#b6e7fb')
    framebot.pack(side=TOP,fill=X)


    # -------------------------------------------------------------------------------------------------


    #logo
    img=Image.open("images/logo.jpg")
    img=ImageTk.PhotoImage(img)
    logolb=Label(frametop,height=100,width=100,image=img,borderwidth=0,highlightthickness=0)
    logolb.place(x=25,y=25)

    #key label
    keylb=Label(frametop,bg='#b6e7fb',fg='#0f3c4f',text='MATHEMATICAL MOZART',anchor=E)
    keylb.config(font=("Oswald", 45))
    keylb.place(x=170,y=40)


    # -------------------------------------------------------------------------------------------------


    def piano_choice():
        global ch
        ch=0
        var.set('Piano')
    
    def guitar_choice():
        global ch
        ch=1
        var.set('Guitar')

    def flute_choice():
        global ch
        ch=2
        var.set('Flute')

    def violin_choice():
        global ch
        ch=3
        var.set('Violin')


    # choose instrument
    keylb=Label(framemid,bg="white",fg='#0f3c4f',text='CHOOSE INSTRUMENT',anchor=E)
    keylb.config(font=("Raleway Bold", 15))
    keylb.place(x=250,y=40)

    piano_img=Image.open("images/piano.jpg")
    piano_img=piano_img.resize((80,80),Image.ANTIALIAS)
    piano_img=ImageTk.PhotoImage(piano_img)
    logo_p=Button(framemid,height=80,width=80,image=piano_img,command=piano_choice)
    logo_p.place(x=270,y=100)
    
    guitar_img=Image.open("images/guitar.jpg")
    guitar_img=guitar_img.resize((80,80),Image.ANTIALIAS)
    guitar_img=ImageTk.PhotoImage(guitar_img)
    logo_g=Button(framemid,height=80,width=80,image=guitar_img,command=guitar_choice)
    logo_g.place(x=370,y=100)

    flute_img=Image.open("images/flute.jpg")
    flute_img=flute_img.resize((80,80),Image.ANTIALIAS)
    flute_img=ImageTk.PhotoImage(flute_img)
    logo_f=Button(framemid,height=80,width=80,image=flute_img,command=flute_choice)
    logo_f.place(x=270,y=200)

    violin_img=Image.open("images/violin.jpg")
    violin_img=violin_img.resize((80,80),Image.ANTIALIAS)
    violin_img=ImageTk.PhotoImage(violin_img)
    logo_v=Button(framemid,height=80,width=80,image=violin_img,command=violin_choice)
    logo_v.place(x=370,y=200)


    keylb=Label(framemid,bg="white",fg='#0f3c4f',textvariable = var,anchor=E)
    keylb.config(font=("Raleway Bold", 15))
    keylb.place(x=330,y=300)

    #---------------------

    # choose details
    keylb=Label(framemid,bg="white",fg='#0f3c4f',text='CHOOSE DETAILS',anchor=E)
    keylb.config(font=("Raleway Bold", 15))
    keylb.place(x=825,y=40)

    #duration label
    durlb=Label(framemid,fg="#0f3c4f",bg="white",text="Duration",anchor=E)
    durlb.config(font=("Raleway SemiBold",13),width=15)
    durlb.place(x=700,y=100)

    #duration menu
    dur_var = StringVar(root)
    dur_var.set("Short") # initial value
    durtb = OptionMenu(framemid, dur_var, "Short", "Medium", "Long")
    durtb.config(font=("Raleway",10),width=10,bg="white",borderwidth=1,highlightthickness=0)
    durtb.place(x=900,y=100)


    #tempo label
    durlb=Label(framemid,fg="#0f3c4f",bg="white",text="Tempo",anchor=E)
    durlb.config(font=("Raleway SemiBold",13),width=15)
    durlb.place(x=700,y=150)

    #tempo menu
    temp_var = StringVar(root)
    temp_var.set("Slow") # initial value
    tempb = OptionMenu(framemid, temp_var, "Short", "Fast")
    tempb.config(font=("Raleway",10),width=10,bg="white",borderwidth=1,highlightthickness=0)
    tempb.place(x=900,y=150)

    #meter label
    meterlb=Label(framemid,fg="#0f3c4f",bg="white",text="Meter (Optional)",anchor=E)
    meterlb.config(font=("Raleway SemiBold",13),width=15)
    meterlb.place(x=700,y=200)

    #meter menu
    meter_var = StringVar(root)
    meter_var.set("6/8") # initial value
    meterb = OptionMenu(framemid, meter_var, "6/8", "4/4", "8/8", "2/2")
    meterb.config(font=("Raleway",10),width=10,bg="white",borderwidth=1,highlightthickness=0)
    meterb.place(x=900,y=200)


    #key label
    keylb=Label(framemid,fg="#0f3c4f",bg="white",text="Key (Optional)",anchor=E)
    keylb.config(font=("Raleway SemiBold",13),width=15)
    keylb.place(x=700,y=250)

    #key menu
    key_var = StringVar(root)
    key_var.set("C") # initial value
    keyb = OptionMenu(framemid, key_var, "A", "B", "C", "D", "E", "F", "G")
    keyb.config(font=("Raleway",10),width=10,bg="white",borderwidth=1,highlightthickness=0)
    keyb.place(x=900,y=250)


    #---------------------------------------------------------------------------


    def gen():
        stopbut.place_forget()
        pausebut.place_forget()
        resbut.place_forget()
        global flag
        flag=1
        predict.predict_abc(ch,dur_var.get(),temp_var.get(),meter_var.get(),key_var.get())
        playbut.place(x=575,y=130)


    def pressplay():
        playbut.place_forget()
        resbut.place_forget()
        pausebut.place(x=575,y=130)
        stopbut.place(x=575,y=180)
        global flag
        if flag==0:
            Player.resume()
        else:
            Player.play()

    def presspause():
        global flag
        flag=0
        pausebut.place_forget()
        resbut.place(x=575,y=130)
        Player.pause()

    def pressstop():
        Player.stop()
        stopbut.place_forget()
        pausebut.place_forget()
        resbut.place_forget()
        global flag
        flag=1
        playbut.place(x=575,y=130)


    genbut=Button(framebot,bg="#0f3c4f",fg="white",text="GENERATE",command=gen)
    genbut.config(font=("Raleway Bold",15),width=15)
    genbut.place(x=575,y=80)


    playbut=Button(framebot,bg="#0f3c4f",fg="white",text="PLAY",command=pressplay)
    playbut.config(font=("Raleway Bold",15),width=15)
    playbut.place_forget()

    pausebut=Button(framebot,bg="#0f3c4f",fg="white",text="PAUSE",command=presspause)
    pausebut.config(font=("Raleway Bold",15),width=15)
    pausebut.place_forget()

    resbut=Button(framebot,bg="#0f3c4f",fg="white",text="RESUME",command=pressplay)
    resbut.config(font=("Raleway Bold",15),width=15)
    resbut.place_forget()

    stopbut=Button(framebot,bg="#0f3c4f",fg="white",text="STOP",command=pressstop)
    stopbut.config(font=("Raleway Bold",15),width=15)
    stopbut.place_forget()


    root.mainloop()