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
    # --- clean up data
    for i in range(len(text_list)):  # reading individual lines of strings from file (working w/ a string)
        if text_list[i][-1] == "\n":  # removing newline at end of lines (except last row)
            text_list[i] = text_list[i][:-1]  # to make one long string

        if '"' not in text_list[i]:  # nice data
            text_list[i] = text_list[i].split(",")
        else:  # disgarsting data
            text_list[i] = text_list[i].split('"')  # to offset a survey comment containing a comma -->
            text_list[i][0] = text_list[i][0].split(",")  # becomes 2D array (split non-survey comment items nicely by ","s)
            text_list[i][-1] = text_list[i][-1].replace(",", "")

            # turn 2D array into 1D
            text_list[i][1] = [text_list[i][1]]  # convert into list from string for concatenation of lists & remove 3rd last item (empty space from split)
            text_list[i][-1] = [text_list[i][-1]]  # convert into list from string for concatenation of lists
            text_list[i] = text_list[i][0] + text_list[i][1] + text_list[i][-1]  # concatenate lists (ends w/ 1D list)
            text_list[i].pop(-3)

        for j in range(len(text_list[i])):
            if text_list[i][j].isnumeric():
                text_list[i][j] = int(text_list[i][j])
            elif text_list[i][j] == "NA":
                text_list[i][j] = ""

    return text_list


def menu() -> int:
    print("""
Please choose an option:
1. Search Population Growth
2. Add new year data
3. Exit
    """)
    return int(input("> "))


def getPopulationGrowthInputs():
    start_year = input("Start year? ")
    end_year = input("End year? ")
    species = input("Bison (1), Elk (2), Moose (3), Deer (4), or all (5)? ")
    return start_year, end_year, species


def getNewYearData():
    park_area = input("Area of park? ")
    population_year = input("Population year? ")
    survey_year = input("Survey year? ")
    survey_month = input("Survey month? ")
    survey_day = input("Survey day? ")
    species = input("Species name? ")
    unknown_age_sex_count = input("Number of animals with unknown age and sex? ")
    adult_male = input("Number of adult males? ")
    adult_female = input("Number of adult females? ")
    unknown_adult_count = input("Number of adults of unknown sex? ")
    yearling_count = input("Number of yearlings? ")
    calf_count = input("Number of calves? ")
    survey_total = input("Survey total? ")
    sightability_correction_factor = input("Sightability correction factor? ")
    extra_captives = input("Number of additional captives? ")
    animals_removed = input("Number of animals removed prior to survey? ")
    fall_population = input("Estimate of fall population? ")
    comment = input("Survey comment: ")  # need to put quotes around if ',' inside
    method = input("Estimate method? ")

# --- Processing
def setupContent(list_data):
    global CURSOR, CONNECTION
    CURSOR.execute("""
        CREATE TABLE
            populations (
                park_area TEXT NOT NULL,
                population_year INTEGER NOT NULL,
                survey_year INTEGER,
                survey_month INTEGER,
                survey_day INTEGER,
                species TEXT NOT NULL,
                unknown_age_sex_count INTEGER,
                adult_male_count INTEGER,
                adult_female_count INTEGER,
                adult_unknown_count INTEGER,
                yearling_count INTEGER,
                calf_count INTEGER,
                survey_total INTEGER,
                sightability_correction_factor INTEGER,
                additional_captive_count INTEGER,
                animals_removed_before_survey INTEGER,
                fall_population_estimate INTEGER,
                survey_comment TEXT,
                estimate_method TEXT
            )
    ;""")

    for i in range(1, len(list_data)):
        CURSOR.execute("""
            INSERT INTO
                populations
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ;""", list_data[i])

    CONNECTION.commit()


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
        CONTENT = getFileContent("Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv")
        setupContent(CONTENT)

    # for i in range(len(CONTENT)):
    #     print(CONTENT[i])

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

# check ability to exclude newly added data --> without affecting previous data calculations?

