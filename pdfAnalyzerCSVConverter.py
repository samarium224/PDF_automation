import csv
import re
from PyPDF2 import PdfReader

path = "prec1_2.pdf"

reader = PdfReader(path)

meta = reader.metadata
TOTALPAGE = len(reader.pages)

# functions

def export_data_to_csv(data, output_file="extracted_data.csv"):
    """
    Exports a dictionary of lists to a CSV file.

    Parameters:
        data (dict): The dictionary to export. Keys become column headers, and values are lists of column data.
        output_file (str): The name of the CSV file to create. Default is 'extracted_data.csv'.

    Returns:
        None
    """
    # Get the headers (keys of the dictionary)
    headers = list(data.keys())

    # Find the maximum number of rows
    max_rows = max(len(values) for values in data.values())

    # Normalize the lengths of all lists in data (fill with empty strings if necessary)
    normalized_data = {key: values + [""] * (max_rows - len(values)) for key, values in data.items()}

    # Write data to CSV
    with open(output_file, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header row
        # writer.writerow(headers)
        
        # Write each row of data
        for row_idx in range(max_rows):
            row = [normalized_data[key][row_idx] for key in headers]
            writer.writerow(row)

def ExtractNameFeatures(fullname):
    first_name = []
    last_name = []
    first_name_flag = False

    for word in fullname:
        if first_name_flag:
            first_name.append(word)
        else:    
            if word != ",":
                last_name.append(word)
            else:
                first_name_flag = True
    
    srtFN = "".join(first_name)
    srtLN = "".join(last_name)
    
    return srtFN, srtLN

def ExtractStreetNumberNameType(fulladdress):
    address = "".join(fulladdress).split()
    streetNum = address[0]
    streetName = address[1]
    try:
        streetType = address[2]
    except:
        streetType = " "

    return streetNum, streetName, streetType

def ExtractCityStateZip(city):
    fullcity = "".join(city).split()
    city = fullcity[0]
    state = fullcity[1]
    zip_ = fullcity[2]

    return city,state,zip_

def extract_age_and_gender(input_str):
    # Regular expression to match age (numbers) and gender (M/F)
    pattern = r"(\d+)([MFU])"
    
    # Search the string using the regular expression
    match = re.search(pattern, input_str)
    
    if match:
        # Extract age and gender from the match
        age = int(match.group(1))
        gender = match.group(2)
        return age, gender
    else:
        # Return None if no match is found
        return "None", "None"



for index in range(0, TOTALPAGE):
    # public variables
    name = []
    age = []
    GlobalPatternIdentity = []
    word = []
    words = []  # To store all words from the page
    name_recorder_writer_flag = False
    age_recorder_flag = False
    preferred_recorder_flag = False
    cell_recorder_flag = False
    address_recorder_flag = False
    city_recorder_flag = False

    # Extracted data storage
    data = {
        "Name": [],
        "First Name": [],
        "Last Name": [],
        "Preferred": [],
        "Cell": [],
        "AgeGender": [],
        "Age": [],
        "Gender": [],
        "StreetNumber": [],
        "StreetName": [],
        "StreetType": [],
        "FullCity": [],
        "City": [],
        "State": [],
        "Zip": [],
        "FullAddress": [],
    }
    page = reader.pages[index]

    for i in page.extract_text():
        if name_recorder_writer_flag:
            if i != "❏":
                name.append(i)
                continue
            else:
                tempName = "".join(name)
                data["Name"].append(tempName)
                name = []
                name_recorder_writer_flag = False
        elif age_recorder_flag:
            if i != "❏":
                age.append(i)
                continue
            else:
                tempAge = "".join(age)
                data["AgeGender"].append(tempAge)
                age = []
                age_recorder_flag = False
        elif preferred_recorder_flag:
            if i != "❏":
                GlobalPatternIdentity.append(i)
                continue
            else:
                tempAge = "".join(GlobalPatternIdentity)
                data["Preferred"].append(tempAge)
                GlobalPatternIdentity = []
                preferred_recorder_flag = False
        elif cell_recorder_flag:
            if i != "❏":
                GlobalPatternIdentity.append(i)
                continue
            else:
                tempAge = "".join(GlobalPatternIdentity)
                data["Cell"].append(tempAge)
                GlobalPatternIdentity = []
                cell_recorder_flag = False
        elif address_recorder_flag:
            if i != "❏":
                GlobalPatternIdentity.append(i)
                continue
            else:
                tempAge = "".join(GlobalPatternIdentity)
                data["FullAddress"].append(tempAge)
                GlobalPatternIdentity = []
                address_recorder_flag = False
        elif city_recorder_flag:
            if i != "❏":
                GlobalPatternIdentity.append(i)
                continue
            else:
                tempAge = "".join(GlobalPatternIdentity)
                data["FullCity"].append(tempAge)
                GlobalPatternIdentity = []
                city_recorder_flag = False
        

        elif i != " " and i != "\n":
            word.append(i)
        else:
            if word: 
                complete_word = "".join(word)  # Join characters to form the word
                # print(complete_word)

                # a pattern is detected. need to record the next data
                if complete_word == "Issue/Notes":
                    name_recorder_writer_flag = True
                if complete_word == "❏Yes":
                    age_recorder_flag = True
                if complete_word == "Preferred:":
                    preferred_recorder_flag = True
                if complete_word == "Cell:":
                    cell_recorder_flag = True
                if complete_word == "❏Later":
                    address_recorder_flag = True
                if complete_word == "❏Unsure":
                    city_recorder_flag = True

                words.append(complete_word)  # Add it to the words list
                word = []  # Reset the word list for the next word


    for name in data["Name"]:
        firstName, LastName = ExtractNameFeatures(name)
        data["First Name"].append(firstName)
        data["Last Name"].append(LastName)

    for item in data["FullAddress"]:
        st_num, st_name, st_type = ExtractStreetNumberNameType(item)
        data["StreetNumber"].append(st_num)
        data["StreetName"].append(st_name)
        data["StreetType"].append(st_type)

    for item in data["FullCity"]:
        city, state, zip_ = ExtractCityStateZip(item)
        data["City"].append(city)
        data["State"].append(state)
        data["Zip"].append(zip_)
    
    for item in data["AgeGender"]:
        age, gender = extract_age_and_gender(item)
        data["Age"].append(age)
        data["Gender"].append(gender)


    print(f"page {index} completed successfully")
    export_data_to_csv(data)