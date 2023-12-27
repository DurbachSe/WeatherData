import tkinter as tk
import threading
from kafka import KafkaConsumer

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
window.geometry('500x300+500+400')  # Set window size and position


#Create Tkinter text widget to display weather data
text_widget = tk.Text(window, height=10, width=80)
text_widget.pack()

# Function to update the Tkinter text widget with weather data
def update_text():
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',
        group_id='weather-consumer',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    for message in consumer:
        weather_data = message.value
        text_widget.insert(tk.END, f'{weather_data}\n')
        text_widget.see(tk.END)  # Scroll to the end
        window.update_idletasks()  # Ensure GUI updates

    consumer.close()

# Use threading to run Kafka message consumption in a separate thread
kafka_thread = threading.Thread(target=update_text)
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
