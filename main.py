"""
title: Large Mammal Population in Elk Island National Park
author: Joanna Hao
date-created: 2022-11-25
"""
import pathlib
import sqlite3


# ----- FUNCTIONS ----- #
# --- INPUTS
def getFileContent(filename) -> list:
    """
    extracts file content into 2D array
    :param filename: str
    :return: list (2D array)
    """
    file = open(filename)
    text_list = file.readlines()
    file.close()
    # clean up data
    for i in range(len(text_list)):
        # assuming not all rows have \n (often true for last row)
        if text_list[i][-1] == "\n":  # \n considered 1 char
            text_list[i] = text_list[i][:-1]

        text_list[i] = text_list[i].split(",")

        for j in range(len(text_list[i])):
            if text_list[i][j].isnumeric():
                text_list[i][j] = int(text_list[i][j])

    return text_list


def menu() -> int:
    print("""
Please choose an option:
1. Search Population Growth
2. Add new year data
3. Exit
    """)
    return int(input("> "))


# --- Processing



# --- Outputs



# --- variables
DATABASE_FILE = "large_mammals.db"
FIRST_RUN = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

if __name__ == "__main__":
    # ----- MAIN PROGRAM CODE ----- #
    if FIRST_RUN:
        # setup everything

    while True:
        # --- inputs
        CHOICE = menu()
        if CHOICE == 1:
            # START_YEAR =
            # END_YEAR =
            # ANIMALS_SEARCHED =
            pass
        elif CHOICE == 2:
            # YEAR =
            # ANIMALS_TO_ADD =
            pass

        # --- processing
        if CHOICE == 1:
            pass
        elif CHOICE == 2:
            pass

        # --- outputs
        if CHOICE == 1:
            pass
        elif CHOICE == 2:
            print("successfully added (or sum like this)")
        elif CHOICE == 3:
            print("Goodbye!")
            exit()
