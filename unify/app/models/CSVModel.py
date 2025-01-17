import csv
import json
from flask import send_file

class CSVModel:
    def __init__(self, input_path):
        self.input_path = input_path
        self.title = None
        self.headers = None
        self.data = None
        self.json_output = None

    ######################
    ### MAIN FUNCTIONS ###
    ######################

    # these are the functions that are called by the handler

    ### 1. Return CSV as json ###
    def get_json(self):
        self.read_csv()
        return self.json_output

    ### 2. Return json as CSV ###
    def get_csv(self):
        try:
            json_data = json.loads(self.json_output)
            data_rows = json_data[self.title]

            # Create CSV content
            csv_content = ",".join(self.headers) + "\n"

            for row in data_rows:
                row_content = ",".join(str(row[header]) for header in self.headers)
                csv_content += row_content + "\n"

            return csv_content
        
        except Exception as e:
            raise Exception(f"Error generating CSV: {str(e)}")

    ########################
    ### HELPER FUNCTIONS ###
    ########################

    ### PPTX reading ###
    # reads the PPTX and updates self.content
    def read_csv(self):
        try:
            with open(self.input_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                self.title = self.input_path.split('/')[-1].rsplit('.', 1)[0]
                self.headers = csv_reader.fieldnames
                
                # Process each row and replace None or missing values with empty string
                self.data = []
                for row in csv_reader:
                    processed_row = {key: (value if value is not None else "") for key, value in row.items()}
                    self.data.append(processed_row)
                
                self.json_output = json.dumps({
                    self.title: self.data
                })
        except FileNotFoundError:
            raise Exception(f"CSV file not found at {self.input_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")