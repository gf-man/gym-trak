from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Tree, MarkdownViewer
from textual.containers import Horizontal, Vertical

import math
import datetime
from enum import Enum

HELP_LIST = ["Press TAB to switch between the display window and the options window","",
             "Move up and down in the options menu or display windows with the arrow keys","",
             "Options can be selected by pressing the letter or number next to the option",
             "To return to the main options menu from another menu press HOME",
             "To cancel entering data and return to the main menu enter the letter q and press enter"]

MAIN_OPTION_DICT = {"N": "New Exercise", "R": "Add Record", "V": "View Today's Record",
                    "A": "View All Records", "E": "View Exercise Records",
                    "S": "Save Records", "H": "Help", "Q": "Quit"}


Exercise_Type = Enum("Exercise_Type", ["Resistance", "Bodyweight", "Isometric", "Distance"])

MAX_EX_NAME_LENGTH = 20

file = ""

class Exercise:
    def __init__(self, name, category):
        self.name = name
        self.category = Exercise_Type(category)
        self.record = {}

    def add_record(self, record):
        self.record.update(record)

exercise_list = []
date_list = []

ex_dict_overflow_chars = ['`', '-', '=', '[', ']', ';', "'", '#', ',', '.', '/' ,'!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '_', '+', ':', '@', '~', '<', '>', '?']

selected_section_position = []


def get_date():
    today = datetime.date.today()
    return today.strftime("%d/%m/%Y")

def is_date(string_to_check):
    try:
        datetime.datetime.strptime(string_to_check, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def load_records():
    file = open("gym.md", "r")
    records_started = False
    rec_date = "01/01/2000"
    for line in file:
        line = line.rstrip('\n')
        if is_date(line):
            rec_date = line
            records_started = True
        else:
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
    show_message("Saved to gym.md")

def generate_exercise_dict():
    ex_dict = {}
    counter = 0
    for ex in exercise_list:
        if ex.name[0].upper() not in ex_dict:
            ex_dict.update({ex.name[0].upper(): ex.name})
        else:
            if counter > 9:
                ex_dict.update({ex_dict_overflow_chars[counter - 10]: ex.name})
            else:
                ex_dict.update({str(counter): ex.name})
            counter += 1
    return ex_dict




class AllRecordsTree(Tree):
    """A tree displaying all records by date allowing the user to edit records"""

    def on_mount(self) -> None:
        self.root.expand()
        self.show_root = False
        for date in date_list:
            date_node = self.root.add(date)
            for exercise in exercise_list:
                if date in exercise.record:
                    ex_node = date_node.add(exercise.name)
                    record_pos = 0
                    for record in exercise.record[date]:
                        rec_node = ex_node.add_leaf('x'.join(record), data=[date, exercise.name, record_pos])
                        record_pos += 1
#            if date == date_list[-1]:
#                date_node.expand_all()




class NavBar(Horizontal):
    def compose(self) -> ComposeResult:
        yield Button("One")
        yield Button("Two")
        yield Button("Three")
        yield Button("X", classes="menu_button")


class GymTrakApp(App):
    CSS_PATH = "style.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        yield AllRecordsTree("All Records")

        yield NavBar()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    load_records()
    app = GymTrakApp()
    app.run()
