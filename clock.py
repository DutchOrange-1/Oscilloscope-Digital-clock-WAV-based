import pygame
import time
import datetime
import os


st = datetime.datetime.now().minute


def update_time():
    global c_hour, c_minute
    c_hour = str(datetime.datetime.now().hour)
    if len(c_hour) == 1:
        c_hour = "0" + c_hour
    c_minute = str(datetime.datetime.now().minute)
    if len(c_minute) == 1:
        c_minute = "0" + c_minute

    print(f"Hour: {c_hour}, Minute: {c_minute}")


def loop_audio_pygame(file_path):
    global st
    # Initialize the mixer
    pygame.mixer.init()

    # Load the sound file
    try:
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(0.7)  # Adjust the volume as needed
    except pygame.error as e:
        print(f"Cannot load file: {e}")
        return

    print(f"Playing '{os.path.basename(file_path)}' in a loop...")

    # Play the sound indefinitely (loops=-1)
    sound.play(loops=-1)

    # Keep the program running so the music continues to play
    # You can add other program logic here
    try:
        while True:
            time.sleep(1)
            print("Running")
            curr = datetime.datetime.now().minute
            if curr != st:
                print("Stopping playback - next time stamp")
                sound.stop()
                st = curr
                break

    except KeyboardInterrupt:
        # Stop the sound and quit pygame gracefully when the user presses Ctrl+C
        print("Stopping playback.")
        sound.stop()
        pygame.mixer.quit()
        exit()


c_hour = str(datetime.datetime.now().hour)
if len(c_hour) == 1:
    c_hour = "0" + c_hour
c_minute = str(datetime.datetime.now().minute)
if len(c_minute) == 1:
    c_minute = "0" + c_minute


try:
    while True:
        loop_audio_pygame("./time_files/t_"+c_hour+"_"+c_minute+".wav")
        update_time()

except KeyboardInterrupt:
    exit()


# loop_audio_pygame("./Music/t_15_10.wav")
# loop_audio_pygame("./Music/t_15_47.wav")
