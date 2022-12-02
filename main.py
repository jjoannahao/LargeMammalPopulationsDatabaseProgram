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
        else:
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
    # print("Welcome to the Elk Island National Park Large Mammal population database! ")
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
    print("""
NOTE:
    Some data is required while some isn't. 
    For questions without the required (R) symbol, you can leave the field blank if there's no data.
    """)
    park_area = input("Area of park? (R) ")
    dataValidationBlanks(park_area)
    population_year = input("Population year? (R) ")
    dataValidationBlanks(population_year)
    population_year = int(population_year)
    if population_year >= 1905 and population_year <= 2017:
        print("Population year data already exists.")
        return getNewYearData()
    survey_year = input("Survey year? ")
    dataValidationInts(survey_year)
    survey_month = input("Survey month? (1-12) ")
    dataValidationSurveyDate(survey_month, 1, 12)
    survey_day = input("Survey day? (1-31) ")
    dataValidationSurveyDate(survey_day, 1, 31)
    species = input("Species name? (R) ")
    dataValidationBlanks(species)
    unknown_age_sex_count = input("Number of animals with unknown age and sex? ")
    dataValidationInts(unknown_age_sex_count)
    adult_male = input("Number of adult males? ")
    dataValidationInts(adult_male)
    adult_female = input("Number of adult females? ")
    dataValidationInts(adult_male)
    unknown_adult_count = input("Number of adults of unknown sex? ")
    dataValidationInts(unknown_adult_count)
    yearling_count = input("Number of yearlings? ")
    dataValidationInts(yearling_count)
    calf_count = input("Number of calves? ")
    dataValidationInts(calf_count)
    survey_total = input("Survey total? ")
    dataValidationInts(survey_total)
    sightability_correction_factor = input("Sightability correction factor? ")
    dataValidationInts(sightability_correction_factor)
    extra_captives = input("Number of additional captives? ")
    dataValidationInts(extra_captives)
    animals_removed = input("Number of animals removed prior to survey? ")
    dataValidationInts(animals_removed)
    fall_population = input("Estimate of fall population? ")
    dataValidationInts(fall_population)
    comment = input("Survey comment: ")  # need to put quotes around if ',' inside
    if "," in comment:
        comment = '"' + comment + '"'
    method = input("Estimate method? ")

    return [park_area, population_year, survey_year, survey_month, survey_day, species, unknown_age_sex_count, adult_male, adult_female, unknown_adult_count, yearling_count, calf_count, survey_total, sightability_correction_factor, extra_captives, animals_removed, fall_population, comment, method]


# --- Processing
def dataValidationSurveyDate(variable, lower_bound, upper_bound):
    if variable.isnumeric():
        variable = int(variable)
        if variable < lower_bound or variable > upper_bound:
            print(f"Please enter a valid {variable}.")
            return getNewYearData()


def dataValidationInts(variable):
    if variable.isnumeric():
        return int(variable)
    return None


def dataValidationBlanks(variable):
    if variable == "":
        print(f"{variable} can't be left blank.")
        return getNewYearData()


def setupContent(data_list):
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
    insertData(data_list)
    CONNECTION.commit()


def insertData(list_data):
    global CURSOR, CONNECTION
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

    while True:
        print("Welcome to the Elk Island National Park Large Mammal population database! ")  # potential duplicate that could be in menu
        # --- inputs
        CHOICE = menu()
        if CHOICE == 1:
            START_YEAR, END_YEAR, SPECIES = getPopulationGrowthInputs()
        elif CHOICE == 2:
            NEW_DATA = getNewYearData()

        # --- processing
        if CHOICE == 1:
            pass
        elif CHOICE == 2:
            insertData(NEW_DATA)

        # --- outputs
        if CHOICE == 1:
            pass
        elif CHOICE == 2:
            print(f"Successfully added {NEW_DATA[1]} data.")
        elif CHOICE == 3:
            print("Goodbye!")
            exit()

# check ability to exclude newly added data --> without affecting previous data calculations?
