import os
import datetime
from enum import Enum


Exercise_Type = Enum("Exercise_Type", ["Resistance", "Bodyweight", "Isometric", "Distance"])

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
    print("Add a new Exercise")
    name = input("Exercise name:")
    print("What type of Exercise?")
    category = int(input("1: Resistance, 2: Bodyweight, 3: Isometric, 4: Distance"))
    exercise_list.append(Exercise(name, category))


def input_record():
    print("Record Exercise")
    print(', '.join([ex.name for ex in exercise_list]))
    record_exercise = input("Exercise name:")
    for ex in exercise_list:
        if record_exercise == ex.name:
            if ex.category == Exercise_Type["Resistance"]:
                weight = input("Weight:\n")
                reps = input("Reps:\n")
                sets = input("Sets:\n")
                ex.add_record({get_date(): [weight + "kg", reps, sets]})
            elif ex.category == Exercise_Type["Bodyweight"]:
                reps = input("Reps:\n")
                sets = input("Sets:\n")
                ex.add_record({get_date(): [reps, sets]})
            elif ex.category == Exercise_Type["Isometric"]:
                time = input("Time:\n")
                reps = input("Sets:\n")
                ex.add_record({get_date(): [time + "s", reps]})
            elif ex.category == Exercise_Type["Distance"]:
                time = input("Time:\n")
                dist = input("Distance:\n")
                ex.add_record({get_date(): [time + "m", dist + "km"]})

            if get_date() not in date_list:
                date_list.append(get_date())
            break

def view_todays_records():
    for ex in exercise_list:
        if get_date() in ex.record:
            print(ex.name, ex.record[get_date()])

def view_exercise_records():
    ex_name = input("Exercise name:")
    for ex in exercise_list:
         if ex_name == ex.name:
            for record in ex.record:
                print(record, ex.record[record])

def view_all_records():
    for rec_date in date_list:
        for ex in exercise_list:
            if rec_date in ex.record:
                print(ex.name, ex.record[rec_date])


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
                print(ex_name)
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
                        print("added record", rec_date, ex_rec)
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

if __name__ == "__main__":
    print(get_date())
    load_records()
    while True:
        print("N: New Exercise, R: Add Record, V: View Today's Record, A: View All Records, E: View Exercise Records")
        option = input()
        if option.lower() == "n":
            input_exercise()
        elif option.lower() == "r":
            input_record()
        elif option.lower() == "v":
            view_todays_records()
        elif option.lower() == "a":
            view_all_records()
        elif option.lower() == "e":
            view_exercise_records()
        elif option.lower() == "s":
            save_records()
