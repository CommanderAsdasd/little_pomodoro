#!/usr/bin/env python3


import time
import os
import sys
import click
import yaml
import datetime

@click.group()
def cli():
    pass

@cli.command()
@click.argument("time")
@click.option("--note", default=None)
def countdown(time, note):
    timer = Timer(time)
    timer.countdown()
    if note and timer.write_note:
        timer.note(note)

@cli.command()
@click.argument("number", default=0, required=False)
@click.option("--all", is_flag=True)
def notes(number, all):

    number, all = number, all
    notes = {}
    with open("notes.yaml", "r") as notefile:
        notes = yaml.load(notefile, Loader=yaml.FullLoader)

    def show():
        if all:
            select_all()
        else:
            select()

    def select_all():    
            for date, payload in notes.items():
                print("{} - {} - {}".format(date, payload.get("length"), payload["note"]))
    
    def select():
        # number reversed to get last values first
        nonlocal number
        number = ~int(number)
        print(number)
        with open("notes.yaml", "r") as notefile:
            date, payload = list(notes.keys())[number], notes.get(list(notes.keys())[number])
            print("{} - {} - {}".format(date, payload["length"], payload["note"]))

    show()

class Timer():

    def __init__(self, countdown):
        self.__time_start = time.time()
        self.__countdown = int(countdown)
        self.write_note = True

    def note(self, note):
        writable_data = {}
        at_time = str(datetime.datetime.now().replace(second=0, microsecond=0))
        writable_data[at_time] = {} 
        writable_data[at_time]["length"] = self.__countdown
        writable_data[at_time]["note"] = note
        with open("notes.yaml", "a") as notefile:
            yaml.safe_dump(writable_data, notefile, encoding='utf-8', allow_unicode=True, default_flow_style=False)


    def countdown(self):
        while self.__countdown > 0:
            try:
                sys.stdout.write("\r{seconds} Seconds".format(seconds=self.__countdown))
                sys.stdout.flush()
                time.sleep(1)
                self.__countdown = self.__countdown - 1
                if self.__countdown == 0:
                    sys.stdout.write("\n Time's up !")
                    sys.stdout.flush()

            except KeyboardInterrupt as e:
                self.write_note = False
                break
        
if __name__ == "__main__":

    cli()
