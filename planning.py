# planning.py - Core functions

import os
import pickle
from pathlib import Path
from datetime import datetime, date, timedelta

__all__ = ["setup", "adduser", "UserData"]

DATA_FOLDER = "./data"
USER_RECORD = "./data/users"
EMPTY_DATA = {
    "dates": [],
    "intervals": [],
    "averages": []
}
DATE_FORMATS = [
    "%d/%m/%Y",
    "%d-%m-%Y"
]

def setup():
    if not os.path.exists("./data"):
        os.mkdir(DATA_FOLDER)
        Path(USER_RECORD).touch()

def get_user_data(userid):
    path = Path(DATA_FOLDER, userid)
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data

def write_user_data(data, userid):
    path = Path(DATA_FOLDER, userid)
    with open(path, "wb") as f:
        pickle.dump(data, f)

def has_user(user):
    with open(USER_RECORD, "r") as f:
        users = [user.strip() for user in f.readlines()]
    return user in users

def adduser(user):
    if has_user(user):
        return False
    
    with open(USER_RECORD, "a") as f:
        f.write(user + "\n")
    write_user_data(EMPTY_DATA, user)
    return True
    
def validate_date(input_date: str):
    """Return date object if input_date matches date format,
    Return None if otherwise."""
    input_date = input_date.strip().lower()

    if input_date == "today":
        return date.today()
    if input_date == "yesterday":
        return date.today() - timedelta(days=1)
    
    input_date = input_date.replace(" ", "")

    for f in DATE_FORMATS:
        try:
            valid_date = datetime.strptime(input_date, f)
            return valid_date.date()
        except ValueError:
            pass
    
    return None

class UserData:
    """Read, process and store user data"""
    
    def __init__(self, userid):
        if not has_user(userid):
            raise FileNotFoundError(f"User ID: {userid} is not in record")
        data = get_user_data(userid)
        self.userid = userid
        self.dates = data["dates"]
        self.intervals = data["intervals"]
        self.averages = data["averages"]
        
    def add(self, date):
        valid_date = validate_date(date)
        if valid_date:
            self.dates.append(valid_date)
            self.update_intervals()
            return valid_date.strftime(DATE_FORMATS[0])
        return False
    
    def update_intervals(self):
        if len(self.dates) > 1:
            interval = self.dates[-1] - self.dates[-2]
            self.intervals.append(interval)
            self.update_averages()

    def update_averages(self):
        if len(self.intervals) == 1:
            average = self.intervals[0]
        else:
            average = (self.intervals[-1] + self.intervals[-2]) / 2
        self.averages.append(average)
    
    def remove_previous(self):
        """Remove previous (pop) entry in dates. Return False if no previous
        entry was made, True if success"""
        try:
            self.intervals.pop()
            self.averages.pop()
        except IndexError:
            pass
        if self.dates:
            self.dates.pop()
            return True
        else:
            return False
        
    def trim(self):
        """Free up data to save space.
        Keep at least 6 dates, 5 intervals and 5 averages. 
        Return True if removed, False if otherwise"""
        if len(self.dates) > 6:
            self.dates = self.dates[-6:]
            self.intervals = self.intervals[-5:]
            self.averages = self.averages[-5:]
            return True
        else:
            return False

    def display_data(self, length: int):
        """Prettify/format data held and return string to be displayed.
        Return None if no entry was made.
        `length`: Number of entries to output. Set -1 for full output."""

        if length == -1:
            length = len(self.dates)

        out = []
        date_format = DATE_FORMATS[0]

        if not self.dates:
            return None
        
        assert len(self.intervals) \
           == (len(self.dates) - 1)
        
        for date, interval in zip(self.dates[-length:], \
                                  self.intervals[-(length-1):]):
            out.append(date.strftime(date_format))
            out.append(f"\t--{interval.days} days")

        # The one left out
        out.append(self.dates[-1].strftime(date_format))

        if self.averages:
            out.append("\nAverages: ")
            averages_list = " ".join([str(a.days) for a in self.averages[-length:]])
            out.append(averages_list)

        return "\n".join(out)

    def predict(self):
        """Predict the next date. Return date object if success, None if otherwise"""
        if self.dates:
            last = self.dates[-1]
            if self.averages:
                return (last + self.averages[-1]).strftime(DATE_FORMATS[0])
        else:
            return None
        
    def save(self):
        data = {
            "dates": self.dates,
            "intervals": self.intervals,
            "averages": self.averages
        }
        write_user_data(data, self.userid)
            
        
if __name__ == "__main__":
    setup()
    print(get_user_data("123111"))
    # print(adduser("123111"))
    # print(adduser("234555"))
    # print(adduser("123111"))
    # print(adduser("121110"))

