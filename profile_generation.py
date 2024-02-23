import pandas as pd
from Pdf_generation.profile import Profile_generation_config





import ocrmypdf
def scannedPdfConverter(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path, skip_text=True)
    print('File converted successfully!')

class PdfPipeline:
    def __init__(self):
        pass
        
    def get_data(self, Mobile_Phone):
        print(type(Mobile_Phone))
        
        upi_list = []
        search_text = {}  # Corrected the initialization to use a dictionary
        path = r'Data\Profile_data.csv' 
        try:
            df = pd.read_csv(path)
            for index, row in df.iterrows():
                if row['Mobile Phone'] == Mobile_Phone:
                    upi_list.extend([row['Name'],row['Original join date'],
                                     row['Current club join date'], row['Years of service'], 
                                     row['Roles'],
                                     row['Sponser'], row['Member ID'], row['Address'], row['Mobile Phone'],
                                     row['Personal email'], row['Classification']])
            (Name,Original_join_date, Current_club_join_date, Years_of_service, 
            ROLES_Coimbatore_North_Rotary_Club, Sponser, Member_ID, Address, Mobile_Phone,
            Personal_email, Classification) = upi_list# Unpacked the list correctly
            search_text['Name']=str(Name)
            search_text["RI"] = str(Member_ID)
            search_text["Ph.No:"] = str(Mobile_Phone)
            search_text["Mail"] = Personal_email
            search_text["Profession"] = Classification 
            search_text["Original"] = Original_join_date
            search_text['Current'] = Current_club_join_date
            search_text["Years"] = Years_of_service
            search_text["ROLES"] = ROLES_Coimbatore_North_Rotary_Club
            search_text['MEMBER'] = str(Sponser)
            
            
            text_dicts = [
                {"x": 270, "y": 700, "text": search_text['Name'], "page_number": 0, "font_name": "Times-Roman", "font_size": 20},
                {"x": 230, "y": 700, "text": "Rtn", "page_number": 0, "font_name": "Times-Roman", "font_size": 20}]


            return search_text,text_dicts
            
        except FileNotFoundError:
            print("Error: CSV file not found")
            return None

class PdfPipelineConfig_profile:
    def __init__(self):
        pass
    
    def main(self, Mobile_number,save_path):
        pdf = PdfPipeline()
        search_text,text_dicts = pdf.get_data(Mobile_number)
        print(search_text)
        print(text_dicts)
        if search_text:
            profile_config = Profile_generation_config()
            pdf = profile_config.main(save_path,search_text,text_dicts)
            return pdf

# save_path = "output.pdf"
# file_path=r"Data\Members profile sample.pdf"
# print("ok")
# scannedPdfConverter(file_path,save_path)     
# profile = PdfPipelineConfig_profile()
# pdf = profile.main("9791339999",save_path)

