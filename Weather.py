import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        
        self.location_label = tk.Label(root, text="Enter Location (e.g., New York, US):", font='Arial 12 bold')
        self.location_label.pack()
        
        self.location_entry = tk.Entry(root)
        self.location_entry.pack()
        
        self.get_weather_button = tk.Button(root, text="Get Weather", font="Arial 10", bg='lightblue', fg='black', activebackground="teal", command=self.get_weather)
        self.get_weather_button.pack()
        
        self.weather_info_label = tk.Label(root, text="The Weather is: ", font='arial 12 bold')
        self.weather_info_label.pack()
        
        # Temperature unit radio buttons
        self.unit_var = tk.StringVar()
        self.unit_var.set("celsius")  # Default unit is Celsius
        self.celsius_radio = tk.Radiobutton(root, text="Celsius", variable=self.unit_var, value="celsius", command=self.update_weather)
        self.celsius_radio.pack()
        self.fahrenheit_radio = tk.Radiobutton(root, text="Fahrenheit", variable=self.unit_var, value="fahrenheit", command=self.update_weather)
        self.fahrenheit_radio.pack()

    def get_weather(self):
        location = self.location_entry.get()
        if not location:
            messagebox.showerror("Error", "Please enter a location.")
            return
        
        weather_data = self.fetch_weather_data(location)
        if weather_data:
            self.display_weather_info(weather_data)
        else:
            messagebox.showerror("Error", "Failed to retrieve weather data.")
    
    def fetch_weather_data(self, location):
        # API integration
        api_key = '17897df9f480864d1df767fa2d64a745'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def display_weather_info(self, weather_data):
        # Extract and display weather information
        temperature = weather_data['main']['temp']
        feels_like_temp = round(weather_data['main']['feels_like'] - 273.15)
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed'] * 3.6
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']
        timezone = weather_data['timezone']
        cloudy = weather_data['clouds']['all']
        description = weather_data['weather'][0]['description']
        
        unit = self.unit_var.get()
        temperature = self.convert_temperature(temperature, unit)
        sunrise_time = self.time_format_for_location(sunrise + timezone)
        sunset_time = self.time_format_for_location(sunset + timezone)
        info_text = f"Temperature: {temperature}\nFeels like: {feels_like_temp} °C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nWind Speed: {wind_speed} km\h\nSunrise: {sunrise_time}\nSunset: {sunset_time}\nTimezone: {timezone}\nCloudy: {cloudy}\nDescription: {description}"
        self.weather_info_label.config(text=info_text)

    def update_weather(self):
        location = self.location_entry.get()
        if not location:
            return

        weather_data = self.fetch_weather_data(location)
        if weather_data:
            self.display_weather_info(weather_data)
        #Temp conversions
    def convert_temperature(self, temperature, unit):
        if unit == "celsius":
            return f"{round(temperature - 273.15)} °C"  
        elif unit == "fahrenheit":
            return f"{round((temperature - 273.15) * 9/5 + 32)} °F"  
        else:
            return f"{temperature} K"

    @staticmethod
    def time_format_for_location(utc_with_tz):
        local_time = datetime.utcfromtimestamp(utc_with_tz)
        return local_time.strftime('%H:%M')  


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
