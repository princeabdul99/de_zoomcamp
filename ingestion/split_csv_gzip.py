import os
import csv
import gzip
from datetime import datetime

def split_csv_stream_gz(filename, date_column_name, output_filename="output_filename", output_folder="output"):
    print(f"[OK] Processing '{filename}' using date column '{date_column_name}'")

    os.makedirs(output_folder, exist_ok=True)
    file_handles = {}  # { "2021-01": (file_obj, writer) }

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        for row in reader:
            date_str = row[date_column_name].strip()
            date_value = datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")
            year_month = date_value.strftime("%Y-%m")

            if year_month not in file_handles:
                output_path = os.path.join(output_folder, f"{output_filename}-{year_month}.csv.gz")
                gzfile = gzip.open(output_path, "wt", newline="", encoding="utf-8")
                writer = csv.DictWriter(gzfile, fieldnames=header)
                writer.writeheader()
                file_handles[year_month] = (gzfile, writer)

                print(f"[OK] Created gzipped output file: {output_path}")

            file_handles[year_month][1].writerow(row)

    # Close all gzip files
    for gzfile, _ in file_handles.values():
        gzfile.close()

    print("[DONE] Splitting and gzipping completed.")

if __name__ == "__main__":
    # Example usage — you can modify these values
    split_csv_stream_gz(
        filename="D:/dataset/green-and-yellow-taxi/Yellow_Taxi_Trip_Data_2023.csv", 
        date_column_name="tpep_pickup_datetime",
        output_folder="D:/dataset/yellow-taxi/2023",
        output_filename="yellow-taxi-tripdata"
    )