import os
import json
import pytest
from flask import Flask
from app.run import app
from app.models.PDFModel import PDFModel
from app.models.CSVModel import CSVModel
from app.models.JSONModel import JSONModel
from app.models.PPTXModel import PPTXModel
from app.models.MainModel import MainModel

# Add this at the top after imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILES_DIR = os.path.join(CURRENT_DIR, "testfiles")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_file_upload_and_unification(client):
    # Use TEST_FILES_DIR instead of "testfiles"
    file_paths = [os.path.join(TEST_FILES_DIR, f) for f in os.listdir(TEST_FILES_DIR) 
                 if os.path.isfile(os.path.join(TEST_FILES_DIR, f))]
    
    # Test file upload endpoint
    data = {}
    files = []
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            file_content = f.read()
            files.append(('files', (os.path.basename(file_path), file_content)))
    
    response = client.post('/api/data/upload', data=data, content_type='multipart/form-data', buffered=True)
    assert response.status_code == 200

    # Test unification endpoint
    response = client.get('/api/data')
    assert response.status_code == 200
    
    # Verify response structure
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_individual_model_processing():
    # Test PDF processing
    pdf_path = os.path.join(TEST_FILES_DIR, "dataset3.pdf")
    if os.path.exists(pdf_path):
        pdf_model = PDFModel(pdf_path)
        pdf_json = pdf_model.get_json()
        assert isinstance(pdf_json, str)
        assert len(pdf_json) > 0
        # Verify it's valid JSON
        pdf_data = json.loads(pdf_json)
        assert isinstance(pdf_data, (dict, list))

    # Test CSV processing
    csv_path = os.path.join(TEST_FILES_DIR, "dataset2.csv")
    if os.path.exists(csv_path):
        csv_model = CSVModel(csv_path)
        csv_json = csv_model.get_json()
        assert isinstance(csv_json, str)
        # Verify it's valid JSON
        csv_data = json.loads(csv_json)
        assert isinstance(csv_data, (dict, list))
        csv_result = csv_model.get_csv()
        assert isinstance(csv_result, str)

    # Test JSON processing
    json_path = os.path.join(TEST_FILES_DIR, "dataset1.json")
    if os.path.exists(json_path):
        json_model = JSONModel(json_path)
        json_result = json_model.get_json()
        assert isinstance(json_result, str)
        assert len(json_result) > 0
        # Verify it's valid JSON
        json_data = json.loads(json_result)
        assert isinstance(json_data, (dict, list))

    # Test PPTX processing
    pptx_path = os.path.join(TEST_FILES_DIR, "dataset4.pptx")
    if os.path.exists(pptx_path):
        pptx_model = PPTXModel(pptx_path)
        pptx_json = pptx_model.get_json()
        assert isinstance(pptx_json, str)
        assert len(pptx_json) > 0
        # Verify it's valid JSON
        pptx_data = json.loads(pptx_json)
        assert isinstance(pptx_data, (dict, list))

def test_main_model_integration():
    file_paths = [os.path.join(TEST_FILES_DIR, f) for f in os.listdir(TEST_FILES_DIR) 
                 if os.path.isfile(os.path.join(TEST_FILES_DIR, f))]
    
    main_model = MainModel(file_paths)
    unified_json = main_model.unified_json
    
    # Verify the unified data structure
    assert isinstance(unified_json, str)
    data = json.loads(unified_json)
    assert isinstance(data, list)
    assert len(data) > 0 