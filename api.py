from tkinter import *
from tkinter import ttk
from tkinter import font
import requests
from urllib.request import urlopen
from datetime import datetime
from PIL import ImageTk
from PIL import Image
from io import BytesIO
from urllib import error

icon = None
key = "021ede9be42baea3619cf33054447972"
example_page = "city"
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title("Weather conditions - Forecast_API")
root.geometry(f"{screen_width}x{screen_height}")

background = Label(root, bg="#0049AF")
background.grid(row=0, column=0)
background.grid_columnconfigure(0, minsize=screen_width)
background.grid_rowconfigure(0, minsize=screen_height)

container = Label(background)
container.grid(row=0, column=0, columnspan=4, rowspan=4, sticky=N)
container.grid_columnconfigure(0, minsize=600)

def clear_example_page():
    global example_page
    if v.get() == example_page:
        example_page = ''
        v.set('')

def get_url():
    city = entry_address.get()
    url = f'http://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric'
    return url, city

def validate_url(url, city):
    json_data = requests.get(url).json()
    try:
        json_data["message"]
        msg = json_data["message"]
        display_message(msg, "#ff0000")
        clear_table()
    except:
        msg = f'Forecast in {city}.'
        display_message(msg, "#00cd00")
        return json_data

def get_data():
    url, city = get_url()
    json_data = validate_url(url, city)
    if json_data:
        display_data(json_data)

def display_message(msg, color):
    app_message.config(text=msg, bg=color)

def get_icon(json_data):
    global icon
    icon_id = json_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    icon_byt = urlopen(icon_url).read()
    icon = PhotoImage(data=icon_byt)

def display_data(json_data):
    get_icon(json_data)
    timestamp = json_data["dt"]
    dt_object = datetime.fromtimestamp(timestamp)
    table_date.config(text=f"day\n{dt_object.date()}")
    table_time.config(text=f'last update\n{dt_object.time()}')

    to_display = f'description: {json_data["weather"][0]["description"]}\n' \
                 f'main: {json_data["weather"][0]["main"]}\n' \
                 f'temperature: {round(json_data["main"]["temp"])} C\n' \
                 f'temperature min.: {round(json_data["main"]["temp_min"])} C\n' \
                 f'temperature max.: {round(json_data["main"]["temp_max"])} C\n' \
                 f'pressure: {json_data["main"]["pressure"]} hPa\n' \
                 f'wind: {json_data["wind"]["speed"]} meter/sec\n' \
                 f'humidity: {json_data["main"]["humidity"]} %\n'
    table_data.config(text=to_display)
    table_icon.config(image=icon)

def clear_table():
    table_date.config(text="")
    table_time.config(text="")
    table_icon.config(image="", text="")
    table_data.config(text="")

''' START Form'''
ask_font_style = font.Font(family="Helvetica", size=16)
ask_about_city = Label(container, text="Entry city", fg="#ffffff", bg="#0080ff", padx=15, font=ask_font_style)
ask_about_city.grid(row=0, column=0, columnspan=4, sticky=EW)

v = StringVar()
v.set(example_page)
entry_address = Entry(container, textvariable=v)
entry_address.grid(row=1, column=0, columnspan=2, sticky=EW)
entry_address.bind('<1>', lambda _: clear_example_page())
entry_address.bind('<Return>', lambda _: get_data())

style = ttk.Style()
style.configure('TButton', background="#0059b3", foreground="#f2f2f2")
style.map('TButton', foreground=[("active", "#ffffff")], background=[("active", "#004080")])
btn_address_ok = ttk.Button(container, text='check', style="TButton", command=get_data)
btn_address_ok.grid(row=1, column=2, sticky=W)

app_message_font_style = font.Font(family="Helvetica", size=14)
app_message = Label(container, bg="#00ffff", font=app_message_font_style)
app_message.grid(row=2, column=0, columnspan=3, sticky=EW)
''' END Form'''

'''START Table with forecast'''
table = Frame(container, bg="#0080ff")
table.grid(row=3, column=0, rowspan=3, columnspan=4, sticky=EW)

date_font_style = font.Font(family="Helvetica", size=14)
table_date = Label(table, wraplength=220, justify=CENTER, padx=30, bg="#0080ff", font=date_font_style, fg="#fff", width=15)
table_date.grid(row=3, column=0, sticky=EW)
time_font_style = font.Font(family="Helvetica", size=14)
table_time = Label(table, wraplength=220, justify=CENTER, padx=30, bg="#0080ff", font=time_font_style, fg="#fff")
table_time.grid(row=4, column=0, sticky=N)

data_font_style = font.Font(family="Helvetica", size=14)
table_data = Label(table, wraplength=320, anchor="w", justify=LEFT, padx=0, bg="#0080ff",
                   font=data_font_style, fg="#fff", width=30)
table_data.grid(row=3, column=1, columnspan=2, rowspan=2, sticky=W)

table_icon = Label(table, padx=20, pady=20, bg="#0080ff")
table_icon.grid(row=3, column=3, rowspan=2, sticky=E)

'''END Table forecast'''

'''START Background '''

img_url = "https://www.larutadelsorigens.cat/wallpic/full/73-737784_20-blue-gradient-background-blue-simple-background-hd.jpg"

try:
    img_data = urlopen(img_url).read()
    image_byt = Image.open(BytesIO(img_data))
    img = ImageTk.PhotoImage(image=image_byt)
    background.config(image=img)
except error.HTTPError:
    print("Incorrect url to background")
except error.URLError:
    print("Brak połaczenia")
'''END Background'''


root.mainloop()
