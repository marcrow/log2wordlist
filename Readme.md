# log2wordlist

## Description
This Python script processes Nginx log files to extract all requested endpoints. It removes duplicates, sorts the results, and saves them to a specified file. Additionally, it allows merging the extracted endpoints with an existing list if desired. The script also maintains a statistics file to track the number of occurrences for each endpoint and provides options to display the most frequent ones.

A supplementary script, `merge.py`, is also provided to merge multiple statistics or wordlist files into a unified output file.

I use it on my honeypot servers to generate wordlists based on bot sollicitations. I'm sure you can use it for something else like website statistic.

## Features
- Extracts requested endpoints from Nginx log files.
- Removes duplicate endpoints.
- Sorts the endpoints alphabetically.
- Merges extracted endpoints with an existing list.
- Outputs the final list to a file.
- Tracks the occurrences of each endpoint in a statistics file.
- Displays the top N most frequent endpoints from the statistics file.
- Merges multiple wordlists or statistics files into one.

## Requirements
- Python 3.x

## Usage

Tips: if you have log rotate use this command to extract gz content to a single file: 
```bash
find /var/log/nginx -name "*.gz" -exec gunzip -c {} + > concatenated_logs.log
```
Then, if it's ok on your server you can delete these logs, to avoid to rerun the script on the same files.

Run the scripts using the command line with the following options:

### `log2wordlist.py` Command-line Options
- `-i, --input`: Path to the Nginx log file to process.
- `-o, --output`: Path to save the output file containing the endpoints.
- `-n, --no-count`: Disable counting occurrences of endpoints.
- `-s, --stats`: Display the top N endpoints from the statistics file.
- `-c, --count-file`: Specify an alternate statistics file (default: `results/stats.txt`).

#### Example Commands for `log2wordlist.py`
##### Basic Usage
```bash
python log2wordlist.py -i /path/to/nginx.log -o endpoints.txt
```

Will save the new wordlist "endpoints.txt" and generate a stats.txt file with 2 columns. 
The first one for the word, the secund for the number of occurences.

##### Merge with an Existing List
```bash
python log2wordlist.py -i /path/to/nginx.log -o endpoints.txt -e
```

##### Disable Counting
```bash
python log2wordlist.py -i /path/to/nginx.log -o endpoints.txt -n
```

##### Display the Top 5 Most Frequent Endpoints
```bash
python log2wordlist.py -s 5
```

##### Display all sorted statistic
```bash
python log2wordlist.py -s 0
```

##### Specify an Alternate Statistics File
```bash
python log2wordlist.py -i /path/to/nginx.log -o endpoints.txt -c custom_stats.txt
```

```bash
python log2wordlist.py -c custom_stats.txt -s 0
```

### `merge.py` Command-line Options
- `-o, --output`: Path to save the merged file.
- `-t, --type`: Type of files to merge: `wordlist` or `stats`.
- `input_files`: List of input files to merge.

#### Example Commands for `merge.py`
##### Merge Wordlists
```bash
python merge.py -o merged_wordlist.txt -t wordlist wordlist1.txt wordlist2.txt
```

##### Merge Statistics Files
```bash
python merge.py -o merged_stats.txt -t stats stats1.txt stats2.txt
```

## How It Works
1. **Input Parsing**:
   - The script reads the provided log file and extracts endpoints based on the standard Nginx log format.
2. **Save Output**:
   - The script writes the final, sorted, and deduplicated list of endpoints to the output file.
3. **Count Tracking**:
   - By default, the script updates a statistics file (`results/stats.txt`) with the occurrences of each endpoint. This can be disabled with the `-n` flag.
4. **Statistics Display**:
   - Use the `-s` option to display the top N most frequent endpoints from the statistics file. You can specify an alternate statistics file with the `-c` option.
5. **File Merging**:
   - The `merge.py` script allows combining multiple wordlists or statistics files into one. Wordlists are deduplicated, and statistics are aggregated.

## Error Handling
- If the input file does not exist, an error message is displayed.
- If the output file does not exist while using the `-e` flag, it warns and skips the merge process.
- If the statistics file is missing when using the `-s` option, an error is displayed.
- The `merge.py` script skips missing files and warns about malformed lines in statistics files.

## Example Nginx Log Format
The script assumes the following standard Nginx log format:
```
<IP_ADDRESS> - - [<DATE>] "<METHOD> <ENDPOINT> HTTP/<VERSION>" <STATUS_CODE> <BYTES>
```
For example:
```
127.0.0.1 - - [21/Jan/2025:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 512
```
In this case, the endpoint extracted would be `/index.html`.

## Notes
- The script processes log files line by line to handle large files efficiently.
- The output is always sorted and deduplicated, ensuring a clean result.


