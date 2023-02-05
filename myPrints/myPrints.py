from termcolor import colored
import os
import time


def color_txt(s, color=None, highlight=None, attrs=None):
    '''
    Function to color text using termcolor module.

    Returns: (str) String of styled text.

    Parameters:
        s (str): text.

        color (str): color of text
            options: white (default), red, green, blue, yellow, magenta, cyan, grey.

        highlight (str): highlight color of text, default - None.
            options: red, green, blue, yellow, magenta, cyan, white, grey.

        attrs (list of str): styles to be applied to text.
            options: bold, underline, dark, reverse, concealed, blink.

        Example: 
            colored('Hello, World!', 'red', 'blue', ['bold', 'blink'])
    '''

    # lists and dicts for checking parameters
    colors = ['white', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
    highlights = {
        None: None,  # default
        'red': 'on_red',
        'green': 'on_green',
        'blue': 'on_blue',
        'yellow': 'on_yellow',
        'magenta': 'on_magenta',
        'cyan': 'on_cyan',
        'grey': 'on_grey'  # doesn't highlight, just changes color of text.
    }
    attributes = ['bold', 'dark', 'underline', 'blink', 'reverse', 'concealed']

    if color:
        if type(color) is not str:
            print(f'The parameter "color" needs to be a string.\n')
            print("Fix before conituning.\n")
            exit(True)
        elif color not in colors:
            print(f'Text color "{color}" is not option.\n')
            txt = f'Available colors: ' + ', '.join(colors)
            print(txt)
            exit(True)

    if highlight:
        if type(highlight) is not str:
            print(f'The parameter "highlight" needs to be a string.\n')
            print("Fix before conituning.\n")
            exit(True)
        elif highlight not in highlights:
            print(f'Highlight color "{highlight}" is not option.\n')
            txt = 'Available highlights: ' + \
                ', '.join([hl for hl in highlights.keys() if hl])
            print(txt)
            exit(True)

    if attrs:
        if type(attrs) is not list:
            print(f'The parameter attribute "{attrs}" needs to be a list.\n')
            print("Fix before continuing\n")
            exit(True)
        else:
            for attr in attrs:
                if attr not in attributes:
                    print(f'Attribute "{attr}" is not option.\n')
                    txt = f'Available options: ' + ', '.join(attributes)
                    print(txt)
                    exit(True)

    t = colored(text=s, color=color,
                on_color=highlights[highlight], attrs=attrs)
    return t


def print_color(s, color=None, highlight=None, attrs=None, **kwargs):
    '''
    Function to print color text using the color_txt function.

    Parameters:
        s (str): text.

        color (str): color of text
            options: white (default), red, green, blue, yellow, magenta, cyan, grey.

        highlight (str): highlight color of text, default - None.
            options: red, green, blue, yellow, magenta, cyan, white, grey.

        attrs (list of str): styles to be applied to text.
            options: bold, underline, dark, reverse, concealed, blink.

        **kwargs: kwargs for print function.

        Example: 
            print_color('Hello, World!', 'red', 'blue', ['bold', 'blink'])
    '''
    t = color_txt(s=s, color=color, highlight=highlight, attrs=attrs)
    print(t, **kwargs)


def warning(color='red', highlight='yellow'):
    '''
    Function to print a color warning banner.

    Initially designed for debugging.
    '''
    print_color("*** Warning ***", color=color, highlight=highlight)


def scroll_str(s, newline=True, delay=25):
    '''
    Function to print a string char by char. (Simulates scrolling)

    Parameters:
        s (str): string to print.
        newline (bool - optional): after the last character make a newline.
        delay (float - optional): time delay between each character in milliseconds.
    '''
    if newline:
        for i, char in enumerate(s):
            if not i+1 == len(s):
                print(char, end='', flush=True)
            else:
                print(char)
            time.sleep(delay/1000)
    else:
        for i, char in enumerate(s):
            if not i+1 == len(s):
                print(char, end='', flush=True)
            else:
                print(char, end=' ')
            time.sleep(delay/1000)


def clear_screen():
    '''
    Function to clear the terminal screen.
    '''
    os.system('clear')


def quit_program(check=False, delay=0):
    '''
    Function to terminate program.

    Parameter:
        check, optional (bool) [default False]: double check if user really wants to quit the program.
        delay, opional (float) [default 0]: delay time to simulate a shut down sequence. 
    '''
    user = input('Exit program? (y/n): ')
    if user == 'y':
        if check:
            user = input("Are you sure? (y/n): ")
            if user == 'y':
                print("\nProgram Closing...")
                time.sleep(delay)
                exit(True)
        else:
            print("\nProgram Closing...")
            time.sleep(delay)
            exit(True)
    else:
        return False


func_list = [
    color_txt,
    print_color,
    warning,
    scroll_str,
    clear_screen,
    quit_program
]