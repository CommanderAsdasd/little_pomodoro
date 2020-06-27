#!/usr/bin/env pipenv-shebang


import time
import os
import sys
import click
import yaml
import datetime
import ast
import math

@click.group()
def cli():
    pass

#region   countdown option
@cli.command()
@click.argument("time")
@click.option("--note", default=None)
@click.option("--jobtype", default="job")
def countdown(time, note, jobtype):
    if jobtype not in ["pet", "job"]:
        print("Jobtype can only be \'pet\' or \'job\' ")
        return
    timer = Timer(time)
    timer.jobtype = jobtype
    timer.countdown()
    timer.make_note(note)
#endregion

# TODO: series of timers


#region   Timer class
class Timer():
    '''states - Running, Interrupted, FInished'''

    def __init__(self, countdown):
        self.__time_start = time.time()
        self.__length = int(countdown)
        self.__countdown = int(countdown)
        self.writable_data = {}
        self.state = None

    def submit_score(self, mark):

        if self.jobtype == "pet":
            update_score = int(math.floor(self.__length / 60)) * -2
        if self.jobtype == "job":
            update_score = int(math.floor(self.__length / 60) * (mark / 10))
        try:
            with open("score.yaml", "r") as scorefile:
                scoretext = scorefile.read()
                if scoretext:
                    score = int(scoretext)
                else:
                    score = 0
        except FileNotFoundError:
            score = 0
        with open("score.yaml", "w") as scorefile:
            score += update_score
            scorefile.write(str(score))
        print("Current score {}".format(score))

    
    def write_file(self):
        with open("notes.yaml", "a") as notefile:
            yaml.safe_dump(self.writable_data, notefile, encoding='utf-8', allow_unicode=True, default_flow_style=False)


    #region   note method
    def make_note(self, note):
        self.writable_data = {}
        at_time = str(datetime.datetime.now().replace(second=0, microsecond=0))
        self.writable_data[at_time] = {} 
        self.writable_data[at_time]["length"] = self.__length
        if self.state == "Finished":
            self.writable_data[at_time]["status"] = self.state
            self.writable_data[at_time]["note"] = note

            print("\n How goals achieved from 0 to 10 ")
            mark = int(input())
            self.writable_data[at_time]["mark"] = mark 
            self.submit_score(mark)

            print("\n What an outcomes from timer: ")
            self.writable_data[at_time]["outcomes"] = input()
            
            self.write_file()

            # TODO: add various prints to my console helper
            print("La vida no vale nada!")
        elif self.state == "Interrupted":
            self.writable_data[at_time]["status"] = self.state

            print("\n Cause of interruption: ")
            self.writable_data[at_time]["cause"] = input()
            self.write_file()
            
    #endregion


    def countdown(self):
        self.state = "Running"
        while self.__countdown > 0:
            try:
                sys.stdout.write("\r{seconds} Seconds".format(seconds=self.__countdown))
                sys.stdout.flush()
                time.sleep(1)
                self.__countdown = self.__countdown - 1
                if self.__countdown == 0:
                    self.state = "Finished"
                    sys.stdout.write("\n Time's up !")
                    sys.stdout.flush()
                    
            except KeyboardInterrupt as e:
                self.state = "Interrupted"
                # DEBUG:
                # self.state = "Finished"
                break
#endregion
        
if __name__ == "__main__":

    cli()
