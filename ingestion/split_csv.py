import os
import csv
from datetime import datetime

def split_csv_stream(filename, date_column_name, output_filename="output_filename", output_folder="output"):
    print(f"[OK] Processing '{filename}' using date column '{date_column_name}'")

    # Create output folder if missing
    os.makedirs(output_folder, exist_ok=True)

    file_handles = {}  # { "2021-01": (file, writer) }

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        for row in reader:
            # Parse the date (change format here if needed)
            date_str = row[date_column_name].strip()
            date_value = datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")

            year_month = date_value.strftime("%m-%Y")

            # Create CSV for month if not already opened
            if year_month not in file_handles:
                output_path = os.path.join(output_folder, f"{output_filename}-{year_month}.csv")
                csvfile = open(output_path, "w", newline="", encoding="utf-8")
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                file_handles[year_month] = (csvfile, writer)

                print(f"[OK] Created output file: {output_path}")

            # Write current row immediately
            file_handles[year_month][1].writerow(row)

    # Close all open files
    for csvfile, _ in file_handles.values():
        csvfile.close()

    print("[DONE] Splitting completed with streaming output.")


if __name__ == "__main__":
    # Example usage — you can modify these values
    split_csv_stream(
        filename="D:/dataset/green-and-yellow-taxi/Green_Taxi_Trip_Data_2021.csv", 
        date_column_name="tpep_pickup_datetime",
        output_folder="D:/dataset/2021-green-taxi",
        output_filename="green-taxi-tripdata"
    )
 