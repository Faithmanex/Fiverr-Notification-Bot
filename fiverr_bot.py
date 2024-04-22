import customtkinter as ctk
import pyautogui
import time
import requests
import threading
import pyscreeze

class FiverrNotificationApp:
    def __init__(self):

        self.app = ctk.CTk()
        self.app.geometry("320x200")
        self.app.title("Fiverr Notification App")
        self.app.iconbitmap('fiverr_icon.ico')

        self.chat_id_label = ctk.CTkLabel(self.app, text="Chat ID:")
        self.chat_id_label.grid(row=0, column=0, padx=10, pady=10)

        self.chat_id_entry = ctk.CTkEntry(self.app, width=100)
        self.chat_id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.chat_id_entry.insert(0, "2040461515")

        self.delay_label = ctk.CTkLabel(self.app, text="Delay (seconds):")
        self.delay_label.grid(row=1, column=0, padx=10, pady=10)

        self.delay_entry = ctk.CTkEntry(self.app, width=100)
        self.delay_entry.grid(row=1, column=1, padx=10, pady=10)
        self.delay_entry.insert(0, "5")

        self.color_label = ctk.CTkLabel(self.app, text="Color (RGB):")
        self.color_label.grid(row=2, column=0, padx=10, pady=10)

        self.color_entry = ctk.CTkEntry(self.app, width=100)
        self.color_entry.grid(row=2, column=1, padx=10, pady=10)
        self.color_entry.insert(0, "193, 74, 131")

        self.start_button = ctk.CTkButton(self.app, text="Start", command=self.start_notification)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.stop_button = ctk.CTkButton(self.app, text="Stop", command=self.stop_notification)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)


        self.notification_thread = None
        self.running = False
        self.bot_token = '7138871504:AAF5YaH40GYqdLlNNqvEud-uFifvDtTHCqk' # Add bot_token as an instance variable
        self.chat_id = self.chat_id_entry.get() # Initialize chat_id from the entry widget

        self.app.protocol("WM_DELETE_WINDOW", self.on_close)
        self.app.mainloop()

    def start_notification(self):
        if not self.running: # Check if the notification loop is not already running
            self.running = True # Set the flag to true
            self.notification_thread = threading.Thread(target=self.notification_loop)
            self.notification_thread.start()
            send_telegram_message(self.bot_token, self.chat_id, "Bot Started")

    def stop_notification(self):
        if self.running: # Check if the notification loop is running
            self.running = False # Set the flag to false to stop the loop
            # Optionally, you can wait for the thread to finish if needed
            # self.notification_thread.join()
            send_telegram_message(self.bot_token, self.chat_id, "Bot Stopped")

    def on_close(self):
        """Called when the window is closed."""
        self.stop_notification()
        self.app.destroy() # This ensures the Tkinter mainloop exits

    def notification_loop(self):
        bot_token = '7138871504:AAF5YaH40GYqdLlNNqvEud-uFifvDtTHCqk'
        chat_id = self.chat_id_entry.get()
        message = 'Fiverr Notification!'
        # color = ("193, 74, 131")
        color = tuple(int(x) for x in self.color_entry.get().split(','))
        timeout = int(self.delay_entry.get())

        while self.running: # Use the flag to control the loop
            screenshot = pyautogui.screenshot()
            if find_color(screenshot, color):
                # print("Notification Sent")
                response = send_telegram_message(bot_token, chat_id, message)
                time.sleep(timeout)
            else:
                # print("Color not found")
                time.sleep(0.1)

def find_color(image, target_color):
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) == target_color:
                return True
    return False

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"    
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=params)
    return response.json()

if __name__ == "__main__":
    app = FiverrNotificationApp()
