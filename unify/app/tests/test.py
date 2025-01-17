import os
from models.PDFModel import PDFModel
from models.CSVModel import CSVModel
from models.JSONModel import JSONModel
from models.PPTXModel import PPTXModel
from models.MainModel import MainModel


###################
# PDF Model tests #
###################


# pdf_path = "../../datasets/dataset3.pdf"
# pdf_model = PDFModel(pdf_path)

# # Get JSON first
# json_result = pdf_model.get_json()
# print("JSON output:", json_result)

# # Convert back to PDF
# pdf_result = pdf_model.get_pdf(return_buffer=True)
# print("PDF generated successfully")

# # Since get_pdf() returns a Flask response, 
# # you might want to save it to a file for testing:
# with open("output_pdf.pdf", "wb") as f:
#     f.write(pdf_result.getvalue())


###################
# CSV Model tests #
###################


# # Get JSON first
# csv_path = "../../datasets/dataset2.csv"
# csv_model = CSVModel(csv_path)
# print(csv_model.json_output)

# # Convert back to CSV
# csv_result = csv_model.get_csv()
# print("CSV generated successfully")
# with open("output_csv.csv", "w") as f:
#     f.write(csv_result)


####################
# JSON Model tests #
####################


# # Get processed JSON
# json_path = "../../datasets/dataset1.json"
# json_model = JSONModel(json_path)
# json_result = json_model.get_json()
# print("JSON output:", json_result)



####################
# PPTX Model tests #
####################


# # Get JSON first
# pptx_path = "../../datasets/dataset4.pptx"
# pptx_model = PPTXModel(pptx_path)
# print(pptx_model.get_json())

# # Convert back to PPTX
# pptx_result = pptx_model.get_pptx(return_buffer=True)
# print("PPTX generated successfully")
# with open("output_pptx.pptx", "wb") as f:
#     f.write(pptx_result.getvalue())


#########################
# Main Model tests #
#########################

dataset_folder = "../../datasets"
file_paths = [os.path.join(dataset_folder, f) for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
ingestion = MainModel(file_paths)
all_json_data = ingestion.ingest_inputs()
print(all_json_data)
with open("output_json.json", "w") as f:
    f.write(all_json_data)

