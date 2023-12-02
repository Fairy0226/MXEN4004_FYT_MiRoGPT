import csv
import re
from Levenshtein import distance

# read csv and evalute the performance
with open('data1-100.csv', 'r') as file:
    reader = csv.DictReader(file)

    # create csv, make a new column
    with open('data_with_distance.csv', 'w', newline='') as new_file:
        fieldnames = reader.fieldnames + ['edit_distance']
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()

    \
        for row in reader:
            model = row['model']
            filename = row['filename']
            translated_text = row['translated_text']
            source_text = row['source_text']
            delay = float(row['delay'])

            # pre-edit the text for evaluation, leave only words and digits
            translated_text = translated_text.lower().strip()
            source_text = source_text.lower().strip()
            translated_text = re.sub(r'[^\w\s]', '', translated_text)
            source_text = re.sub(r'[^\w\s]', '', source_text)

            # change sentence to list
            translated_words = translated_text.split()
            source_words = source_text.split()

            # calculate edit distance
            edit_dist = distance(translated_words, source_words)
            # write to new column
            row['edit_distance'] = edit_dist

            # write to csv
            writer.writerow(row)
