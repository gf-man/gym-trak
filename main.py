from textual import events, on
from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button, Tree, Select, Input
from textual.reactive import reactive
from textual.containers import Horizontal, Vertical, Grid, ScrollableContainer
from textual.validation import Validator, ValidationResult, Function, Number

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


def get_date() -> str:
    today = datetime.date.today()
    return today.strftime("%d/%m/%Y")

def is_date(string_to_check: str) -> bool:
    try:
        if string_to_check == "":
            return True
        else:
            datetime.datetime.strptime(string_to_check, "%d/%m/%Y")
            return True
    except ValueError:
        return False

def is_integer(string_to_check:str) -> bool:
    try:
        int(string_to_check)
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
#    show_message("Saved to gym.md")

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


class RecordDataInput(Horizontal):
    """Widget for inputting record data, should change depending on exercise type"""
    exercise_type = reactive(0, layout=True)

    position = 0

    validator_dict = {"Weight":[Number(minimum=0.1, maximum=1000)], 
                      "Reps":[Number(minimum=1, maximum=1000), Function(is_integer, "Not a whole number")], 
                      "Sets":[Number(minimum=1, maximum=1000), Function(is_integer, "Not a whole number")], 
                      "Time (s)":[Number(minimum=1, maximum=60)],
                      "Time (m)":[Number(minimum=1, maximum=60)],
                      "Distance":[Number(minimum=1, maximum=100)]}

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Weight", id="first_input", validators=self.validator_dict["Weight"])
        yield Input(placeholder="Reps", id="second_input", validators=self.validator_dict["Reps"])
        yield Input(placeholder="Sets", id="third_input", validators=self.validator_dict["Sets"])
        yield Button("/\\", classes="up_down_buttons", id="up_button", disabled=True)
        yield Button("\\/", classes="up_down_buttons", id="down_button", disabled=True)

    def watch_exercise_type(self) -> None:
        if self.exercise_type == Exercise_Type["Resistance"].value:
            try:
                self.query_one("#third_input")
            except:
                self.mount(Input(placeholder="Sets", id="third_input"), before=2)
            self.query_one("#first_input").placeholder = "Weight"
            self.query_one("#second_input").placeholder = "Reps"
            self.query_one("#third_input").placeholder = "Sets"

            self.query_one("#first_input").validators = self.validator_dict["Weight"]
            self.query_one("#second_input").validators = self.validator_dict["Reps"]
            self.query_one("#third_input").validators = self.validator_dict["Sets"]

        elif self.exercise_type == Exercise_Type["Bodyweight"].value:
            try:
                self.query_one("#third_input").remove()
            except:
                pass
            self.query_one("#first_input").placeholder = "Reps"
            self.query_one("#second_input").placeholder = "Sets"

            self.query_one("#first_input").validators = self.validator_dict["Reps"]
            self.query_one("#second_input").validators = self.validator_dict["Sets"]

        elif self.exercise_type == Exercise_Type["Isometric"].value:
            try:
                self.query_one("#third_input").remove()
            except:
                pass
            self.query_one("#first_input").placeholder = "Time (s)"
            self.query_one("#second_input").placeholder = "Sets"

            self.query_one("#first_input").validators = self.validator_dict["Time (s)"]
            self.query_one("#second_input").validators = self.validator_dict["Sets"]

        elif self.exercise_type == Exercise_Type["Distance"].value:
            try:
                self.query_one("#third_input").remove()
            except:
                pass
            self.query_one("#first_input").placeholder = "Time (m)"
            self.query_one("#second_input").placeholder = "Distance"

            self.query_one("#first_input").validators = self.validator_dict["Time (m)"]
            self.query_one("#second_input").validators = self.validator_dict["Distance"]

def reorder_record_data_inputs(data_inputs):
    """Reorders RecordDataInput(s) according to their order in the list"""
    data_input_counter = 0
    for data_input in data_inputs:
        data_input.position = data_input_counter
        data_input_counter += 1
    return data_inputs



