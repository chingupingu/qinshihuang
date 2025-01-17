import json

class JSONModel:
    def __init__(self, input_path):
        self.input_path = input_path
        self.title = None
        self.data = None
        self.json_output = None

    ######################
    ### MAIN FUNCTIONS ###
    ######################

    def get_json(self):
        if self.json_output is None:
            self.load_and_validate_json()
        return self.json_output
    
    ########################
    ### HELPER FUNCTIONS ###
    ########################

    def load_and_validate_json(self):
        try:
            with open(self.input_path, 'r') as file:
                self.data = json.load(file)
                self.json_output = self.data
            return True
        
        except FileNotFoundError:
            print(f"Error: File not found at {self.input_path}")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.input_path}")
            return False
