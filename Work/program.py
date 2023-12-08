import numpy as np 
import numpy.random as rnd
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
import tkinter as tk
from tkinter import ttk, filedialog
import xlsxwriter
import math


def barchart():
    """
    This function makes bar chart of 2018 population by continent
    
    Author: Vladimir Volkov
    """
    global figure, ax
    
    piv2 = pd.pivot_table(data, index=["Continent"], values=[2018], aggfunc={2018: np.sum})
    
    continents = piv2.index.array
    ypos = np.arange(len(continents))
    
    populations = []
    for i in range(len(continents)):
        populations.append(piv2.values[i][0])
    
    
    ax.clear()
    ax.bar(continents, populations, color='midnightblue')
    ax.xaxis.set_tick_params(labelsize=7)
    ax.set_ylabel("population")
    ax.set_title('2018 population by continent')
    chart.draw()
    bar_describtion.config(text="Bar chart of 2018 population\n by continent")
    
def hist():
    """
    This function makes hist chart
        
    Author: Dima Buchelnikov
    """
    global figure, ax
    ax.clear()
    ax.hist(x=data[2018], density=True, bins=100)
    ax.set_ylabel('Number of countries')
    ax.set_xlabel('Populations')
    chart.draw()
    bar_describtion.config(text="Hist chart")

def boxplot():
    """
    This function makes boxplot chart
        
    Author: Arkadiy Drevalev
    """
    global figure, ax
    ax.clear()
    data1 = [data[1950], data[1960], data[1970], data[1980], data[1990], data[2000], data[2010], data[2018]]
    ax.set_xticklabels(['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2018'])
    ax.boxplot(data1)
    chart.draw()
    bar_describtion.config(text="Boxplot chart,\ndots are countries")


def scatter():
    """
    This function makes scatter chart
        
    Author: Dima Buchelnikov
    """
    global figure, ax, data
    
    maximum = data[data.columns[-1]].max()
    ax.clear()
    ax.set_xlim([0, maximum])
    ax.set_ylim([0, maximum])
    ax.plot([0, maximum], [0, maximum])
    ax.scatter(data[2010], data[2018], color = 'hotpink')
    ax.set_title('y=x is the blue line')
    ax.set_ylabel('Populations by 2018')
    ax.set_xlabel('Populations by 2010')
    chart.draw()
    bar_describtion.config(text="Scatter chart\n countries below blue line\n are having problems\n with demography")
    
    
def report1(T):
    """
    This function prints a list of countries with population less than 1 million
    
    Argument: scrolledtext element for inserting result
        
    Author: Vladimir Volkov
    """
    desc = "List of countries with population less than 1 million\n\n\n"
    
    rp1 = pd.DataFrame(columns=['Country', 'Continent', '2018 population'])
    
    for i in range(len(data)):
        if (data.loc[i][2018] < 1000000):
            rp1 = rp1.append({'Country': data.loc[i]['Country'], 
                              'Continent': data.loc[i]['Continent'], 
                              '2018 population': int(data.loc[i][2018])}, 
                             ignore_index=True)
            
    T.delete("1.0","end")
    T.insert(END, desc)
    T.insert(END, rp1)
    
    
def report2(T):
    """
    This function prints a list of countries with population decrease between 2010 and 2018
    
    Argument: scrolledtext element for inserting result
        
    Author: Vladimir Volkov
    """
    desc = "List of countries with population decrease between 2010 and 2018\n\n"
    
    rp2 = pd.DataFrame(columns=['Country', 'Continent', '2018 population'])
    
    for i in range(len(data)):
        if (data.loc[i][2018] < data.loc[i][2010]):
            rp2 = rp2.append({'Country': data.loc[i]['Country'], 
                              'Continent': data.loc[i]['Continent'], 
                              '2018 population': int(data.loc[i][2018])}, 
                             ignore_index=True)
    T.delete("1.0","end")
    T.insert(END, desc)
    T.insert(END, rp2)
    
    
def report3(T):
    """
    This function prints a list of North and South America countries with population > 100 million
    
    Argument: scrolledtext element for inserting result
        
    Author: Arkadiy Drevalev
    """
    desc = "List of North and South America with population > 100 million\n\n"
    
    rp3 = pd.DataFrame(columns=['Country', 'Continent', '2018 population'])
    
    for i in range(len(data)):
        if ((data.loc[i]['Continent'] == "North America" or data.loc[i]['Continent'] == "South America") and data.loc[i][2018] > 100000000):
            rp3 = rp3.append({'Country': data.loc[i]['Country'], 
                              'Continent': data.loc[i]['Continent'], 
                              '2018 population': int(data.loc[i][2018]*1000)}, 
                             ignore_index=True)

    T.delete("1.0","end")
    T.insert(END, desc)
    T.insert(END, rp3)
    
    
