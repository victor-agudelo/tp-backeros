# import pywhatkit
# import pyautogui
# import time

class MessageSender:
    def __init__(self, number, message, seconds=5):
        self.number = number
        self.message = message
        self.seconds = seconds

    # def send_message(self):
    #     pywhatkit.sendwhatmsg_instantly(self.number, self.message)
    #
    #     time.sleep(self.seconds)
    #
    #     pyautogui.press("enter")
    #
    #     return "Message sent"
