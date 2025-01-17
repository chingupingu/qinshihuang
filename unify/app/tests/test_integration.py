import os
import json
import pytest
from flask import Flask
from run import app
from models.PDFModel import PDFModel
from models.CSVModel import CSVModel
from models.JSONModel import JSONModel
from models.PPTXModel import PPTXModel
from models.MainModel import MainModel

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_file_upload_and_unification(client):
    # Test data paths
    testfiles_folder = "testfiles"
    file_paths = [os.path.join(testfiles_folder, f) for f in os.listdir(testfiles_folder) if os.path.isfile(os.path.join(testfiles_folder, f))]
    
    # Test file upload endpoint
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            response = client.post('/upload', data={
                'file': (f, os.path.basename(file_path))
            })
            assert response.status_code == 200

    # Test unification endpoint
    response = client.post('/unify', json={'fileType': 'all'})
    assert response.status_code == 200
    
    # Verify response structure
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_individual_model_processing():
    # Test PDF processing
    pdf_path = "testfiles/dataset3.pdf"
    if os.path.exists(pdf_path):
        pdf_model = PDFModel(pdf_path)
        pdf_json = pdf_model.get_json()
        assert isinstance(pdf_json, str)
        assert len(pdf_json) > 0

    # Test CSV processing
    csv_path = "testfiles/dataset2.csv"
    if os.path.exists(csv_path):
        csv_model = CSVModel(csv_path)
        assert csv_model.json_output is not None
        csv_result = csv_model.get_csv()
        assert isinstance(csv_result, str)

    # Test JSON processing
    json_path = "testfiles/dataset1.json"
    if os.path.exists(json_path):
        json_model = JSONModel(json_path)
        json_result = json_model.get_json()
        assert isinstance(json_result, str)
        assert len(json_result) > 0

    # Test PPTX processing
    pptx_path = "testfiles/dataset4.pptx"
    if os.path.exists(pptx_path):
        pptx_model = PPTXModel(pptx_path)
        pptx_json = pptx_model.get_json()
        assert isinstance(pptx_json, str)
        assert len(pptx_json) > 0

def test_main_model_integration():
    testfiles_folder = "testfiles"
    file_paths = [os.path.join(testfiles_folder, f) for f in os.listdir(testfiles_folder) if os.path.isfile(os.path.join(testfiles_folder, f))]
    
    ingestion = MainModel(file_paths)
    all_json_data = ingestion.ingest_inputs()
    
    # Verify the unified data structure
    assert isinstance(all_json_data, str)
    data = json.loads(all_json_data)
    assert isinstance(data, list)
    assert len(data) > 0 