def pivot_table_reports(T):
    """
    This function makes a table of continents, countries, 2018 populations and a table of continents with their overall 2018 populations 
    
    Argument: scrolledtext element for inserting result
        
    Author: Dima Buchelnikov
    """
    piv1 = pd.pivot_table(data, index=["Continent", "Country"], values=[2018])
    piv2 = pd.pivot_table(data, index=["Continent"], values=[2018], aggfunc={2018: np.sum})

    T.delete("1.0","end")
    T.insert(END, "Table of continents, countries, 2018 populations\n\n")
    T.insert(END, piv1.to_string())
    T.insert(END, "\n\nTable of continents with their overall 2018 populations\n\n")
    T.insert(END, piv2.to_string())
    
    
def file_open_xl():
    """
    This function shows an open file dialog. When file selected, it loads excel chart into "data" dataframe and calls treeview_update() function
    When something goes wrong, Error message appears.
        
    Author: Arkadiy Drevalev
    """
    global filename, data
    filename_1 = filedialog.askopenfilename(
        initialdir="C:/",
        title = "Open A File",
        filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*"))
        )
    if filename_1:
        try:
            df = pd.read_excel(filename_1)
            filename = filename_1
            data = df
            treeview_update(df)
            label_file.config(text="Loaded successfully")
        except:
            label_file.config(text="Error")
            
def file_save_xl():
    """
    This function saves a "data" dataframe into a file
        
    Author: Dima Buchelnikov
    """
    global filename, data

    filename_2 = filedialog.askopenfilename(
        initialdir="C:/",
        title = "Save File",
        filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*"))
        )
    with pd.ExcelWriter(filename_2, engine='xlsxwriter') as writer:
        data.to_excel(writer)
    label_file.config(text="Saved to %s" % filename_2)
            

def treeview_update(df):
    """
    This function clears treeview table using clear_tree() function and sets it up with given dataframe
    
    Arguments: dataframe
    Returns: none
        
    Author: Vladimir Volkov
    """
    # Clear old treeview
    clear_tree()
    # Set up new treeview
    my_tree["column"] = list(df.columns)
    my_tree["show"] = "headings"
    # Loop thru column list for headers
    for column in my_tree["column"]:
        my_tree.heading(column, text=column)
        my_tree.column(column, width=80)
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("", "end", values=row)
        
        
def clear_tree():
    """
    This function clears treeview table
    
    Author: Vladimir Volkov
    """
    my_tree.delete(*my_tree.get_children())
    

def delete_row():
    """
    This function deletes row in a "data" dataframe and calls treeview_update(data) to update treeview table
    
    Author: Arkadiy Drevalev
    """
    global data, erase
    country = erase.get()
    data = data.drop(data.loc[data['Country'] == country].index.array[0])
    treeview_update(data)
    label_file.config(text="Deleted successfully")
    


#----------------------------Configuring tabs----------------------------------


filename = "populations.xlsx"
try:
    data = pd.read_excel(filename)
except:
    print("no file")
root = Tk()
root.title("Program")
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Data')
tabControl.add(tab2, text ='Graphs')
tabControl.add(tab3, text ='Text reports')
tabControl.add(tab4, text ='Graph Tool')
tabControl.pack(expand = 1, fill ="both")
root.geometry("700x500") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0)



#----------------------------Configuring 1st tab----------------------------------

frame1 = tk.Frame(tab1)
frame1.place(height=400, width=700)
my_tree = ttk.Treeview(frame1, height = 33, selectmode = "extended")
my_tree.place(relheight=1, relwidth=1)
treescrolly = tk.Scrollbar(frame1, orient="vertical", command=my_tree.yview)
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=my_tree.xview)
my_tree.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")


try:
    treeview_update(data)
except:
    print("")
    
erase = Entry(tab1)
erase.place(rely=0.85, relx=0.15)


delete_row = tk.Button(tab1, text="Delete row by country", command=delete_row)
delete_row.place(rely=0.9, relx=0.15)



    

button1 = tk.Button(tab1, text="Save File", command=lambda: file_save_xl())
button1.place(rely=0.85, relx=0.55)
button2 = tk.Button(tab1, text="Load File", command=lambda: file_open_xl())
button2.place(rely=0.85, relx=0.35)
label_file = ttk.Label(tab1, text="No messages")
label_file.place(rely=0.96, relx=0.43)



#----------------------------Configuring 2nd tab----------------------------------



