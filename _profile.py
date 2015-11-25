# Author: Thomas Fischer
# GitHub: gragas

# This file contains one class: Profile.
# Profile represents a user's profile.
# It stores information about the user,
# like the user's name, level, and various
# other attributes.
# Profiles can be saved and loaded. All
# profiles are saved in the folder
# profiles/ under the name of the profile.
# For example, the relative path of my
# profile would be profiles/tom.

import os
import sys
import datetime
import traceback

class Profile:
    def __init__(self, name=None, load_from_file=False):
        if name is None:
            for line in traceback.format_stack()[:-1]:
                print(line)
            print("ERROR: You must specify a profile name.")
            sys.exit(1)
        self.name = name
        if load_from_file:
            self.load()
            return
        self.level = 0
        self.wins = 0
        self.losses = 0
        self.games_started = 0
        self.gold_earned = 0
        self.gold_spent = 0
        self.gold_taxed = 0
        self.wood_collected = 0
        self.stone_collected = 0
        self.largest_population = 0
        self.units_killed = 0
        self.kingdoms_conquered = 0
        self.date_created = datetime.datetime.today()
        self.check_attributes()

    def check_attributes(self):
        attributes = [
            ("name", str),
            ("level", int),
            ("wins", int),
            ("losses", int),
            ("games_started", int),
            ("gold_earned", int),
            ("gold_spent", int),
            ("gold_taxed", int),
            ("wood_collected", int),
            ("stone_collected", int),
            ("largest_population", int),
            ("units_killed", int),
            ("kingdoms_conquered", int),
            ("date_created", datetime.datetime),
        ]
        for attr, attr_type in attributes:
            if not hasattr(self, attr) or getattr(self, attr) is None:
                self.missing_attribute_error(attr)
            if type(getattr(self, attr)) is not attr_type:
                try:
                    setattr(self, attr, attr_type(getattr(self, attr)))
                except:
                    if attr == "date_created":
                        try:
                            self.date_created = datetime.datetime.strptime(
                                self.date_created,
                                "%Y-%m-%d",
                            )
                            continue
                        except:
                            self.could_not_cast_attribute_error(attr)
                    self.could_not_cast_attribute_error(attr)

    def missing_attribute_error(self, attr):
        print("ERROR: This profile's '" + attr + "' attribute was never set.")
        sys.exit(1)

    def could_not_cast_attribute_error(self, attr):
        print("ERROR: This profile's '" + attr + \
              "' attribute is of incorrect type.")
        sys.exit(1)

    def load(self):
        self.level = None
        self.wins = None
        self.losses = None
        self.games_started = None
        self.gold_earned = None
        self.gold_spent = None
        self.gold_taxed = None
        self.wood_collected = None
        self.stone_collected = None
        self.largest_population = None
        self.units_killed = None
        self.kingdoms_conquered = None
        self.date_created = None
        try:
            if not os.path.isfile(os.path.join("profiles", self.name)):
                for line in traceback.format_stack()[:-1]:
                    print(line)
                print("ERROR: " + os.path.join("profiles", self.name) + \
                      " is not a file.")
                sys.exit(1)
            with open(os.path.join("profiles", self.name), "r") as _file:
                for line in _file:
                    parsed = line.strip().split(" ")
                    if len(parsed) >= 2:
                        key = parsed[0]
                        if hasattr(self, key):
                            setattr(self, key, " ".join(parsed[1:]))
                        else:
                            for line in traceback.format_stack()[:-1]:
                                print(line)
                            print("ERROR: No such profile attribute '" + key + \
                                  "'.")
                            sys.exit(1)
            self.check_attributes()
        except Exception as e:
            print(e)
            for line in traceback.format_stack()[:-1]:
                print(line)
            print("ERROR: Could not load profile.")
            sys.exit(1)

    def save(self):
        file_path = os.path.join("profiles", self.name)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, "w") as _file:
            _file.write(self.__repr__())
        return
        try:
            file_path = os.path.join("profiles", self.name)
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            with open(file_path, "w") as _file:
                _file.write(self.__repr__())
        except:
            for line in traceback.format_stack()[:-1]:
                print(line)
            print("ERROR: Could not save profile.")
            sys.exit(1)

    def __str__(self):
        return self.name + ", Created " + self.date_created.strftime("%Y-%m-%d")

    def __repr__(self):
        strings = [
            "name " + self.name,
            "level " + str(self.level),
            "wins " + str(self.wins),
            "losses " + str(self.losses),
            "games_started " + str(self.games_started),
            "gold_earned " + str(self.gold_earned),
            "gold_spent " + str(self.gold_spent),
            "gold_taxed " + str(self.gold_taxed),
            "wood_collected " + str(self.wood_collected),
            "stone_collected " + str(self.stone_collected),
            "largest_population " + str(self.largest_population),
            "units_killed " + str(self.units_killed),
            "kingdoms_conquered " + str(self.kingdoms_conquered),
            "date_created " + self.date_created.strftime("%Y-%m-%d"),
        ]
        return "\n".join(strings)
