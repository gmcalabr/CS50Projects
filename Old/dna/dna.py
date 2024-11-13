import csv
import sys

def main():

    if len(sys.argv) != 3:
        print("Bad command-line arguments")
        sys.exit(1)
    database = sys.argv[1]
    perp_file = sys.argv[2]


    # open files
    with open(perp_file, 'r') as f:
        perp = f.read()
    dbfile = csv.DictReader(open(database))
    headers = dbfile.fieldnames

    # do DNA Testing
    dna_test_results = []
    for i in range(len(headers)-1):
        dna_test_results.append(longest_match(perp, headers[i+1]))

    name = "No match"

    database_listing = []
    for row in dbfile:
        database_listing = []
        for i in range(len(headers)-1):
            database_listing.append(int(row[headers[i+1]]))
        if dna_test_results == database_listing:
            name = row["name"]
            break

    print(name)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
