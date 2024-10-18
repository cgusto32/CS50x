import csv
import sys


def longest_match(sequence, subsequence):
    """Returns length of longest run of `subsequence` in `sequence`."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0

        # Instead of a while loop, using a manual loop with a flag to break out (not optimal)
        keep_counting = True
        while keep_counting:
            start = i + count * subsequence_length
            end = start + subsequence_length

            # Check if the subsequence matches
            if sequence[start:end] == subsequence:
                count += 1
            else:
                keep_counting = False

        # Compare current count with the longest one found so far
        if count > longest_run:
            longest_run = count

    return longest_run


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 3:
        print("Error: You need to provide both a CSV file and a DNA sequence file.")
        return
    elif len(sys.argv) > 3:
        print("Error: Too many arguments provided.")
        return

    # Open and read the CSV file
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        people = []
        for row in reader:
            people.append(row)

    # Open and read the DNA sequence file
    with open(sys.argv[2], "r") as file:
        dna_sequence = ""
        for line in file:
            dna_sequence += line.strip()  # Strip and concatenate lines manually

    # Get STR sequences from the header row of the CSV file
    str_sequences = []
    for header in reader.fieldnames:
        if header != "name":
            str_sequences.append(header)

    # Create a dictionary to store the counts of STRs
    str_counts = {}
    for str_seq in str_sequences:
        # Calculate the longest match for each STR
        str_counts[str_seq] = longest_match(dna_sequence, str_seq)

    # Try to find a matching person
    found_match = False
    for person in people:
        match = True
        for str_seq in str_sequences:
            # Compare each STR count
            if int(person[str_seq]) != str_counts[str_seq]:
                match = False
                break

        if match:
            print(person["name"])
            found_match = True
            break  # Break out of the loop as soon as a match is found

    # If no match was found
    if not found_match:
        print("No match")


if __name__ == "__main__":
    main()
