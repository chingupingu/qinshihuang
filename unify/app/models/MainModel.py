import json
from .PDFModel import PDFModel
from .CSVModel import CSVModel
from .JSONModel import JSONModel
from .PPTXModel import PPTXModel

class MainModel:
    def __init__(self, input_paths):
        self.input_paths = [input_paths] if isinstance(input_paths, str) else input_paths
        self.file_types = {path: self.detect_file_type(path) for path in self.input_paths}
        self.unified_json = self.unify_to_json()

    def detect_file_type(self, path):
        if path.endswith('.pdf'):
            return 'pdf'
        elif path.endswith('.pptx'):
            return 'pptx'
        elif path.endswith('.csv'):
            return 'csv'
        elif path.endswith('.json'):
            return 'json'
        else:
            raise ValueError(f"Unsupported file type: {path}")
        
    def unify_to_json(self):
        try:
            json_results = []
            for path in self.input_paths:
                if self.file_types[path] == 'pdf':
                    pdf_model = PDFModel(path)
                    json_results.append(json.loads(pdf_model.get_json()))
                elif self.file_types[path] == 'csv':
                    csv_model = CSVModel(path)
                    json_results.append(json.loads(csv_model.get_json()))
                elif self.file_types[path] == 'json':
                    json_model = JSONModel(path)
                    json_results.append(json.loads(json_model.get_json()))
                elif self.file_types[path] == 'pptx':
                    pptx_model = PPTXModel(path)
                    json_results.append(json.loads(pptx_model.get_json()))
            return json.dumps(json_results)
        
        except Exception as e:
            return json.dumps({
                "error": f"Failed to ingest inputs: {str(e)}"
            })
        
# ignore this

    # def convert_to_file(self, file_type):
    #     if file_type == 'pdf':
    #         pdf_model = PDFModel(self.unified_json)
    #         return pdf_model.get_pdf()
    #     elif file_type == 'pptx':
    #         pptx_model = PPTXModel(self.unified_json)
    #         return pptx_model.get_pptx()
    #     elif file_type == 'csv':
    #         csv_model = CSVModel(self.unified_json)
    #         return csv_model.get_csv()
    #     elif file_type == 'json':
    #         json_model = JSONModel(self.unified_json)
    #         return json_model.get_json()
    
    
    