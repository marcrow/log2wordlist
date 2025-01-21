import argparse
import os
from collections import Counter

def parse_nginx_log(file_path):
    """Parse the Nginx log file to extract endpoints."""
    endpoints = Counter()
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                parts = line.split()
                if len(parts) > 6:  # Assuming standard Nginx log format
                    endpoint = parts[6]
                    endpoints[endpoint] += 1
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
    return endpoints


def save_to_file(output_file, endpoints):
    """Append the sorted endpoints to a file and remove duplicates."""
    try:
        # Read existing content if the file exists
        existing_endpoints = set()
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                existing_endpoints = set(file.read().splitlines())

        # Merge and sort endpoints
        all_endpoints = existing_endpoints.union(endpoints.keys())
        with open(output_file, 'w') as file:
            for endpoint in sorted(all_endpoints):
                file.write(f"{endpoint}\n")
    except Exception as e:
        print(f"Error saving to file '{output_file}': {e}")


def save_endpoint_counts(count_file, endpoints):
    """Update the count file with the occurrences of each endpoint."""
    try:
        # Read existing counts if the file exists
        existing_counts = Counter()
        if os.path.exists(count_file):
            with open(count_file, 'r') as file:
                for line in file:
                    endpoint, count = line.rsplit(' ', 1)
                    existing_counts[endpoint] = int(count)

        # Update counts with new data
        existing_counts.update(endpoints)

        # Save updated counts
        with open(count_file, 'w') as file:
            for endpoint, count in existing_counts.items():
                file.write(f"{endpoint} {count}\n")
    except Exception as e:
        print(f"Error saving endpoint counts to file '{count_file}': {e}")


def display_top_stats(count_file, top_n):
    """Display the top N endpoints from the count file."""
    try:
        if os.path.exists(count_file):
            with open(count_file, 'r') as file:
                counts = Counter({line.rsplit(' ', 1)[0]: int(line.rsplit(' ', 1)[1]) for line in file})
                if top_n == 0:
                    for endpoint, count in counts.items():
                        print(f"{endpoint}: {count}")
                else:
                    for endpoint, count in counts.most_common(top_n):
                        print(f"{endpoint}: {count}")
        else:
            print(f"Error: Count file '{count_file}' not found.")
    except Exception as e:
        print(f"Error displaying stats from '{count_file}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Process Nginx log files to extract endpoints.")
    parser.add_argument('-i', '--input', help="Path to the Nginx log file.")
    parser.add_argument('-o', '--output', help="Path to save the output file.")
    parser.add_argument('-n', '--no-count', action='store_true', help="Disable counting occurrences of endpoints.")
    parser.add_argument('-s', '--stats', type=int, default=0, help="Display the top N endpoints from the statistics file.")
    parser.add_argument('-c', '--count-file', default="stats.txt", help="Specify an alternate statistics file.")

    args = parser.parse_args()

    count_file = args.count_file

    if args.stats or args.stats == 0:
        display_top_stats(count_file, args.stats)
        return

    if not args.input or not args.output:
        print("Error: -o and -i options are required to generate wordlist")
        print("Otherwise, use the -s to display current stats")
        return

    # Parse the log file
    endpoints = parse_nginx_log(args.input)

    # Merge with the output file if -e is set
    # if args.existing:
    #     try:
    #         if os.path.exists(args.output):
    #             with open(args.output, 'r') as existing_file:
    #                 existing_endpoints = set(existing_file.read().splitlines())
    #                 endpoints.update(Counter({endpoint: 1 for endpoint in existing_endpoints}))
    #     except FileNotFoundError:
    #         print(f"Warning: Output file '{args.output}' not found. Skipping merge.")

    # Save the final list of endpoints
    save_to_file(args.output, endpoints)

    # Save endpoint counts unless -n is set
    if not args.no_count:
        save_endpoint_counts(count_file, endpoints)

    print(f"Processed endpoints have been saved to '{args.output}'.")
    if not args.no_count:
        print(f"Endpoint counts have been saved to '{count_file}'.")


if __name__ == "__main__":
    main()
