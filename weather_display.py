import tkinter as tk
import threading
import json
import time
import re
from kafka import KafkaConsumer, TopicPartition
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime

kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'weather-data'

# Create Kafka consumer
consumer = KafkaConsumer(
    #kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    #auto_offset_reset='earliest',
    #group_id='weather-consumer',
    value_deserializer=lambda x: x.decode('utf-8')
)

subscribe_from_beginning = True

# Manually assign partitions for your specific topic
partitions = [TopicPartition(kafka_topic, partition) for partition in range(3)]  # Adjust the range accordingly
consumer.assign(partitions)

# Reset the offset to the beginning for each assigned partition
if subscribe_from_beginning:
    for partition in partitions:
        consumer.seek_to_beginning(partition)

# Create Tkinter window
window = tk.Tk()
window.title('Weather Data Consumer')
window.geometry('800x600')  # Set window size

# Create Figure for the Matplotlib graph
fig = Figure(figsize=(6, 5), dpi=100)
fig.subplots_adjust(bottom=0.3)  # Adjust the bottom margin to leave more space
ax = fig.add_subplot(111)
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')

# Create a secondary y-axis for humidity
ax2 = ax.twinx()
ax2.set_ylabel('Humidity (%)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Create Tkinter canvas for embedding the Matplotlib graph
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Initialize empty lists for data
time_data = []
temperature_data = []
humidity_data = []

# Set minimum ranges for axes
min_temperature_range = 5.0
min_humidity_range = 10.0
data_offset = 1
max_timestamps = 8

# Create Tkinter text widget to display weather data
text_widget = tk.Text(window, height=10, width=120)
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
            datetime_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', message_text)
            temperature_match = re.search(r'Temperature: ([-+]?\d*\.\d+|\d+)', message_text)
            humidity_match = re.search(r'Humidity: ([-+]?\d*\.\d+|\d+)', message_text)
            description_match = re.search(r'Description: (.+)', message_text)

            # Convert temperature and humidity to numbers, set to 'N/A' if not valid
            current_datetime = datetime_match.group(1) if datetime_match else 'N/A'
            temperature = float(temperature_match.group(1)) if temperature_match else 'N/A'
            humidity = float(humidity_match.group(1)) if humidity_match else 'N/A'
            description = description_match.group(1) if description_match else 'N/A'

            print(f'Received: Time={current_datetime}, Temperature={temperature}, Humidity={humidity}, Description={description}')

            # Append data to lists
            time_data.append(current_datetime)
            temperature_data.append(temperature)
            humidity_data.append(humidity)

            # Update the Matplotlib graph with separate y-axes
            ax.clear()

            # Set minimum range for temperature axis
            temperature_data_range = max(temperature_data) - min(temperature_data)
            temperature_axis_min = min(temperature_data) - max(0, min_temperature_range - temperature_data_range / 2)+data_offset
            temperature_axis_max = max(temperature_data) + max(0, min_temperature_range - temperature_data_range / 2)+data_offset
            ax.set_ylim(temperature_axis_min, temperature_axis_max)
            ax.plot(time_data, temperature_data, label='Temperature (°C)', color='blue')

            # Set minimum range for humidity axis
            humidity_data_range = max(humidity_data) - min(humidity_data)
            humidity_axis_min = min(humidity_data) - max(0, min_humidity_range - humidity_data_range / 2)-data_offset
            humidity_axis_max = max(humidity_data) + max(0, min_humidity_range - humidity_data_range / 2)-data_offset
            ax2.set_ylim(humidity_axis_min, humidity_axis_max)
            ax2.plot(time_data, humidity_data, label='Humidity (%)', color='green')

            ax.set_xlabel('Time')
            ax.set_ylabel('Temperature (°C)', color='blue')
            #ax.legend(loc='upper left')

            # Set x-axis ticks to display every n-th timestamp
            n = max(1, len(time_data) // max_timestamps)  # Avoid division by zero
            ax.set_xticks(time_data[::n])
            ax.set_xticklabels(time_data[::n], rotation=45, ha='right')  # Adjust rotation and alignment as needed

            # Redraw the canvas
            canvas.draw()

            # Update the Tkinter text widget
            text_widget.insert(tk.END, f'Time: {current_time}, Temperature: {temperature}°C, Humidity: {humidity}%, Description: {description}\n')
            text_widget.see(tk.END)  # Scroll to the end

        except Exception as e:
            print(f"Error processing message: {e}, Raw message: {message.value}")

# Use threading to run Kafka message consumption in a separate thread
kafka_thread = threading.Thread(target=update_display)
kafka_thread.start()

# Use Tkinter after method to periodically update the text widget
def periodic_update():
    window.after(1000, periodic_update)  # Update every 1000 milliseconds (1 second)

# Start periodic updates
periodic_update()

# Run the Tkinter event loop
window.mainloop()

# Close the Kafka consumer when the Tkinter window is closed
consumer.close()
