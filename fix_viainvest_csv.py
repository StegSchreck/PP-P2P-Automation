import csv
import sys


def main(input_file: str, output_file: str):
  """
  Moves the value from column 7 to column 6 if it's not empty.

  Args:
    input_file: The path to the input CSV file.
    output_file: The path to the output CSV file.
  """

  with open(input_file, 'r', newline='', encoding="UTF-8") as infile, open(output_file, 'w', newline='', encoding="UTF-8") as outfile:
      reader = csv.reader(infile)
      writer = csv.writer(outfile)
      _ = next(reader)  # ignore broken header row

      writer.writerow(["Transaction date","Transaction type","Description","Underlying LO","ISIN","Credit (€)","Debit (€)"])
      for row in reader:
          if not row[5]:
              # Column 7 is not empty, so move its value to column 6 and remove it
              row[5] = row[6]
              row[6] = ''
          writer.writerow(row)

if __name__ == '__main__':
    main(input_file=sys.argv[1], output_file=sys.argv[2])
