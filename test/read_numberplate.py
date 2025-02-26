from JsonFileFactory import JsonFileFactory
from RecordingNumberPlate import RecordingNumberPlate

# Initialize JsonFileFactory
jff = JsonFileFactory()

# Define the path to the JSON file
filename = "../dataset/car_plate_data.json"

# Read the data from the JSON file
plate_records = jff.read_data(filename, RecordingNumberPlate)

# Display the data
if len(plate_records) == 0:
    print("No number plates found.")
else:
    print(f"{'Number Plate':<20}{'Date':<15}{'Time':<10}")
    print("=" * 45)
    for record in plate_records:
        print(f"{record.numberplate:<20}{record.date:<15}{record.time:<10}")
