import csv
import sys

#def load_data(database_ldf):
#    dbfile_ldf = csv.DictReader(open(database_ldf))
#    headers_ldf = dbfile_ldf.fieldnames
#    return dbfile_ldf, headers_ldf



def main():

    if len(sys.argv) != 3:
        print("Bad command-line arguments")
        sys.exit(1)
    database = sys.argv[1]
    perp_file = "sequences/" + sys.argv[2]


    with open(perp_file, 'r') as f:
        perp = f.read()
#    dbfile, headers = load_data(database)


    with open(database) as file:
        database = csv.DictReader(file)
        for row in database:
            name = row[headers[0]]
            print(name)
 #           telephone = row[headers[1]]
 #           print(telephone)
 #           email = row[headers[2]]
 #           print(email)

    list1 = {"a1", "b2", "c3"}
    list2 = {"a1", "b2", "c4"}

    if list1 == list2:
        print("whoopee")
    else:
        print("fuck")





main()


#ddb
#Not quite. Each row represents a single person's data. For example, if you have a CSV with columns
#   Name, Telephone, and Email, you would access each person's data like this:
#
#import csv
#
#with open(filename) as file:
#    input_file = csv.DictReader(file)
#    for row in input_file:
#        name = row['Name']
#        telephone = row['Telephone']
#        email = row['Email']
#        # Do something with name, telephone, and email
#In this example, name, telephone, and email will contain the data for the current person in the
#   iteration. Each iteration of the loop processes one row (one person's data).

#headers = ['name', 'telephone', 'email']
#print(headers[0])  # Output: name
#print(headers[1])  # Output: telephone
#print(headers[2])  # Output: email
