from flask import Flask, send_file, jsonify, request, render_template
from models.MainModel import MainModel
import os
def register_routes(app):

    @app.route('/')
    def upload_page():
        return render_template('index.html')

    @app.route('/api/data/files', methods=['GET'])
    def list_files():
        try:
            input_folder = "inputs"
            files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
            return jsonify(files)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/data/files/<string:filename>', methods=['DELETE'])
    def delete_file(filename):
        try:
            input_folder = "inputs"
            file_path = os.path.join(input_folder, filename)
            
            # Check if file exists and is within the inputs folder
            if not os.path.exists(file_path) or not os.path.commonpath([file_path, input_folder]) == input_folder:
                return jsonify({"error": "File not found"}), 404
            
            os.remove(file_path)
            return jsonify({"message": f"File {filename} deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/api/data', methods=['GET'])
    def get_json():
        input_folder = "inputs"
        file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
        unified_json = MainModel(file_paths).unify_to_json()
        # Since unified_json is already a JSON string, return it directly
        return app.response_class(
            response=unified_json,
            status=200,
            mimetype='application/json'
        )

    @app.route('/api/data/<string:file_type>', methods=['GET'])
    def get_data_by_type(file_type):
        input_folder = "inputs"
        file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
        search_list = []
        if file_type == "pdf":
            search_list = [f for f in file_paths if f.endswith('.pdf')]
        elif file_type == "pptx":
            search_list = [f for f in file_paths if f.endswith('.pptx')]
        elif file_type == "csv":
            search_list = [f for f in file_paths if f.endswith('.csv')]
        elif file_type == "json":
            search_list = [f for f in file_paths if f.endswith('.json')]

        unified_json = MainModel(search_list).unify_to_json()
        return app.response_class(
            response=unified_json,
            status=200,
            mimetype='application/json'
        )
    
    @app.route('/api/data/upload', methods=['POST'])
    def upload_files():
        try:
            files = request.files.getlist('files')
            upload_folder = "inputs"
            
            # Create inputs folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)
            
            for file in files:
                if file.filename:
                    file_path = os.path.join(upload_folder, file.filename)
                    file.save(file_path)
            
            return jsonify({"message": f"{len(files)} files uploaded successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # ignore this

    # @app.route('/api/data/convert/<string:file_type>', methods=['GET'])
    # def convert_to_file_type(file_type):
    #     input_folder = "inputs"
    #     output_folder = "outputs"
    #     # Create output folder if it doesn't exist
    #     os.makedirs(output_folder, exist_ok=True)
        
    #     output_filename = f"unified.{file_type}"
    #     output_path = os.path.join(output_folder, output_filename)
        
    #     file_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    #     MainModel(file_paths).convert_to_file(file_type)
        
    #     return jsonify({"message": f"File saved as {output_filename}", "path": output_path})