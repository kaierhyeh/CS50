import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: dna.py [database.csv] [sequence.txt]")
        return

    # TODO: Read database file into a variable
    database = []								# []: Store as a list
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)
    """
    DictReader by default takes the first line of the file as the header,
    the format to assign the fieldnames.

    The database stores one row, ie. one dictionary, at a time.
    Here, each dictionary happens to represent only one person,
    with different “indices” (keys) for different STR columns.
    """

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        sequence = file.read().strip()

    # TODO: Find longest match of each STR in DNA sequence
    str_list = list(database[0].keys())[1:]		# Skip "name"
    count = {}
    """
    Store as a dict, {}.

    A dictionary is like a list (array) where:
        Instead of positions (0, 1, 2 …),
        You can use custom keys (like "name", "age", "score") to access data.
    A dict is like an array, but the “indices” (called keys) can be
    any unique labels instead of just numbers.
    """
    for str_name in str_list:
        count[str_name] = longest_match(sequence, str_name)

    # TODO: Check database for matching profiles
    for person in database:
        match = True
        # print("Checking", person["name"], "against", count)
        for str_name in str_list:
            # print(f"{person['name']}[{str_name}] = {person[str_name]}")
            if int(person[str_name]) != count[str_name]:
                match = False					# Need int() cuz csv reads everything as string
                break
        if match == True:
            print(person['name'])
            return
    print("No match")
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