class RecordEditScreen(ModalScreen):
    """Screen containing record data allowing more rows to be added, will change depending on previously selected exercise (type)"""
    number_of_added_record_data_inputs = 0

    def enable_disable_up_down_buttons(self):
        for up_down_button in self.query(".up_down_buttons"):
            up_down_button.disabled = False
        self.query("RecordDataInput").first().query_one("#up_button").disabled = True
        self.query("RecordDataInput").last().query_one("#down_button").disabled = True

    def compose(self) -> ComposeResult:
        with Grid():
            #yield Input(placeholder="Date (leave blank for today)")
            yield Input(placeholder=get_date(), validators=[Function(is_date, "Not a valid date")])
            yield Select(((ex.name, ex) for ex in exercise_list), allow_blank=False)
            with ScrollableContainer(id="record_data_inputs"):
                yield RecordDataInput()
                with Horizontal(id="add_remove_buttons"):
                    yield Button("Add", variant="success", id="add_record_data_input")
                    yield Button("Remove", variant="error" ,id="remove_record_data_input", disabled=True)
            yield Button("Confirm", variant="success", id="confirm")
            yield Button("Cancel", variant="error", id="cancel")

    def on_select_changed(self, event: Select.Changed) -> None:
        for record_data_input in self.query("RecordDataInput"):
            record_data_input.exercise_type = event.select.value.category.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.app.pop_screen()
        elif event.button.id == "confirm":
            self.dismiss([])
        elif event.button.id == "up_button":
            move_position = event.button.parent.position - 1
            self.query_one("#record_data_inputs").move_child(event.button.parent, before=move_position)
            self.query_one("#record_data_inputs").displayed_children[0:-1] = reorder_record_data_inputs(self.query_one("#record_data_inputs").displayed_children[0:-1])
            self.enable_disable_up_down_buttons()
        elif event.button.id == "down_button":
            move_position = event.button.parent.position + 1
            self.query_one("#record_data_inputs").move_child(event.button.parent, after=move_position)
            self.query_one("#record_data_inputs").displayed_children[0:-1] = reorder_record_data_inputs(self.query_one("#record_data_inputs").displayed_children[0:-1])
            self.enable_disable_up_down_buttons()

    @on(Button.Pressed, "#add_record_data_input")
    async def action_add_record_data_input(self) -> None:
        self.number_of_added_record_data_inputs += 1
        new_record_data_input = RecordDataInput()
        new_record_data_input.position = self.number_of_added_record_data_inputs
        await self.query_one("#record_data_inputs").mount(new_record_data_input, before=self.number_of_added_record_data_inputs)
        try:
            new_record_data_input.exercise_type = self.query_one("Select").value.category.value
        except:
            new_record_data_input.exercise_type = 1
        if self.number_of_added_record_data_inputs == 1:
            self.get_widget_by_id("remove_record_data_input").disabled = False
        self.enable_disable_up_down_buttons()

    @on(Button.Pressed, "#remove_record_data_input")
    def action_remove_record_data_input(self) -> None:
        record_data_inputs = self.query("RecordDataInput")
        if record_data_inputs:
            record_data_inputs.filter("RecordDataInput").last().remove()
            self.number_of_added_record_data_inputs -= 1
            if self.number_of_added_record_data_inputs == 0:
                self.get_widget_by_id("remove_record_data_input").disabled = True
        self.enable_disable_up_down_buttons()

class AllRecordsTree(Tree):
    """A tree displaying all records by date allowing the user to edit records"""

    def on_mount(self) -> None:
        self.root.expand()
        self.show_root = False
        for date in date_list[1:]:
            date_node = self.root.add(date)
            for exercise in exercise_list:
                if date in exercise.record:
                    ex_record_string = ""
                    record_pos = 0
                    for record in exercise.record[date]:
                        if record_pos == 0:
                            pass
                        else:
                            ex_record_string += " > "
                        record_pos += 1
                        ex_record_string += 'x'.join(record)
                    ex_node = date_node.add(exercise.name, data=[date, exercise.name], expand=True, allow_expand=False)
                    ex_node.add_leaf(ex_record_string)
#            if date == date_list[-1]:
#                date_node.expand_all()






class GymTrakApp(App):
    CSS_PATH = "style.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("r", "add_record", "Add Record")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        yield AllRecordsTree("All Records")
        
        with Horizontal(id="nav_bar"):
            yield Button("Add Record", classes="nav_button", id="add_record")
            yield Button("Two", classes="nav_button")
            yield Button("Three", classes="nav_button")
            yield Button("X", classes="menu_button")
            

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


    @on(Button.Pressed, "#add_record")
    def action_add_record(self) -> None:
        self.push_screen(RecordEditScreen())


if __name__ == "__main__":
    load_records()
    app = GymTrakApp()
    app.run()
