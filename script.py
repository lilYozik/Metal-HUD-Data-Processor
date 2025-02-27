import csv
import os
import argparse
import numpy as np

# Function to process a single line of the metal-HUD data and return rows for the CSV
def process_line(metal_hud_str):
    # Remove the "<random-timestamp>" part and "metal-HUD:"
    cleaned_str = metal_hud_str.split("metal-HUD:")[1].strip()
    data_values = cleaned_str.split(',')

    # Extract the fixed part of the data (first frame number, frame misses, and memory usage)
    frame_number = int(data_values[0])  # Convert frame_number to integer
    frame_misses = data_values[1]
    memory_usage = data_values[2]

    # Extract dynamic part of the data (pairs of frame-present-interval-float, frame-gpu-time-float)
    intervals_and_gpu_times = data_values[3:]

    # Create pairs of frame-present-interval-float and frame-gpu-time-float
    interval_gpu_pairs = []
    for i in range(0, len(intervals_and_gpu_times), 2):
        interval_gpu_pairs.append((intervals_and_gpu_times[i], intervals_and_gpu_times[i + 1]))

    # Prepare a list of rows to return for the CSV
    data_rows = []
    fps_values = []  # List to store FPS values for summary statistics
    for i, (interval, gpu_time) in enumerate(interval_gpu_pairs):
        # Convert Frame Present Interval (in milliseconds) to FPS (frames per second)
        fps = 1000 / float(interval) if float(interval) > 0 else 0  # Avoid division by zero
        fps_values.append(fps)
        
        # For the first row, include Frame Misses and Memory Usage
        if i == 0:
            data_rows.append([frame_number, frame_misses, memory_usage, interval, gpu_time])
        else:
            # For subsequent rows, exclude Frame Misses and Memory Usage
            data_rows.append([frame_number + i, "", "", interval, gpu_time])
    
    return data_rows, fps_values

# Calculate summary statistics from FPS values
def calculate_summary_statistics(fps_values):
    min_fps = min(fps_values)
    avg_fps = np.mean(fps_values)
    max_fps = max(fps_values)
    percentile_1 = np.percentile(fps_values, 1)
    percentile_5 = np.percentile(fps_values, 5)
    
    return {
        "Min FPS": min_fps,
        "Avg FPS": avg_fps,
        "Max FPS": max_fps,
        "1 Percentile FPS": percentile_1,
        "5 Percentile FPS": percentile_5
    }

# Write the summary to a CSV file
def write_summary_file(summary, input_filename):
    # Get the base name of the input file (without extension)
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    
    # Construct the summary file name
    summary_filename = f"{base_name}_summary.csv"

    with open(summary_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metric", "Value"])
        for key, value in summary.items():
            writer.writerow([key, value])

    print(f"Summary file '{summary_filename}' created successfully.")

# Function to check for missing frame numbers and print a warning if there are any
def check_missing_frame_numbers(all_frame_numbers):
    expected_frame_numbers = set(range(min(all_frame_numbers), max(all_frame_numbers) + 1))
    missing_frame_numbers = expected_frame_numbers - set(all_frame_numbers)
    if missing_frame_numbers:
        print(f"WARNING: Missing frames: {sorted(missing_frame_numbers)}")

# Function to check for frame number overlap and print a warning if there are any
def check_frame_overlap(all_frame_numbers):
    frame_count = {}
    for frame in all_frame_numbers:
        if frame in frame_count:
            frame_count[frame] += 1
        else:
            frame_count[frame] = 1
    
    overlapping_frames = [frame for frame, count in frame_count.items() if count > 1]
    if overlapping_frames:
        print(f"WARNING: Overlapping frames: {sorted(overlapping_frames)}")

# Read the file and process all lines
def process_file(input_filename):
    # Get the base name of the input file (without extension)
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    
    # Construct the output file name
    output_filename = f"{base_name}_output.csv"
    all_fps_values = []  # List to store all FPS values across all lines
    all_frame_numbers = []  # List to store all frame numbers for missing and overlap check

    with open(input_filename, 'r') as infile:
        # Read all lines from the file
        lines = infile.readlines()

        # Open the CSV file for writing
        with open(output_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header to the CSV
            writer.writerow(["Frame Number", "Frame Misses", "Memory Usage", "Frame Present Interval", "Frame GPU Time"])

            # Process each line and write the data to the CSV
            for line in lines:
                line = line.strip()
                if "metal-HUD" in line:  # Ensure we only process lines with "metal-HUD"
                    data_rows, fps_values = process_line(line)
                    all_fps_values.extend(fps_values)  # Accumulate FPS values for summary
                    for row in data_rows:
                        writer.writerow(row)
                        all_frame_numbers.append(row[0])  # Collect frame numbers for missing and overlap check

    # Check if any frame numbers are missing
    check_missing_frame_numbers(all_frame_numbers)

    # Check if any frame numbers overlap
    check_frame_overlap(all_frame_numbers)

    # Calculate the summary statistics
    summary = calculate_summary_statistics(all_fps_values)
    
    # Write the summary to a CSV file
    write_summary_file(summary, input_filename)

    print(f"CSV file '{output_filename}' created successfully.")

# Main function to handle command-line arguments
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process metal-HUD data into CSV format.")
    parser.add_argument('input_filename', type=str, help="Input file containing metal-HUD data")
    args = parser.parse_args()

    # Process the file using the input filename from the command-line argument
    process_file(args.input_filename)

if __name__ == "__main__":
    main()
