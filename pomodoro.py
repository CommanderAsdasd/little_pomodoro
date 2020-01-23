#!/usr/bin/env python
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
    if note:
        timer.note(note)
    timer.countdown()

# @click.option('--note', default=1, help='Number of greetings.')

class Timer():

    def __init__(self, countdown):
        self.__time_start = time.time()
        self.__countdown = int(countdown)

    def note(self, note):
        writable_data = {}
        at_time = str(datetime.datetime.now().replace(second=0, microsecond=0))
        writable_data[at_time] = {} 
        writable_data[at_time]["length"] = self.__countdown
        writable_data[at_time]["note"] = note
        with open("notes.yaml", "a") as notefile:
            yaml.safe_dump(writable_data, notefile, encoding='utf-8', allow_unicode=True, default_flow_style=False)

    # def kitchen(self,time_start, seconds, minutes):
        
    #     while True:
    #         try:
    #             sys.stdout.write("\r{minutes} Minutes {seconds} Seconds".format(minutes=minutes, seconds=seconds))
    #             sys.stdout.flush()
    #             time.sleep(1)
    #             seconds = int(time.time() - time_start) - minutes * 60
    #             if seconds >= 60:
    #                 minutes += 1
    #                 seconds = 0
    #         except KeyboardInterrupt, e:
    #             break

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

            except KeyboardInterrupt, e:
                break
        
if __name__ == "__main__":

    cli()
