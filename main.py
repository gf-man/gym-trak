import curses
import math
import datetime
from enum import Enum


Exercise_Type = Enum("Exercise_Type", ["Resistance", "Bodyweight", "Isometric", "Distance"])

MAX_EX_NAME_LENGTH = 20

exercise_list = []
date_list = []


def get_date():
    today = datetime.date.today()
    return today.strftime("%d/%m/%Y")

class Exercise:
    def __init__(self, name, category):
        self.name = name
        self.category = Exercise_Type(category)
        self.record = {}

    def add_record(self, record):
        self.record.update(record)

def load_records():
    file = open("gym.md", "r")
    records_started = False
    rec_date = "01/01/2000"
    for line in file:
        line = line.rstrip('\n')
        try:
            datetime.datetime.strptime(line,"%d/%m/%Y")
            rec_date = line
            records_started = True
        except ValueError:
            if line == "":
                pass
            elif line[0] == "-" and records_started:
                ex_data = line[2:].split(':')
                ex_name = ex_data[0]
                ex_rec = ex_data[1].split('>')
                ex_rec_ind = ex_rec[0].split('x') # ONLY THE FIRST RECORD
                if ex_rec_ind[0][-2:] == "kg":
                    # Resistance
                    ex_cat = 1
                elif ex_rec_ind[0][-1:] == "s":
                    # Isometric
                    ex_cat = 3
                elif ex_rec_ind[1][-2:] == "km":
                    # Distance
                    ex_cat = 4
                else:
                    # Bodyweight
                    ex_cat = 2

                if ex_name not in [ex.name for ex in exercise_list]:
                    exercise_list.append(Exercise(ex_name, ex_cat))

                ex_recs = []
                for rec in ex_rec:
                    ex_recs.append(rec.split('x'))

                for ex in exercise_list:
                    if ex.name == ex_name:
                        ex.add_record({rec_date: ex_recs})
                if rec_date not in date_list:
                    date_list.append(rec_date)

    file.close()

def save_records():
    file = open("gym.md", "w")
    file.write("# Gym Tracker\n\n## Format\nDD/MM/YYYY\n- resistance:WEIGHTkgxREPSxSETS:notes\n- bodyweight:REPSxSETS:notes\n- isometric:TIMEsxSETS:notes\n- distance:TIMEmxDISTANCEkm:notes\n\n\n## Dates\n")
    for rec_date in date_list:
        file.write(rec_date + "\n")
        for ex in exercise_list:
            if rec_date in ex.record:
                output_line = "- " + ex.name + ":"
                for rec_number in range(len(ex.record[rec_date])):
                    output_line += "x".join(ex.record[rec_date][rec_number])
                    if rec_number != max(range(len(ex.record[rec_date]))):
                        output_line += ">"
                output_line += "\n"
                file.write(output_line)
        file.write("\n")
    file.close()

def input_exercise():
    #print("Add a new Exercise")
    name = get_input("Exercise name: ", MAX_EX_NAME_LENGTH, "s")
    if name == False:
        return
    #print("What type of Exercise? ")
    category = int(get_input("1: Resistance, 2: Bodyweight, 3: Isometric, 4: Distance: ", 1, "i"))
    exercise_list.append(Exercise(name, category))
    clear_message()

def generate_exercise_dict():
    ex_dict = {}
    counter = 1
    for ex in exercise_list:
        if ex.name[0] not in ex_dict:
            ex_dict.update({ex.name[0].upper(): ex.name})
        else:
            ex_dict.update({str(counter): ex.name})
            counter += 1
    return ex_dict


