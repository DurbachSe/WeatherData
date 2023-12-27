import tkinter as tk
import threading
import json
import time
import re
from kafka import KafkaConsumer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'weather-data'

#Create Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    auto_offset_reset='earliest',
    group_id='weather-consumer',
    value_deserializer=lambda x: x.decode('utf-8')
)

#Create Tkinter window
window = tk.Tk()
window.title('Weather Data Consumer')
window.geometry('500x500+500+400')  # Set window size and position

# Create Figure for the Matplotlib graph
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlabel('Time')
ax.set_ylabel('Value')

# Create Tkinter canvas for embedding the Matplotlib graph
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Initialize empty lists for data
time_data = []
temperature_data = []
humidity_data = []

#Create Tkinter text widget to display weather data
text_widget = tk.Text(window, height=10, width=80)
text_widget.pack()

# Function to update the Matplotlib graph and text widget with weather data
def update_display():
    for message in consumer:
        try:
            # Treat the message as plain text
            message_text = str(message.value)

            # Extract data from the received text
            current_time = time.strftime("%H:%M:%S")

            # Extract numerical values using regular expressions
            temperature_match = re.search(r'Temperature: ([-+]?\d*\.\d+|\d+)', message_text)
            humidity_match = re.search(r'Humidity: ([-+]?\d*\.\d+|\d+)', message_text)

            # Convert temperature and humidity to numbers, set to 'N/A' if not valid
            temperature = float(temperature_match.group(1)) if temperature_match else 'N/A'
            humidity = float(humidity_match.group(1)) if humidity_match else 'N/A'

            print(f'Received: Time={current_time}, Temperature={temperature}, Humidity={humidity}')

            # Append data to lists
            time_data.append(current_time)
            temperature_data.append(temperature)
            humidity_data.append(humidity)

            # Update the Matplotlib graph with separate y-axes
            ax.clear()
            ax.plot(time_data, temperature_data, label='Temperature (°C)', color='blue')
            
            # Create a secondary y-axis for humidity
            ax2 = ax.twinx()
            ax2.plot(time_data, humidity_data, label='Humidity (%)', color='green')
            ax2.set_ylabel('Humidity (%)', color='green')
            ax2.tick_params(axis='y', labelcolor='green')
            
            ax.set_xlabel('Time')
            ax.set_ylabel('Temperature (°C)', color='blue')
            ax.legend(loc='upper left')
            
            # Redraw the canvas
            canvas.draw()

            # Update the Tkinter text widget
            text_widget.insert(tk.END, f'Time: {current_time}, Temperature: {temperature}°C, Humidity: {humidity}%\n')
            text_widget.see(tk.END)  # Scroll to the end

        except Exception as e:
            print(f"Error processing message: {e}, Raw message: {message.value}")
            
# Use threading to run Kafka message consumption in a separate thread
kafka_thread = threading.Thread(target=update_display)
kafka_thread.start()

#Use Tkinter after method to periodically update the text widget
def periodic_update():
    window.after(1000, periodic_update)  # Update every 1000 milliseconds (1 second)

#Start periodic updates
periodic_update()

#Run the Tkinter event loop
window.mainloop()

# Close the Kafka consumer when the Tkinter window is closed
consumer.close()
