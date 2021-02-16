import re
import csv

with open('locations.list', encoding='latin1') as infile:
    lines = infile.readlines()[14:-1]

    for i in range(len(lines)):
        lines[i] = re.sub("\t+", "\t", lines[i]).strip()

    data = []

    for line in lines:
        line = line.split('\t')

        try:
            year = re.findall("\([0-9]+\)", line[0])[0]
            year = int(year[1:-1])
        except IndexError:
            continue

        title = re.sub('\(.*?\)', '', line[0]).strip()
        title = re.sub('{.*?}', '', title).strip()

        location = line[1]

        data.append((title, year, location))

with open('locations.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(data)
