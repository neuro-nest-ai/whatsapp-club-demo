import pandas as pd
import ocrmypdf
import os
from PyPDF2 import PdfMerger
from Pdf_generation.report import Report_generation_config
from datetime import datetime, timedelta

def scannedPdfConverter(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path, skip_text=True)
    print('File converted successfully!')

class PdfPipeline:
    def __init__(self):
        pass
        
    def get_data(self, Date):
        data_list = []
        path = r'Data\report.csv'
        directory = r"roatryevents\roatryevents"
        
        try:
            df = pd.read_csv(path)
            for index, row in df.iterrows():
                if row['Date'] == Date:
                    search_text = {
                        "Date": str(row['Date']),
                        "Service": str(row['Service']),
                        "Heading": str(row['Heading']),
                        "content":str(row['content']),
                        "Hours": str(row['Duration_in_Hours']),
                        "Cost": str(row['Cost_of_club_in_Rs_For_Service _Projects_Only']),
                        "Volunteer": str(row['Volunteer_hours_For_Service_Projects_Only']),
                        "beneficieries": str(row['Value_to_beneficieries_in_Rs_For_Service_Projects_Only']),
                        "value": str(row['No_of_beneficieries_For_Service_Projects_Only']),
                        "Rupees":"0",
                        "Members": str(row['Members']),
                        "Guest": str(row['Guest_Rtns']),
                        "Rotaractors": str(row['Rotaractors']),
                        "Public": str(row['Public']),
                        "Family": str(row['Family'])
                    }
                    
                    text_dicts = [
                        {"x": 50, "y": 800-5, "text": search_text["Date"], "page_number": 0,"font_name": "Times-Roman", "font_size": 14},
                        {"x": 150, "y": 700, "text": search_text["Heading"], "page_number": 0,"font_name": "Times-Roman", "font_size": 25},
                        {"x": 60, "y": 400, "text": search_text["content"], "page_number": 0,"font_name": "Times-Roman", "font_size": 14},
                        {"x": 400, "y": 800-5, "text": search_text["Service"], "page_number": 0,"font_name": "Times-Roman", "font_size": 14}
                    ]
                    
                    image_path = os.path.join(directory, row['IMG'] + ".jpg")
                    
                    data_list.append({"search_text": search_text, "text_dicts": text_dicts, "image_path": image_path})
            return data_list
        

        except FileNotFoundError:
            print("Error: CSV file not found")
            return None

class PdfPipelineConfig:
    def __init__(self):
        pass
    
    def main(self, start_date, end_date, save_path_base):
        pdf = PdfPipeline()
        merged_output_filenames = []
        merged_pdf = PdfMerger()  # Initialize the merger
        
        # Convert start_date and end_date strings to datetime objects
        start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
        end_datetime = datetime.strptime(end_date, "%d-%m-%Y")
        
        # Iterate over the range of dates
        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            current_date = current_datetime.strftime("%d-%m-%Y")
            data_list = pdf.get_data(current_date)
            
            if data_list:
                # Create the directory if it doesn't exist
                if not os.path.exists(save_path_base):
                    os.makedirs(save_path_base)
                
                for i, data in enumerate(data_list):
                    search_text = data["search_text"]
                    text_dicts = data["text_dicts"]
                    image_path = data["image_path"]
                    profile_config = Report_generation_config()
                    output_filename = f"output_{current_date}_{i+1}.pdf"  # Include the date in the filename
                    file_path = r"Data\Duplicate.pdf"
                    scannedPdfConverter(file_path, output_filename)
                    
                    # Check if 'Value' key exists in search_text dictionary
                    if 'Value' not in search_text:
                        search_text['Value'] = ''  # Provide a default value if 'Value' key is missing
                    
                    profile_config.main(output_filename, search_text, image_path, text_dicts)
                    print(f"PDF file {output_filename} created successfully.")
                    
                    # Add the generated PDF to the merger
                    merged_pdf.append(output_filename)
                
                print(f"All PDF files for {current_date} merged successfully.")
            else:
                print(f"No data found for the date {current_date}. No PDF generated.")
                
            # Move to the next date
            current_datetime += timedelta(days=1)
        
        # Write the merged PDF to the output file
        merged_output_filename = os.path.join(save_path_base, "merged_output.pdf")
        with open(merged_output_filename, 'wb') as merged_output_file:
            merged_pdf.write(merged_output_file)
            
        merged_output_filenames.append(merged_output_filename)
        print(f"All PDF files merged successfully into {merged_output_filename}.")
        
        return merged_output_filename

# Example usage:
if __name__ == "__main__":
    save_path_base = "output"
    profile = PdfPipelineConfig()
    start_date = "01-07-2023"
    end_date = "01-09-2023"
    merged_output_filenames = profile.main(start_date, end_date, save_path_base)
    merged_pdf_path = merged_output_filenames[0]  # Assuming only one merged PDF is generated
    with open(merged_pdf_path, 'rb') as file:
        pdf_data = file.read()
    # Now you can use pdf_data as needed, for example, you can save it to a file or send it through email.
