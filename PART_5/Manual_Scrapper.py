import pyautogui
import time
from pynput import mouse, keyboard
import threading

urls = {
    r"efreipicturestudio.fr/gallery/weixico-2023--jour2-2023": 669,
    r"efreipicturestudio.fr/gallery/weisabi-2022---jour2-2022": 871,
    r"efreipicturestudio.fr/gallery/weixico-2023--jour3-2023": 995,
}

# Initial time delay
time_delay = 0.7

# Function to adjust time delay
def on_press(key):
    global time_delay
    try:
        if key == keyboard.Key.up:
            time_delay -= 0.01
            if time_delay < 0:
                time_delay = 0
            print(f"Time delay adjusted to: {time_delay:.2f} seconds")
        elif key == keyboard.Key.down:
            time_delay += 0.01
            print(f"Time delay adjusted to: {time_delay:.2f} seconds")
    except AttributeError:
        pass

def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

# Function to save pictures
def save_pictures(number_of_pictures):
    global time_delay
    for i in range(number_of_pictures):
        pyautogui.moveTo(1056, 775)
        pyautogui.click(button='right')
        time.sleep(time_delay)
        pyautogui.moveTo(1056, 870)
        pyautogui.click(button='right')
        time.sleep(time_delay)
        pyautogui.press('enter')
        time.sleep(time_delay)
        pyautogui.press('right')
        time.sleep(time_delay)

def automate():
    global time_delay
    time.sleep(3)  # Initial delay to prepare the screen
    for url, number in urls.items():
        pyautogui.moveTo(1064, 103)
        pyautogui.click()
        
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(3)
        pyautogui.press('delete')
        
        time.sleep(3)
        pyautogui.write(url, interval=0.05)
        pyautogui.press('enter')
        time.sleep(3)
        
        pyautogui.moveTo(598, 805)
        time.sleep(3)
        pyautogui.click(button='left')
        time.sleep(3)
        
        save_pictures(number)
        
        time.sleep(2)

# Main execution
if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True
    listener_thread.start()
    automate()

