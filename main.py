import os
from datetime import date
from enum import Enum


Exercise_Type = Enum("Exercise_Type", ["Resistance", "Bodyweight", "Isometric", "Distance"])

exercise_list = []
date_list = []


def get_date():
    today = date.today()
    return today.strftime("%d/%m/%Y")

class Exercise:
    def __init__(self, name, category):
        self.name = name
        self.category = Exercise_Type(category)
        self.record = {}

    def add_record(self, record):
        self.record.update(record)


def create_exercise():
    print("Add a new Exercise")
    name = input("Exercise name:")
    print("What type of Exercise?")
    category = int(input("1: Resistance, 2: Bodyweight, 3: Isometric, 4: Distance"))
    exercise_list.append(Exercise(name, category))


def create_record():
    print("Record Exercise")
    print(', '.join([ex.name for ex in exercise_list]))
    record_exercise = input("Exercise name:")
    for ex in exercise_list:
        if record_exercise == ex.name:
            if ex.category == Exercise_Type["Resistance"]:
                weight = input("Weight:\n")
                reps = input("Reps:\n")
                sets = input("Sets:\n")
                ex.add_record({get_date(): [weight, reps, sets]})
            elif ex.category == Exercise_Type["Bodyweight"]:
                reps = input("Reps:\n")
                sets = input("Sets:\n")
                ex.add_record({get_date(): [reps, sets]})
            elif ex.category == Exercise_Type["Isometric"]:
                time = input("Time:\n")
                reps = input("Sets:\n")
                ex.add_record({get_date(): [time, reps]})
            elif ex.category == Exercise_Type["Distance"]:
                time = input("Time:\n")
                dist = input("Distance:\n")
                ex.add_record({get_date(): [time, dist]})

            if get_date() not in date_list:
                date_list.append(get_date())
            break

def view_todays_records():
    for ex in exercise_list:
        if get_date() in ex.record:
            print(ex.name, ex.record[get_date()])

def view_exercise_records():
    ex = input("Exercise name:")
    if ex in exercise_list:
        print(ex.name)
        for record in ex.record:
            print(record)

def view_all_records():
    for rec_date in date_list:
        for ex in exercise_list:
            if rec_date in ex.record:
                print(ex.name, ex.record[rec_date])



if __name__ == "__main__":
    get_date()
    while True:
        print("N: New Exercise, R: Add Record, V: View Today's Record, A: View All Records, E: View Exercise Records")
        option = input()
        if option.lower() == "n":
            create_exercise()
        elif option.lower() == "r":
            create_record()
        elif option.lower() == "v":
            view_todays_records()
        elif option.lower() == "a":
            view_all_records()
        elif option.lower() == "e":
            view_exercise_records()
