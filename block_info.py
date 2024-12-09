import os
from data_analysis import load_df
from clearsky import ClearSkyAPI

# Modifies df in place
def add_column(df, new_column_name, column_name, function):
    def safe_apply(value):
        try:
            return function(value)
        except Exception as e:
            print(f"Error processing value {value}: {e}")
            return -1

    df[new_column_name] = df[column_name].apply(safe_apply)

def process_files_in_directory(input_directory, output_directory, api):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file_path = os.path.join(input_directory, filename)
            print(f"Processing file: {filename}")
            df = load_df(input_file_path)

            # Add the new column
            add_column(df, "total_blocked_by", "handle", api.get_total_blocked_by)

            # Save to new file in the output directory
            new_filename = filename.replace('.csv', '_with_blocks.csv')
            output_file_path = os.path.join(output_directory, new_filename)
            df.to_csv(output_file_path, index=False)
            print(f"Saved modified file to: {output_file_path}")

def main():
    input_directory = './datasets/'
    output_directory = './datasets/block_datasets/'
    api = ClearSkyAPI()
    process_files_in_directory(input_directory, output_directory, api)

if __name__ == "__main__":
    main()
