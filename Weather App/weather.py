import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io

# Replace with your OpenWeatherMap API Key
API_KEY = "08f269b02892d617e2eff9bb0ed4f23b"
0
# Colors and Fonts
BG_COLOR = "#E3F2FD"
BTN_COLOR = "#90CAF9"
HOVER_COLOR = "#64B5F6"
TEXT_COLOR = "#0D47A1"
FONT_LARGE = ("Helvetica", 18, "bold")
FONT_MEDIUM = ("Helvetica", 13)
FONT_SMALL = ("Helvetica", 10)

# Get weather data
def get_weather(city, unit="metric"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            raise Exception(data.get("message"))
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve weather: {e}")
        return None

# Update GUI with weather info
def update_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Required", "Please enter a city name.")
        return

    unit = "metric" if unit_var.get() == "Celsius" else "imperial"
    data = get_weather(city, unit)

    if data:
        temp = data['main']['temp']
        condition = data['weather'][0]['description'].title()
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        icon_id = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"

        weather_info.set(f"{temp}°{unit[0]} | {condition}")
        humidity_info.set(f"Humidity: {humidity}%")
        wind_info.set(f"Wind: {wind} {'m/s' if unit == 'metric' else 'mph'}")

        # Load and display weather icon
        icon_img = Image.open(io.BytesIO(requests.get(icon_url).content))
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

# Button hover effects
def on_enter(e): e.widget.config(bg=HOVER_COLOR)
def on_leave(e): e.widget.config(bg=BTN_COLOR)

# ---- GUI Setup ---- #
root = tk.Tk()
root.title("🌦️ Weather App")
root.geometry("400x500")
root.config(bg=BG_COLOR)
root.resizable(False, False)

# Header
tk.Label(root, text="Weather Forecast", font=FONT_LARGE, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

# Input Frame
input_frame = tk.Frame(root, bg=BG_COLOR)
input_frame.pack(pady=10)

city_entry = tk.Entry(input_frame, font=FONT_MEDIUM, width=20, justify='center')
city_entry.pack(side='left', padx=10)

unit_var = tk.StringVar(value="Celsius")
unit_menu = ttk.Combobox(input_frame, textvariable=unit_var, values=["Celsius", "Fahrenheit"], width=10, state="readonly")
unit_menu.pack(side='left')

# Search Button
search_btn = tk.Button(root, text="🔍 Search", font=FONT_MEDIUM, bg=BTN_COLOR, relief="flat", command=update_weather)
search_btn.pack(pady=10)
search_btn.bind("<Enter>", on_enter)
search_btn.bind("<Leave>", on_leave)

# Weather Display
icon_label = tk.Label(root, bg=BG_COLOR)
icon_label.pack(pady=10)

weather_info = tk.StringVar()
tk.Label(root, textvariable=weather_info, font=("Helvetica", 14), bg=BG_COLOR, fg=TEXT_COLOR).pack()

humidity_info = tk.StringVar()
tk.Label(root, textvariable=humidity_info, font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()

wind_info = tk.StringVar()
tk.Label(root, textvariable=wind_info, font=FONT_SMALL, bg=BG_COLOR, fg=TEXT_COLOR).pack()

# Footer
tk.Label(root, text="Made with ❤️by Hiten", font=FONT_SMALL, bg=BG_COLOR, fg="#1565C0").pack(side='bottom', pady=15)

root.mainloop()
