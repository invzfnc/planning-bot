# planning.py - Core functions

import os
import pickle
from pathlib import Path

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

def adduser(user):
    with open(USER_RECORD, "r") as f:
        users = [user.strip() for user in f.readlines()]
    if user in users:
        return False
    
    with open(USER_RECORD, "a") as f:
        f.write(user + "\n")
    write_user_data(EMPTY_DATA, user)
    return True
    
if __name__ == "__main__":
    setup()
    print(get_user_data("123111"))
    # print(adduser("123111"))
    # print(adduser("234555"))
    # print(adduser("123111"))
    # print(adduser("121110"))

