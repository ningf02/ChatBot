def sort_id(input_file_path, output_file_path):
    # Dictionary to store the highest value in column 5 for each unique value in column 4
    highest_values = {}

    # Open the original CSV file for reading
    with open(input_file_path, 'r', newline='', encoding="latin-1") as input_file:
        # Open the new CSV file for writing
        with open(output_file_path, 'w', newline='', encoding="latin-1") as output_file:
            # Create CSV reader and writer objects
            csv_reader = csv.reader(input_file)
            csv_writer = csv.writer(output_file)

            # Write the header to the output file
            header = next(csv_reader)
            csv_writer.writerow(header)

            # Iterate through each row in the input file
            for row in csv_reader:
                column4_value = row[1]  # Value in column 4
                column5_value = float(row[2])  # Value in column 5

                # Check if column4_value is already in highest_values dictionary
                if column4_value in highest_values:
                    # Update the value in highest_values dictionary if the current value is higher
                    if column5_value > highest_values[column4_value]:
                        highest_values[column4_value] = column5_value
                else:
                    # If column4_value is not in highest_values dictionary, add it with the current value
                    highest_values[column4_value] = column5_value

            # Write rows to the output file, only storing the highest value for each unique value in column 4
            input_file.seek(0)  # Reset the file pointer to read from the beginning
            next(csv_reader)  # Skip header
            for row in csv_reader:
                column4_value = row[1]  # Value in column 4
                column5_value = float(row[2])  # Value in column 5

                # Write the row to the output file only if the value in column 5 is the highest for the corresponding
                # value in column 4
                if column5_value == highest_values[column4_value]:
                    csv_writer.writerow(row)