barchart_button = Button(tab2, text="  Bar chart  ", padx=0, pady=0, font=('Consolas', 10), command=lambda:barchart())
barchart_button.grid(row=1, column=1)
    
hist_button = Button(tab2, text=" Hist chart ", padx=0, pady=0, font=('Consolas', 10), command=lambda:hist())
hist_button.grid(row=1, column=2)
    
boxplot_button = Button(tab2, text="Boxplot chart", padx=0, pady=0, font=('Consolas', 10), command=lambda:boxplot())
boxplot_button.grid(row=2, column=1)
    
scatter_button = Button(tab2, text="Scatter chart", padx=0, pady=0, font=('Consolas', 10), command=lambda:scatter())
scatter_button.grid(row=2, column=2)
    
bar_describtion = Label(tab2, text="description", font=('Arial', 11))
bar_describtion.grid(row=3, column=1, columnspan=2)
figure = plt.figure(figsize = (5,4), dpi = 100)
ax = figure.add_subplot(111)
chart = FigureCanvasTkAgg(figure, master=tab2)
chart.get_tk_widget().grid(row = 1, column = 0, rowspan=10)
toolbarFrame = Frame(master=tab2)
toolbar = NavigationToolbar2Tk(chart, toolbarFrame)
toolbarFrame.grid(row = 11, column = 0, rowspan=1, sticky="W")



#----------------------------Configuring 3rd tab----------------------------------
    


ttk.Label(tab3,
        text =" ").grid(column = 0,
                            row = 2,
                            padx = 10,
                            pady = 30)
report1_button = Button(tab3, text="Text 1", padx=0, pady=10, font=('Consolas', 15), command=lambda:report1(T))
report1_button.grid(row=1, column=1)
    
report2_button = Button(tab3, text="Text 2", padx=0, pady=10, font=('Consolas', 15), command=lambda:report2(T))
report2_button.grid(row=2, column=1)
report3_button = Button(tab3, text="Text 3", padx=0, pady=10, font=('Consolas', 15), command=lambda:report3(T))
report3_button.grid(row=3, column=1)
    
pivot_button = Button(tab3, text=" Pivot ", padx=0, pady=10, font=('Consolas', 15), command=lambda:pivot_table_reports(T))
pivot_button.grid(row=4, column=1)
ttk.Label(tab3,
        text =" ").grid(column = 2,
                            row = 2,
                            padx = 10,
                            pady = 30)
T = scrolledtext.ScrolledText(tab3, height = 28, width = 65) 
T.grid(row=1, column=3, rowspan=15, columnspan=4)



#----------------------------Configuring 4th tab----------------------------------





def loadFile():
    
    '''
    This function shows open file dialog. When file choosed, function reads coordinates 
    from it and builds a graph.
    
    Author: Arkadiy Drevalev
    '''
    
    global y, x, figure, bx
    filepath = filedialog.askopenfilename(initialdir="C:\\",
                                          title="Load file",
                                          filetypes= (("Text files","*.txt"),
                                          ("all files","*.*")))
    x = []
    y = []
    file = open(filepath,'r')
    
    while True:
        try:
            x_input, y_input = file.readline().split()
            x_input = float(x_input)
            y_input = float(y_input)
        except:
            break
        x.append(x_input)
        y.append(y_input)
        
    if (x != []) and (y != []):
        bx.clear()
        bx.plot(x,y)
        chart_2.draw()
        messages.config(text='Loaded succesfully')
    else:
        messages.config(text='ERROR: Not possible to draw')
    
    file.close()
    

def saveFile():
    
    '''
    This function shows save file dialog. When file path selected, 
    function saves coordinates of showed graph 
    
    Author: Dima Buchelnikov
    '''
    
    global y, x, figure, bx
    files = [('Text Files', '*.txt'),
             ('All Files', '*.*')]
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    for i in range(len(x)):
        file.write("%f %f\n" % (x[i], y[i]))
    file.close()
    messages.config(text='Saved succesfully')


def module_dict(module):
    
    '''
    This function is neccesary for applying formula to graph coordinates
    
    Author: Vladimir Volkov
    '''
    
    return {k: getattr(module, k) for k in dir(module) if not k.startswith('_')}


def newButton():

    '''
    This function transphorms graph coordinates with desired formulas and redraws a graph
    
    Author: Vladimir Volkov
    '''
    
    global y, x, figure, bx
    messages.config(text='no messages')
    fx = fx_entry.get()
    x0 = x0_entry.get()
    x1 = x1_entry.get()
    step = step_entry.get()
    try:
        x=np.arange(float(x0), float(x1)+0.000000000000001, float(step))
    except:
        messages.config(text='ERROR: invalid input')
        return

    y = np.copy(x)
    for i, xi in enumerate(x):
        try:
            var = {'x': xi, **module_dict(math)}
            y[i] = eval(fx, var)
            messages.config(text='Drawed succesfully')
        except:
            messages.config(text='ERROR: invalid formula')
            return
    bx.clear()
    bx.plot(x,y)
    chart_2.draw()


