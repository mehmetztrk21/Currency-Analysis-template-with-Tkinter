# libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import win32com.client

window = tk.Tk()
window.geometry("1080x640")  #ana window
window.wm_title("Trading")

pw = ttk.PanedWindow(window, orient = tk.HORIZONTAL) #2 yapı yatay şekilde birleştiği için horizontal yaptık
pw.pack(fill = tk.BOTH, expand = True) #yatay ve dikeyde doldursun(fill yatay expand dikey)

w2 = ttk.PanedWindow(pw, orient = tk.VERTICAL) #f2 ve f3 ü tutuan paned window dikey olduğu için Vertical yaptık.

frame1 = ttk.Frame(pw, width = 360, height = 640, relief = tk.SUNKEN) #(relief=)sunken kenarlık demek
frame2 = ttk.Frame(pw, width = 720, height = 400, relief = tk.SUNKEN)
frame3 = ttk.Frame(pw, width = 720, height = 240, relief = tk.SUNKEN)

w2.add(frame2) #frame2 ve fram3 ü soldaki kısma dikey şekilde alt alta ekledik.
w2.add(frame3)

pw.add(w2) #panedwindow2 yi de ana paned windowa ekledik.
pw.add(frame1) #frame1 i zaten ana paned windowa ekliyoruz.

# frame1: treeview, open trade button (sağdaki kısım)

item = ""
def callback(event):  #treeviewe basılmaları kontrol eden fonksiyon.
    global item  #başka yerde de item i kullanaccağımız için item i global yaptık.
    item = treeview.identify("item", event.x,event.y) #basılan başlığı alıyor.
#    print("Clicked: ",item)
    
# treeview
treeview = ttk.Treeview(frame1)
treeview.grid(row = 0, column = 1, padx = 25 , pady = 25) #0.satır 1.sütun yandakilerden 25dp uzak alt ve üstten 25dp uzak
treeview.insert("", "0", "Major", text = "Major")
treeview.insert("Major", "1", "EUR/USD", text ="EUR/USD") #hangi başlığın altında ,sütunu kaç, ismi ne, texti ne
treeview.insert("", "2", "Minor", text = "Minor")
treeview.insert("Minor", "3", "EUR/GBR", text ="EUR/GBR")
treeview.bind("<Double-1>",callback) #iki kere basılırsa callback e git.(tıklama kontrolü bind ile oluyor.)

def readNews(item):
    
    if item == "EUR/USD":
        news = pd.read_csv("C:\\Users\\User\\Desktop\\veri_setleri\\news_EURUSD.txt") #klasördeki içeriği al
    elif item == "EUR/GBR":
        news = pd.read_csv("C:\\Users\\User\\Desktop\\veri_setleri\\news_EURGBR.txt")
    textBox.insert(tk.INSERT, news) #textboxa yapıştır.

