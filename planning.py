# planning.py - Core functions

import os
import pickle
from pathlib import Path
from datetime import datetime, date, timedelta

__all__ = ["adduser",]

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
    
    def __init__(self, userid, cached_data):
        if not has_user(userid):
            raise FileNotFoundError(f"User ID: {userid} is not in record")
        if not userid in cached_data:
            cached_data[userid] = get_user_data(userid)
        
    def add(self, date):
        pass
        
if __name__ == "__main__":
    setup()
    print(get_user_data("123111"))
    # print(adduser("123111"))
    # print(adduser("234555"))
    # print(adduser("123111"))
    # print(adduser("121110"))

