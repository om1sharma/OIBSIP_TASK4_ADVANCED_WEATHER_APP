import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import pycountry 

# Initialize main window
root = tk.Tk()
root.title("Detailed Weather App")
root.geometry("520x700")
root.configure(bg="#E9F7FC")

tk.Label(root, text="🌤️ Weather Info Finder", font=("Arial", 18, "bold"), bg="#E9F7FC", fg="#333").pack(pady=20)

# Function to create labeled entries
def create_labeled_entry(text):
    frame = tk.Frame(root, bg="#E9F7FC")
    tk.Label(frame, text=text, font=("Arial", 11, "bold"), bg="#E9F7FC").pack(side=tk.LEFT)
    e = tk.Entry(frame, font=("Arial", 11), width=30)
    e.pack(side=tk.LEFT, padx=10)
    frame.pack(pady=8)
    return e

# Input fields
country_entry = create_labeled_entry("Country Name:")
state_entry = create_labeled_entry("State:")
city_entry = create_labeled_entry("City:")
locality_entry = create_labeled_entry("Locality (optional):")
pincode_entry = create_labeled_entry("Pin Code (optional):")

# Temperature unit selector
unit_var = tk.StringVar(value="metric")
unit_frame = tk.Frame(root, bg="#E9F7FC")
tk.Label(unit_frame, text="Temperature Unit:", font=("Arial", 11, "bold"), bg="#E9F7FC").pack(side=tk.LEFT)
for txt, val in [("Celsius", "metric"), ("Fahrenheit", "imperial")]:
    tk.Radiobutton(unit_frame, text=txt, variable=unit_var, value=val, bg="#E9F7FC").pack(side=tk.LEFT, padx=10 if val=="metric" else 0)
unit_frame.pack(pady=10)

# Result box
result_box = tk.Text(root, height=12, width=60, font=("Arial", 11), bd=1, relief=tk.SOLID, wrap=tk.WORD)
result_box.pack(pady=10)

# ✅ API Key (defined separately)
API_KEY = "140d8230fe1a9e9a701099695b677884"

# Weather function
def get_weather():
    ctry = country_entry.get().strip()
    st = state_entry.get().strip()
    ct = city_entry.get().strip()
    loc = locality_entry.get().strip()
    pin = pincode_entry.get().strip()

    if not ctry and not pin:
        messagebox.showerror("Input Missing", "Please enter either a Pin Code or a Country name.")
        return
    if pin:
        location = f"{pin},{ctry}" if ctry else pin
    else:
        if not ct or not st:
            messagebox.showerror("Input Missing", "Please enter City and State when Pin Code is not provided.")
            return
        location = f"{ct},{st},{ctry}"

    # ✅ Use API_KEY in the request URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units={unit_var.get()}"

    try:
        data = requests.get(url, timeout=10).json()
    except requests.RequestException as e:
        messagebox.showerror("Network Error", f"Error fetching data:\n{e}")
        return

    if str(data.get("cod")) != "200":
        messagebox.showerror("Error", f"Location not found: {location}")
        return

    weather = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    unit_symbol = "°C" if unit_var.get() == "metric" else "°F"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if pin and not (ct or st):
        country_code = data['sys'].get('country')
        try:
            country_full = pycountry.countries.get(alpha_2=country_code).name
        except:
            country_full = country_code
        loc_name = f"{data.get('name')}, {country_full}"

        result = (
            f"📍 Address: {loc_name}\n"
            f"🕒 Date & Time: {now}\n\n"
            f"🌡️ Temperature: {temp}{unit_symbol}\n"
            f"☁️ Weather: {weather}\n"
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind Speed: {wind} m/s"
        )
    else:
        loc_name = f"{data.get('name')}, {data['sys'].get('country')}"
        result = (
            f"📍 Location: {loc_name}\n"
            f"🗺️ State: {st}\n"
            f"🏙️ City: {ct}\n"
            f"📌 Locality: {loc if loc else 'N/A'}\n"
            f"🕒 Date & Time: {now}\n\n"
            f"🌡️ Temperature: {temp}{unit_symbol}\n"
            f"☁️ Weather: {weather}\n"
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind Speed: {wind} m/s"
        )

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result)

    for k in ["🌡️", "☁️", "💧", "💨"]:
        idx = result_box.search(k, "1.0", tk.END)
        if idx:
            result_box.tag_add("highlight", idx, f"{idx.split('.')[0]}.end")
    result_box.tag_config("highlight", font=("Arial", 12, "bold"), foreground="blue")

# Clear function
def clear_all():
    for entry in [country_entry, state_entry, city_entry, locality_entry, pincode_entry]:
        entry.delete(0, tk.END)
    result_box.delete("1.0", tk.END)

# Buttons
btn_frame = tk.Frame(root, bg="#E9F7FC")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🔍 Get Weather", font=("Arial", 12, "bold"), bg="#2E8B57", fg="white",
          padx=20, pady=8, bd=0, relief=tk.RAISED,
          activebackground="#276749", activeforeground="white",
          command=get_weather).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="❌ Clear", font=("Arial", 12, "bold"), bg="#B22222", fg="white",
          padx=20, pady=8, bd=0, relief=tk.RAISED,
          activebackground="#8B1A1A", activeforeground="white",
          command=clear_all).pack(side=tk.LEFT, padx=10)

# Run the application
root.mainloop()
