import json
import os
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from flask import send_file
import tabula
import pandas as pd

class PDFModel:
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

    ### 1. Return PDF as json ###
    def get_json(self):
        self.read_pdf()
        self.process_content()
        return self.json_output

    ### 2. Return json as PDF ###
    def get_pdf(self, return_buffer=False):
            try:
                json_data = json.loads(self.json_output)
                # create PDF in memory
                buffer = BytesIO()
                pdf = canvas.Canvas(buffer)
                self.write_json_to_pdf(pdf, json_data)
                pdf.save()
                buffer.seek(0)

                if return_buffer:
                    return buffer
                
                # return the PDF
                return send_file(
                    buffer,
                    mimetype='application/pdf',
                    as_attachment=False  # This will display in browser
                )

            except Exception as e:
                raise Exception(f"Error converting JSON to PDF: {str(e)}")


    ########################
    ### HELPER FUNCTIONS ###
    ########################

    ### PDF reading ###
    # reads the pdf and updates self.content
    def read_pdf(self):
        try:
            # title
            with open(self.input_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = reader.pages[0].extract_text()
                self.title = content.split('\n')[0]

        except Exception as e:
            return json.dumps({
                "error": f"Failed to read PDF with PyPDF2: {str(e)}"
            })
        
        try:
            # table
            table = tabula.read_pdf(
                self.input_path,
                pages=1,  
                multiple_tables=False,
                lattice=True
            )
            
            if table:
                # Get first table
                df = table[0]
                self.headers = df.columns.tolist()
                self.data = df.values.tolist()
            
            return None
        
        except Exception as e:
            return json.dumps({
                "error": f"Failed to read PDF with Tabula: {str(e)}"
            })

    
    ### PDF processing ###
    # converts the content to a json object and updates self.processed_content
    def process_content(self):
        # Process data rows
        data_rows = []
        for row in self.data:
            row_dict = {}

            # Create key-value pairs
            for header, value in zip(self.headers, row):
                # Handle missing/null values
                if pd.isna(value) or value is None:
                    value_str = ""
                else:
                    value_str = str(value)
                
                # convert to float if possible
                # try:
                #     if '.' in value_str:
                #         value = float(value_str.replace(',', ''))
                #     elif value_str.replace(',', '').isdigit():
                #         value = int(value_str.replace(',', ''))
                # except ValueError:
                #     value = value_str  # Keep as string if conversion fails
                
                row_dict[header] = value_str
                
            data_rows.append(row_dict)

        # Create final JSON object with title as key
        result = {self.title: data_rows}
        self.json_output = json.dumps(result)
            
    ### Write JSON to PDF ###
    def write_json_to_pdf(self, pdf, json_data):
        # Set up initial coordinates and styling
        page_width = 612  # Standard letter width in points
        margin = 50
        y_start = 750
        row_height = 30
        
        # Get title and data
        title = list(json_data.keys())[0]
        data_rows = json_data[title]
        
        # Get headers from first row
        headers = list(data_rows[0].keys())
        col_widths = [120] * len(headers)  # Equal width for all columns
        
        # Draw the title
        pdf.setFont("Helvetica-Bold", 14)
        title_width = pdf.stringWidth(title)
        pdf.drawString((page_width - title_width) / 2, y_start, title)
        
        # Move down for table
        y = y_start - 50
        
        # Draw headers
        pdf.setFont("Helvetica-Bold", 12)
        x = margin
        for i, header in enumerate(headers):
            # Draw header cell
            pdf.rect(x, y, col_widths[i], row_height)
            # Format header for display (replace underscores with spaces)
            display_header = header.replace('_', ' ').title()
            # Center text in cell
            text_width = pdf.stringWidth(display_header)
            x_text = x + (col_widths[i] - text_width) / 2
            pdf.drawString(x_text, y + 10, display_header)
            x += col_widths[i]
        
        # Draw data rows
        y -= row_height
        pdf.setFont("Helvetica", 12)
        
        for row in data_rows:
            if y < 50:  # Check if we need a new page
                pdf.showPage()
                y = y_start
                pdf.setFont("Helvetica", 12)
            
            x = margin
            for header in headers:
                value = str(row[header])
                
                # Draw cell border
                pdf.rect(x, y, col_widths[0], row_height)
                
                # Center text in cell
                text_width = pdf.stringWidth(value)
                x_text = x + (col_widths[0] - text_width) / 2
                pdf.drawString(x_text, y + 10, value)
                
                x += col_widths[0]
            
            y -= row_height