def openTrade():
    global data, future, line, canvas, data_close_array, future_array, ax1,line2,canvas2,ax2,line3,canvas3,ax3,line4,canvas4,ax4 #bunları başka bir fonksiyonda da kullanacağımız için global tanımlamamız lazım.
    print("openTrade")
    if item != "":  #eğer item(yani treewievde birşey seçtiysek.)
        print("Chosen item: ",item )
        
        if item == "EUR/USD": #eğer bunu seçmişsek
            # button setting
            open_button.config(state = "disabled") #open butonunu pasif et.
            start_button.config(state = "normal") #start butonunu aktif et.
            
            # read data
            data = pd.read_csv("C:\\Users\\User\\Desktop\\veri_setleri\\eurusd.csv") #eur/usd verisini getirdik.
            
            # split data
            future = data[-1000:] #sondaki 100 tane veriyi futureye attık.
            data = data[:len(data)-1000] #geri kalan veriyi dataya attık.
            data_close_array = data.close1.values #tablodaki kapanış değerlerinin değerlerini aldık.
            future_array = list(future.close1.values) #futuredeki kapanış değerlerini aldık.
            
            # line
            fig1 = plt.Figure(figsize =(5,4), dpi = 100) #bu hep var zaten 500*400px lik bir figür oluşturduk.
            ax1 = fig1.add_subplot(111) #1.satır 1.sütuna bir tane plot koyacağız demek(111)
            line, = ax1.plot(range(len(data)),data.close1,color = "blue") #x ekseni datanın boyu kadar y ekseni datanın close sütunu değerleri,renk mavi
            
            canvas = FigureCanvasTkAgg(fig1, master = tab1) 
            canvas.draw() #çizdir.
            canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True) #yukarıda heryeri doldursun.

            # scatter  (line ile aynı şeyler hemen hemen)
            fig2 = plt.Figure(figsize =(5,4), dpi = 100)
            ax2 = fig2.add_subplot(111)
            line2 = ax2.scatter(range(len(data)),data.close1,s = 1, alpha = 0.5, color = "blue") #alpha(saydamlık),size= noktanın boyutları
            
            canvas2 = FigureCanvasTkAgg(fig2, master = tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
            
            # read news
            readNews(item) #read news fonksiyonuna git.
            
        elif item == "EUR/GBR": #eğer tercih buysa
            
            # button setting
            open_button.config(state = "disabled")
            start_button.config(state = "normal")
            
            # read data
            data = pd.read_csv("C:\\Users\\User\\Desktop\\veri_setleri\\eurgbr.csv")
            
            # split data
            future = data[-1000:]
            data = data[:len(data)-1000]
            data_close_array = data.close1.values
            future_array = list(future.close1.values)
            
            # line
            fig3 = plt.Figure(figsize =(5,4), dpi = 100)
            ax3 = fig3.add_subplot(111)
            line3, = ax3.plot(range(len(data)),data.close1,color = "blue")
            
            canvas3 = FigureCanvasTkAgg(fig3, master = tab1)
            canvas3.draw()
            canvas3.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

            # scatter
            fig4 = plt.Figure(figsize =(5,4), dpi = 100)
            ax4 = fig4.add_subplot(111) #eksen
            line4 = ax4.scatter(range(len(data)),data.close1,s = 1, alpha = 0.5, color = "blue")
            
            canvas4 = FigureCanvasTkAgg(fig4, master = tab2)
            canvas4.draw()
            canvas4.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)  #ekpan=1 denemk expand=Trrue aynı şey
            
            # read news
            readNews(item) #read news fonksiyonuna git.
            
        else:
            messagebox.showinfo(title = "Warning", message = "Double click to choose currency pair")# eğer ikisinden biri değilse uyarı ver.
    else:
        messagebox.showinfo(title = "Warning", message = "Double click to choose currency pair")#eğer başka bir hata ile karşılaşırsa da hata mesajı ver.
          
# button
open_button = tk.Button(frame1, text = "Open Trading", command = openTrade)
open_button.grid(row = 2, column = 1, padx = 5, pady = 5)

# frame3: text editor (fundamental analysis), scroll bar #text kısmı(sol alt)

textBox = tk.Text(frame3, width = 70, height = 10, wrap = "word") #wrap yani kelimeleri alacak anlamına geliyor.
textBox.grid(row = 0, column = 0, padx =25, pady = 25) #frame3 te 0.satır 0.sütun anlamına geliyor.
scroll = tk.Scrollbar(frame3, orient = tk.VERTICAL, command = textBox.yview)#dikey olacağı için orient vertical olacağı için,textbox ın y ekseni olacağı için fonksiyonu o yaptık.
scroll.grid(row = 0, column = 1, sticky = tk.N + tk.S, pady=10) #sol dikey kısma yerleştirdik.
textBox.config(yscrollcommand = scroll.set) #text baksa etki etmesini sağladık.


# frame2: tab view, radio button, button, result(labelframe), plot

tabs = ttk.Notebook(frame2, width = 540, height = 300) #line ve scatter için tab oluşurduk.
tabs.place(x = 25, y= 25)

tab1 = ttk.Frame(tabs, width = 50, height = 50) #line tabı
tab2 = ttk.Frame(tabs) #scatter tabı genişlik ve yüksekliği üst satırda tanımlaığımız için yeter.

tabs.add(tab1, text = "Line") #tab1 ve tab2 yi tabs a koyduk.
tabs.add(tab2, text = "Scatter", compound = tk.LEFT) #tab2 yi sola yatık yaaptık(tab1 ile yapışsın diye.)

# radio button
method = tk.StringVar()
tk.Radiobutton(frame2, text = "m1: ", value = "m1", variable = method).place(x = 580, y= 100)
tk.Radiobutton(frame2, text = "m2: ", value = "m2", variable = method).place(x = 580, y= 125)

# label frame: result
label_frame = tk.LabelFrame(frame2, text = "Result", width = 100, height = 150)#başlıklı frame
label_frame.place(x = 580, y = 25)
tk.Label(label_frame, text = "Buy: ", bd = 3).grid(row = 0, column = 0) #üstte bu olsun
tk.Label(label_frame, text = "Sell: ", bd = 3).grid(row = 1, column = 0)#altta bu olsun(grid ile)
  