def transformButton():
    
    '''
    This function transforms graph coordinates with desired formulas and redraws a graph
    
    Author: Vladimir Volkov
    '''
    
    global y, x, figure, bx
    messages.config(text='no messages')
    fx_transform = fx_transforn_entry.get()
    fy_transform = fy_transforn_entry.get()
    error = 0
    x_orig = np.copy(x)
    y_orig = np.copy(y)
    
    for i, xi in enumerate(x_orig):
        try:
            var = {'x': xi, **module_dict(math)}
            x[i] = eval(fx_transform, var)
        except:
            messages.config(text='ERROR: invalid formula')
            error = 1
            
    if (error == 0):    
        for i, yi in enumerate(y_orig):
            try:
                var = {'y': yi, **module_dict(math)}
                y[i] = eval(fy_transform, var)
            except:
                messages.config(text='ERROR: invalid formula')
                error = 1
                
    if (error == 0):
        bx.clear()
        bx.plot(x,y)
        chart_2.draw()


def country_graph():
    '''
    This function builds a graph of a country's population. 
    If name of the country in country_select entry was not found, error message appears
    
    Author: Arkadiy Drevalev
    '''
    
    global data, x, y
    x=[]
    y=[]
    try:
        country = country_select.get()
        cnt = 0
        y_o = data.loc[data['Country'] == country].values
        x_o = data.loc[data['Country'] == country].columns
        
        for i in range(len(x_o)-1):
            if (isinstance(x_o[i], int)) and (x_o[i] > 1000):
                x.append(x_o[i])
        
        for i in range(len(y_o[0])-1):
            if (isinstance(y_o[0][i], int)) and (y_o[0][i] > 1000):
                y.append(y_o[0][i])

        bx.clear()
        bx.plot(x,y)
        chart_2.draw()
        messages.config(text='Drawed country chart')
    except:
        messages.config(text='ERROR: country not found')
    
    

x = []
y = []
x_orig = []
y_orig = []




figure = plt.figure(figsize = (5,4), dpi = 100)
bx = figure.add_subplot(111)
chart_2 = FigureCanvasTkAgg(figure, master=tab4)
chart_2.get_tk_widget().grid(row = 1, column = 0, rowspan=8)

toolbarFrame = Frame(master=tab4)
toolbar = NavigationToolbar2Tk(chart_2, toolbarFrame)
toolbarFrame.grid(row = 9, column = 0, rowspan=1, sticky="W")

but_load = Button(tab4, text="load", padx=40, pady=10, font=('Helvatical bold', 15), command=lambda:loadFile())
but_load.grid(row=1, column=1)

but_save = Button(tab4, text="save", padx=0, pady=10, font=('Helvatical bold', 15), command=lambda:saveFile())
but_save.grid(row=1, column=2)

but_new = Button(tab4, text="new", padx=2, pady=90, font=('Helvatical bold', 15), command=lambda:newButton())
but_new.grid(row=2, column=2, rowspan=4)

but_transform = Button(tab4, text="trans\nform", padx=0, pady=17, font=('Helvatical bold', 15), command=lambda:transformButton())
but_transform.grid(row=6, column=2, rowspan=2)

fx_entry = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
fx_entry.grid(row=2, column=1)
fx_entry.insert(0, "f(x)")

x0_entry = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
x0_entry.grid(row=3, column=1)
x0_entry.insert(0, "x0")

x1_entry = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
x1_entry.grid(row=4, column=1)
x1_entry.insert(0, "x1")

step_entry = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
step_entry.grid(row=5, column=1)
step_entry.insert(0, "step")

fx_transforn_entry = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
fx_transforn_entry.grid(row=6, column=1)
fx_transforn_entry.insert(0, "x transform")

fy_transforn_entry = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
fy_transforn_entry.grid(row=7, column=1)
fy_transforn_entry.insert(0, "y transform")

country_select = Entry(tab4, width=18, borderwidth=3, font=('Helvatical bold', 10))
country_select.grid(row=8, column=1)
country_select.insert(0, "enter country")

country_select_button = Button(tab4, text="show", padx=0, pady=10, font=('Helvatical bold', 15), command=lambda:country_graph())
country_select_button.grid(row=8, column=2)

messages = Label(tab4, text="no messages", font=('Helvatical bold', 12))
messages.grid(row=9, column=1, columnspan=3)




root.mainloop()