def input_record(ex_name):
    #print("Add a Record")

    for ex in exercise_list:
        if ex_name == ex.name:
            if get_date() in ex.record:
                record = ex.record[get_date()]
            else:
                record = []

            if ex.category == Exercise_Type["Resistance"]:
                while True:
                    weight = get_input("Weight(kilograms): ", 4, "f")
                    if weight is False:
                        clear_message()
                        return
                    reps = get_input("Reps: ", 2, "i")
                    if reps is False:
                        clear_message()
                        return
                    sets = get_input("Sets: ", 2, "i")
                    if sets is False:
                        clear_message()
                        return
                    record.append([weight + "kg", reps, sets])
                    if not yn_prompt("Add more sets? (y/n)"):
                        #if yn_prompt("Add notes? (y/n)")
                        #    notes = get_input("Notes: ", 64)
                        break

            elif ex.category == Exercise_Type["Bodyweight"]:
                while True:
                    reps = get_input("Reps: ", 2, "i")
                    if reps is False:
                        clear_message()
                        return
                    sets = get_input("Sets: ", 2, "i")
                    if sets is False:
                        clear_message()
                        return
                    record.append([reps, sets])
                    if not yn_prompt("Add more sets? (y/n)"):
                        #if yn_prompt("Add notes? (y/n)")
                        #    notes = get_input("Notes: ", 64)
                        break

            elif ex.category == Exercise_Type["Isometric"]:
                while True:
                    time = get_input("Time(seconds): ", 3, "i")
                    if time is False:
                        clear_message()
                        return
                    reps = get_input("Sets: ", 2, "i")
                    if reps is False:
                        clear_message()
                        return
                    record.append([time + "s", reps])
                    if not yn_prompt("Add more sets? (y/n)"):
                        #if yn_prompt("Add notes? (y/n)")
                        #    notes = get_input("Notes: ", 64)
                        break

            elif ex.category == Exercise_Type["Distance"]:
                while True:
                    time = get_input("Time(minutes): ", 3, "f")
                    if time is False:
                        clear_message()
                        return
                    dist = get_input("Distance(kilometers): ", 3, "f")
                    if dist is False:
                        clear_message()
                        return
                    record.append([time + "m", dist + "km"])
                    if not yn_prompt("Add more sets? (y/n)"):
                        #if yn_prompt("Add notes? (y/n)")
                        #    notes = get_input("Notes: ", 64)
                        break

            ex.add_record({get_date(): record})

            if get_date() not in date_list:
                date_list.append(get_date())
            break

def view_todays_records():
    todays_records_list = []
    for ex in exercise_list:
        if get_date() in ex.record:
            todays_records_list.append(ex.name + ": " + "x".join(ex.record[get_date()][0]))
            for record in ex.record[get_date()][1:]:
                todays_records_list.append(" " * len(ex.name + ": ") + "x".join(record))
    return todays_records_list

def view_exercise_records(ex_name):
    ex_records_list = []
    for ex in exercise_list:
         if ex_name == ex.name:
            ex_records_list.append(ex_name)
            for rec_date in ex.record:
                ex_records_list.append(rec_date + ": " + "x".join(ex.record[rec_date][0]))
                for record in ex.record[rec_date][1:]:
                    ex_records_list.append(" " * len(rec_date + ": ") + "x".join(record))
    return ex_records_list

def view_all_records():
    all_records_list = []
    for rec_date in date_list:
        all_records_list.append(rec_date)
        for ex in exercise_list:
            if rec_date in ex.record:
                all_records_list.append(str(ex.name + ": " + "x".join(ex.record[rec_date][0])))
                for record in ex.record[rec_date][1:]:
                    all_records_list.append(" " * len(ex.name + ": ") + "x".join(record))
        all_records_list.append("")
    return all_records_list



def start_curses():
    curses.noecho()
    curses.cbreak()
    curses.curs_set(2)
    if curses.has_colors():
        curses.start_color()
    stdscr.keypad(True)

def end_curses():
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    stdscr.keypad(False)
    curses.endwin()

def show_message(message):
    clear_message()
    stdscr.addstr(curses.LINES - 1, 1, message)

def clear_message():
    stdscr.addstr(curses.LINES -1, 1, str(" " * (curses.COLS - 2)))

def yn_prompt(prompt):
    show_message(prompt)
    choice = stdscr.getkey().lower() 
    while choice not in ["y", "n"]:
        clear_message()
        show_message("Press (y)es or (n)o:")
        choice = stdscr.getkey().lower() 
    clear_message()
    if choice == "y":
        return True
    else:
        return False

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_input(prompt, max_length, input_type):
    curses.echo()
    while True:
        show_message(prompt)
        stdscr.refresh()
        string_input = stdscr.getstr(curses.LINES - 1, len(prompt) + 1, max_length)
        string_input = string_input.decode("utf-8")
        if string_input.lower() == "q":
            return False
        if input_type == "i" and is_int(string_input):
            break
        if input_type == "f" and is_float(string_input):
            break
        if input_type == "s" and len(string_input) > 0:
            break
        clear_message()
    curses.noecho()
    return string_input

def update_display_pad(display_list): # No support for text formatting (colors etc)
    display_pad.erase()
    if display_list:
        for line_number in range(len(display_list)):
            display_pad.addstr(line_number, 0, display_list[line_number])
    global display_pad_pos
    display_pad_pos = len(display_list) - curses.LINES + 4

def update_display_win(focused):
    display_window.chgat(curses.A_NORMAL)
    if focused:
        global display_pad_pos
        display_window.chgat(display_pad_pos, 0, -1, curses.A_REVERSE)