# buy sell labels
buy_value = tk.Label(label_frame, text = "1", bd = 3) #alış ve satış değerleri için labeller.
buy_value.grid(row = 0, column = 1)
sell_value = tk.Label(label_frame, text = "0", bd = 3)
sell_value.grid(row = 1, column = 1)

def moving_average(a, n = 50):
    ret = np.cumsum(a, dtype= float) #gelen verideki bütün verileri topla(veritipini float yap.)
    ret[n:] = ret[n:] - ret[:-n] #matematiksel işlemler.(güncelleme için)
    return ret[n-1:]/n 
    
def update():
    global data_close_array, ax1,ax2,ax3,ax4
    
    spread = 0.0002 #kafadan attık.
    buy_value.config(text = str((data_close_array[-1]-spread).round(5))) #bu matematiksel işlemi tamamen kafadan attık
    sell_value.config(text = str((data_close_array[-1]+spread).round(5))) #round virgülden sonra 5 basamak olsun demek
    
    window.after(500, update) #yarım saniyede bir güncelle(update fonksiyonuna git.)
    
    data_close_array = np.append(data_close_array,future_array.pop(0)) #data_close_arrayın sonuna future_array in ilk elemanını ekliyoru her seferinde.
    
    if method.get() == "m1": #eğer method 1 i seçmişsek:
        if item == "EUR/USD": #treeviewde eur/usd yi seçmişsek
            # line
            ax1.set_xlim(0,len(data_close_array) + 10) #grafiği güncelleyecek bilgiyi yazdık.
            line.set_ydata(data_close_array) #y eksenini güncelledik.
            line.set_xdata(range(len(data_close_array)))#y eksenini güncelledik.
            
            # scatter
            ax2.set_xlim(0,len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue") #scatter grafiğini güncellemek için yaptık.
            
            # moving average
            n = 50 #sallama rakam
            mid_rolling = moving_average(data_close_array,n) #fonksiyona gönderdik.
            ax1.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red") #n-1 den data_clos arrayın uzuunluğuna kadar.
            ax2.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            
            canvas.draw()
            canvas2.draw()  #çizdirmek için.
        
        elif item == "EUR/GBR": #üstteki ile aynı işler.
            # line
            ax3.set_xlim(0,len(data_close_array) + 10)
            line3.set_ydata(data_close_array)
            line3.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax4.set_xlim(0,len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 50
            mid_rolling = moving_average(data_close_array,n) #fonksiyona gönderdik.
            ax3.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            ax4.plot(range(n-1,len(data_close_array)),mid_rolling,linestyle = "--", color = "red")
            
            canvas3.draw()
            canvas4.draw()
            
    elif method.get() == "m2":
        if item == "EUR/USD":
            # line
            ax1.set_xlim(0,len(data_close_array) + 10)
            line.set_ydata(data_close_array)
            line.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax2.set_xlim(0,len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 200
            long_rolling = moving_average(data_close_array,n)
            ax1.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            ax2.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            
            canvas.draw()
            canvas2.draw()
        
        elif item == "EUR/GBR":
            # line
            ax3.set_xlim(0,len(data_close_array) + 10)
            line3.set_ydata(data_close_array)
            line3.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax4.set_xlim(0,len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            # moving average
            n = 200
            long_rolling = moving_average(data_close_array,n)
            ax3.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            ax4.plot(range(n-1,len(data_close_array)),long_rolling,linestyle = "--", color = "green")
            
            canvas3.draw()
            canvas4.draw()
    else:   #m1 veya m2 seçilmemişse sadece grafiği çizdir.güncelleme yapma.
        if item == "EUR/USD":
            # line
            ax1.set_xlim(0,len(data_close_array) + 10)
            line.set_ydata(data_close_array)
            line.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax2.set_xlim(0,len(data_close_array) + 10)
            ax2.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            canvas.draw()
            canvas2.draw()
        elif item == "EUR/GBR":
            # line
            ax3.set_xlim(0,len(data_close_array) + 10)
            line3.set_ydata(data_close_array)
            line3.set_xdata(range(len(data_close_array)))
            
            # scatter
            ax4.set_xlim(0,len(data_close_array) + 10)
            ax4.scatter(range(len(data_close_array)), data_close_array, s = 1, alpha = 0.5, color = "blue")
            
            canvas3.draw()
            canvas4.draw()
           
# button
def startTrading():
    window.after(0,update) #butona basılır basılmaz update metoduna git.
    print("startTrading")
    
start_button = tk.Button(frame2, text = "Start Trading", command = startTrading)
start_button.place(x=580, y = 150)
start_button.config(state = "disabled")#ilk başta pasif olmasını istiyoruz.(opene basınca bu aktif olsun istiyoruz.)



























window.mainloop()











