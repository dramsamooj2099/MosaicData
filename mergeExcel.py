import sys
import os
import csv
import glob

# Get the input file paths from the command line arguments
input_file_1 = sys.argv[1]
input_file_2 = sys.argv[2]

# Extract the folder names from the input file paths
folder_1 = input_file_1.split("\\")
folder_2 = input_file_2.split("\\")

# Create the output file path by combining the two folder names and adding a file extension
output_file_path = folder_1[0] + "_" + folder_2[0] + ".csv"
if os.path.exists(output_file_path):
    os.remove(output_file_path)
if os.path.exists("temp.csv"):
    os.remove("temp.csv")

    

# Define the headers for the output CSV file
headers = [
    'Date and Time',
    ' ',
    'V2X Message Detail',
    'Sender',
    'Receiver',
    'Message Type',
    'Msg Id',
    'Seq Num',
    'Latitude - Sender',
    'Longitude - Sender',
    'Message Content',
    'Latitude - Receiver',
    'Longitude - Receiver',
    'Simulation Time - Sender',
    ' ',
    'Simulation Time - Receiver',
    ' ',
]

# Read in the data from the input files
with open(input_file_1, 'r') as f1, open(input_file_2, 'r') as f2, open('temp.csv', 'w+', newline='') as outfile:
    reader1 = csv.reader(f1)
    reader2 = csv.reader(f2)
    writer = csv.writer(outfile)

    # Write the contents of the input files to the output file
    for row in reader1:
        writer.writerow(row)
    for row in reader2:
        writer.writerow(row)

# Open the input CSV file and read its contents
with open('temp.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    rows = list(reader)

# Delete rows that do not have 13 columns
for row in rows[:]:
    if len(row) < 13:
        rows.remove(row)

matching_rows = []
# Define a function to determine if a row has a matching pair based on column 7
#row: Broadcast
#other_row:Received
def has_matching_pair(row, rows):
    addrow = [None] * len(headers)
    for other_row in rows:
        if row is other_row:
            continue
        if row[6] == other_row[6] and row[5] == other_row[5]:
            addrow[0] = row[0] #Date and Time
            addrow[1] = row[1] #Empty
            addrow[2] = row[2] #V2X Message Detail
            addrow[3] = row[3] #Sender
            if other_row[3] == folder_1[0]:
                addrow[4] = folder_2[0] #Receiver
            else: 
                addrow[4] = folder_1[0]
            addrow[5] = row[4] #Message Type
            addrow[6] = row[5] #Msg Id
            addrow[7] = row[6] #Seq Num
            addrow[8] = row[7] #Latitude - Sender
            addrow[9] = row[8] #Longitude - Sender
            addrow[10] = row[9] #Message Content
            addrow[11] = other_row[11] #Latitude - Receiver
            addrow[12] = other_row[12] #Longitude - Receiver
            addrow[13] = row[10] #Simulation Time - Sender
            addrow[14] = row[11] #Simulation Time - Sender
            addrow[15] = other_row[13] #Simulation Time - Receiver
            addrow[16] = other_row[14] #Simulation Time - Receiver





            matching_rows.append(addrow)
            return True
    return False


for row in rows:
    if "Received" in row[2]:
        continue
    has_matching_pair(row, rows)
        

# Open the output CSV file and write the matching rows and headers to it
with open(output_file_path, 'w+', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(headers)
    writer.writerows(matching_rows)
