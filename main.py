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


def input_exercise():
    #print("Add a new Exercise")
    name = get_input("Exercise name: ", MAX_EX_NAME_LENGTH)
    if name.lower() == "q":
        return
    #print("What type of Exercise? ")
    category = int(get_input("1: Resistance, 2: Bodyweight, 3: Isometric, 4: Distance: ", 1))
    exercise_list.append(Exercise(name, category))

def generate_exercise_dict():
    ex_dict = {}
    counter = 1
    for ex in exercise_list:
        ex_dict.update({str(counter): ex.name})
        counter += 1
    return ex_dict
    

def input_record(ex_name):
    #print("Add a Record")
    
    for ex in exercise_list:
        if ex_name == ex.name:
            if ex.category == Exercise_Type["Resistance"]:
                weight = get_input("Weight(kilograms): ", 4)
                reps = get_input("Reps: ", 2)
                sets = get_input("Sets: ", 2)
                ex.add_record({get_date(): [weight + "kg", reps, sets]})
            elif ex.category == Exercise_Type["Bodyweight"]:
                reps = get_input("Reps: ", 2)
                sets = get_input("Sets: ", 2)
                ex.add_record({get_date(): [reps, sets]})
            elif ex.category == Exercise_Type["Isometric"]:
                time = get_input("Time(seconds): ", 3)
                reps = get_input("Sets: ", 2)
                ex.add_record({get_date(): [time + "s", reps]})
            elif ex.category == Exercise_Type["Distance"]:
                time = get_input("Time(minutes): ", 3)
                dist = get_input("Distance(kilometers): ", 3)
                ex.add_record({get_date(): [time + "m", dist + "km"]})

            
            if get_date() not in date_list:
                date_list.append(get_date())
            break

def view_todays_records():
    todays_records_list = []
    for ex in exercise_list:
        if get_date() in ex.record:
            todays_records_list.append(ex.name + " " + "x".join(ex.record[get_date()]))
    return todays_records_list

def view_exercise_records(ex_name):
    ex_records_list = []
    for ex in exercise_list:
         if ex_name == ex.name:
            ex_records_list.append(ex_name)
            for record in ex.record:
                ex_records_list.append(str(record + " " + "x".join(ex.record[record])))
    return ex_records_list

def view_all_records():
    all_records_list = []
    for rec_date in date_list:
        all_records_list.append(rec_date)
        for ex in exercise_list:
            if rec_date in ex.record:
                all_records_list.append(str(ex.name + ":" + "x".join(ex.record[rec_date])))
        all_records_list.append("")
    return all_records_list


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
                ex_rec = ex_data[1].split('x')
                if ex_rec[0][-2:] == "kg":
                    # Resistance
                    ex_cat = 1
                elif ex_rec[0][-1:] == "s":
                    # Isometric
                    ex_cat = 3
                elif ex_rec[1][-2:] == "km":
                    # Distance
                    ex_cat = 4
                else:
                    # Bodyweight
                    ex_cat = 2
                if ex_name not in [ex.name for ex in exercise_list]:
                    exercise_list.append(Exercise(ex_name, ex_cat))

                for ex in exercise_list:
                    if ex.name == ex_name:
                        ex.add_record({rec_date: ex_rec})
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
                output_line = "- " + ex.name + ":" + "x".join(ex.record[rec_date]) + "\n"
                file.write(output_line)
        file.write("\n")
    file.close()
    print("Records Saved")

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

def get_input(prompt, max_length):
    curses.echo()
    stdscr.addstr(curses.LINES - 1, 1, prompt)
    stdscr.refresh()
    string_input = stdscr.getstr(curses.LINES - 1, len(prompt) + 1, max_length)
    stdscr.addstr(curses.LINES -1, 1, str("  " * (len(prompt) + max_length + 1)))
    curses.noecho()
    return string_input.decode("utf-8")

def update_display(display_list):
    display_pad.erase()
    if display_list:
        for line_number in range(len(display_list)):
            display_pad.addstr(line_number, 0, display_list[line_number])

def update_options(option_dict, selected):
    option_window.erase()
    option_number = 0
    for key in option_dict:
        option_window.addstr(option_number * 2, 0, key, curses.A_REVERSE)
        option_window.addstr(option_number * 2, 2, option_dict[key])
        if option_number == selected:
            option_window.chgat(option_number * 2, 0, -1, curses.A_REVERSE)
        option_number += 1

def draw_windows():
    stdscr.noutrefresh()
    main_window.noutrefresh()
    display_window.noutrefresh(display_pad_pos, 0, 2, 2, curses.LINES - 3, vertical_divide)
    option_window.noutrefresh()
    curses.doupdate()
    stdscr.move(curses.LINES - 1, 1)


MAIN_OPTION_DICT = {"N": "New Exercise", "R": "Add Record", "V": "View Today's Record", "A": "View All Records", "E": "View Exercise Records", "S": "Save Records" , "Q": "Quit"}

if __name__ == "__main__":
    stdscr = curses.initscr()
    start_curses()
    stdscr.addstr(0, 0, "gym-trak", curses.A_REVERSE)
    stdscr.addstr(0, curses.COLS - len(get_date()), get_date(), curses.A_REVERSE)
    stdscr.chgat(0, 0, -1, curses.A_REVERSE)

    main_window = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    main_window.box()

    vertical_divide = math.floor(curses.COLS * 0.75)

    display_pad_pos = 0
    display_pad = curses.newpad(4096, 256)
    display_window = display_pad.subpad(0, 0)

    option_menu = "main"
    option_dict = MAIN_OPTION_DICT
    option_selector = 0
    option_window = main_window.subwin(curses.LINES - 4, curses.COLS - vertical_divide - 2, 2, vertical_divide + 1)

    load_records()
    while True:
        #stdscr.addstr(curses.LINES - 1, 0, "N: New Exercise, R: Add Record, V: View Today's Record, A: View All Records, E: View Exercise Records, S: Save Records , Q: Quit")
        if option_menu == "main":
            option_dict = MAIN_OPTION_DICT
        update_options(option_dict, option_selector)
        draw_windows()
        option = stdscr.getkey()

        if option.lower() == "k" and display_pad_pos > 0:
            display_pad_pos -= 1
        elif option.lower() == "j":
            display_pad_pos += 1


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

        if option_menu == "main":
            if option.lower() == "n":
                input_exercise()
            elif option.lower() == "r":
                option_dict = generate_exercise_dict()
                option_menu = "exercises-record"
            elif option.lower() == "v":
                update_display(view_todays_records())
            elif option.lower() == "a":
                update_display(view_all_records())
            elif option.lower() == "e":
                option_dict = generate_exercise_dict()
                option_menu = "exercises-view"
            elif option.lower() == "s":
                save_records()
            elif option.lower() == "q":
                break
        elif option_menu == "exercises-record":
            if option in option_dict:
                input_record(option_dict[option])
                option_menu = "main"
            elif option == "KEY_HOME":
                option_menu = "main"
        elif option_menu == "exercises-view":
            if option in option_dict:
                update_display(view_exercise_records(option_dict[option]))
                option_menu = "main"
            elif option == "KEY_HOME":
                option_menu = "main"



    end_curses()
