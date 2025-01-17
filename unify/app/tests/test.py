import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.models.PDFModel import PDFModel
from app.models.CSVModel import CSVModel
from app.models.JSONModel import JSONModel
from app.models.PPTXModel import PPTXModel
from app.models.MainModel import MainModel

os.makedirs("../outputs", exist_ok=True)


###################
# PDF Model tests #
###################


pdf_path = "../inputs/dataset3.pdf"
pdf_model = PDFModel(pdf_path)

# Get JSON first
json_result = pdf_model.get_json()
print("JSON output:", json_result)

################# IGNORE THIS #################
# Convert back to PDF
# pdf_result = pdf_model.get_pdf(return_buffer=True)
# print("PDF generated successfully")

# with open("../outputs/pdf_test_output.pdf", "wb") as f:
#     f.write(pdf_result.getvalue())
################# IGNORE THIS #################


###################
# CSV Model tests #
###################


# Get JSON first
csv_path = "../inputs/dataset2.csv"
csv_model = CSVModel(csv_path)
print(csv_model.get_json())

################# IGNORE THIS #################
# # Convert back to CSV
# csv_result = csv_model.get_csv()
# print("CSV generated successfully")
# with open("../outputs/csv_test_output.csv", "w") as f:
#     f.write(csv_result)
################# IGNORE THIS #################


####################
# JSON Model tests #
####################


# Get processed JSON
json_path = "../inputs/dataset1.json"
json_model = JSONModel(json_path)
print(json_model.get_json())

with open("../outputs/json_test_output.json", "w") as f:
    f.write(str(json_model.get_json()))


####################
# PPTX Model tests #
####################


# Get JSON first
pptx_path = "../inputs/dataset4.pptx"
pptx_model = PPTXModel(pptx_path)
print(pptx_model.get_json())

################# IGNORE THIS #################
# # Convert back to PPTX
# pptx_result = pptx_model.get_pptx(return_buffer=True)
# print("PPTX generated successfully")
# with open("../outputs/pptx_test_output.pptx", "wb") as f:
#     f.write(pptx_result.getvalue())
################# IGNORE THIS #################


#########################
# Main Model tests #
#########################

dataset_folder = "../inputs"
file_paths = [os.path.join(dataset_folder, f) for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
ingestion = MainModel(file_paths)
all_json_data = ingestion.unify_to_json()
print(all_json_data)
with open("../outputs/main_model_test_output.json", "w") as f:
    f.write(all_json_data)

