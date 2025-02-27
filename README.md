# Metal-HUD-Data-Processor

This Python script processes `metal-HUD` data from a text file, extracting key information and outputting it into two CSV files:
1. **Data Output**: A CSV file with detailed information about frame numbers, misses, memory usage, frame present interval, and GPU time.
2. **Summary**: A CSV file with summary statistics calculated from the Frame Present Interval values, including Min FPS, Avg FPS, Max FPS, 1 Percentile FPS, and 5 Percentile FPS.

## Requirements

- Python 3.x
- **numpy** library

## Usage

1. **Prepare your `metal-HUD` data file:** Your input file should have lines in the following format:
   ```bash
   <timestamp> metal-HUD: <frame-number>,<frame-misses>,<memory-usage>,<frame-present-interval-1>,<frame-gpu-time-1>,<frame-present-interval-2>,<frame-gpu-time-2>,..
   
2. **Run the script:** To process the data, simply run the script with your input filename:
   ```bash
   python3 script.py your_input_file.txt
3. **Output:**

- `<input_filename>_output.csv`: A CSV file containing the processed data with the following columns:
  - Frame Number
  - Frame Misses
  - Memory Usage
  - Frame Present Interval
  - Frame GPU Time
- `<input_filename>_summary.csv`: A CSV file containing the following summary statistics:
  - Min FPS
  - Avg FPS
  - Max FPS
  - 1 Percentile FPS
  - 5 Percentile FPS

  The output filenames are based on the input filename, with `_output.csv` and `_summary.csv` appended to the name.

   