def update_options(option_dict, selector, focused):
    option_window.erase()
    option_number = 0
    for key in option_dict:
        option_window.addstr(option_number * 2, 0, key, curses.A_REVERSE)
        option_window.addstr(option_number * 2, 2, option_dict[key])
        if option_number == selector and focused:
            option_window.chgat(option_number * 2, 0, -1, curses.A_REVERSE)
        option_number += 1

def draw_windows():
    stdscr.noutrefresh()
    main_window.noutrefresh()
    display_window.noutrefresh(display_pad_pos, 0, 2, 2, curses.LINES - 3, vertical_divide - 1)
    option_window.noutrefresh()
    curses.doupdate()
    stdscr.move(curses.LINES - 1, 1)

HELP_LIST = ["Press TAB to switch between the display window and the options window","",
             "Move up and down in the options menu or display windows with the arrow keys","",
             "Options can be selected by pressing the letter or number next to the option",
             "To return to the main options menu from another menu press HOME",
             "To cancel entering data and return to the main menu enter the letter q and press enter"]

MAIN_OPTION_DICT = {"N": "New Exercise", "R": "Add Record", "V": "View Today's Record",
                    "A": "View All Records", "E": "View Exercise Records",
                    "S": "Save Records", "H": "Help", "Q": "Quit"}

if __name__ == "__main__":
    stdscr = curses.initscr()
    start_curses()
    stdscr.addstr(0, 0, "gym-trak", curses.A_REVERSE)
    stdscr.addstr(0, curses.COLS - len(get_date()), get_date(), curses.A_REVERSE)
    stdscr.chgat(0, 0, -1, curses.A_REVERSE)

    main_window = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    main_window.box()

    vertical_divide = math.floor(curses.COLS * 0.6667)

    focus_areas = ["display", "options"]
    focus = 1

    display_pad_pos = 0
    display_pad = curses.newpad(4096, 256)
    display_window = display_pad.subpad(0, 0)

    option_menu = "main"
    option_dict = MAIN_OPTION_DICT
    option_selector = 0
    option_window = main_window.subwin(curses.LINES - 4, curses.COLS - vertical_divide - 2, 2, vertical_divide + 1)

    load_records()
    while True:
        if option_menu == "main":
            option_dict = MAIN_OPTION_DICT
        update_options(option_dict, option_selector, (True if focus_areas[focus] == "options" else False))
        update_display_win((True if focus_areas[focus] == "display" else False))
        draw_windows()
        option = stdscr.getkey()

        if focus_areas[focus] == "display":
            if option == "KEY_UP" and display_pad_pos > 0:
                display_pad_pos -= 1
            elif option == "KEY_DOWN":
                display_pad_pos += 1
            elif option == "\t":
                focus += 1
                if focus > len(focus_areas) - 1:
                    focus -= len(focus_areas)

        elif focus_areas[focus] == "options":
            if option == "KEY_UP":
                option_selector -= 1
                if option_selector < 0:
                    option_selector += len(option_dict)
            elif option == "KEY_DOWN":
                option_selector += 1
                if option_selector >= len(option_dict):
                    option_selector -= len(option_dict)
            elif option == "\n":
                option = list(option_dict)[option_selector]
            elif option == "\t":
                focus += 1
                if focus > len(focus_areas) - 1:
                    focus -= len(focus_areas)

            if option_menu == "main":
                if option.lower() == "n":
                    input_exercise()
                elif option.lower() == "r":
                    if exercise_list == []:
                        show_message("No exercises found...")
                    else:
                        option_dict = generate_exercise_dict()
                        option_selector = 0
                        option_menu = "exercises-record"
                elif option.lower() == "v":
                    if exercise_list == []:
                        show_message("No records found...")
                    else:
                        update_display_pad(view_todays_records())
                elif option.lower() == "a":
                    if exercise_list == []:
                        show_message("No records found...")
                    else:
                        update_display_pad(view_all_records())
                elif option.lower() == "e":
                    if exercise_list == []:
                        show_message("No records found...")
                    else:
                        option_dict = generate_exercise_dict()
                        option_selector = 0
                        option_menu = "exercises-view"
                elif option.lower() == "s":
                    save_records()
                elif option.lower() == "h":
                    update_display_pad(HELP_LIST)
                elif option.lower() == "q":
                    break

            elif option_menu == "exercises-record":
                if option.upper() in option_dict:
                    input_record(option_dict[option.upper()])
                    option_menu = "main"
                elif option == "KEY_HOME":
                    option_selector = 0
                    option_menu = "main"

            elif option_menu == "exercises-view":
                if option.upper() in option_dict:
                    update_display_pad(view_exercise_records(option_dict[option.upper()]))
                    option_menu = "main"
                elif option == "KEY_HOME":
                    option_selector = 0
                    option_menu = "main"



    end_curses()
