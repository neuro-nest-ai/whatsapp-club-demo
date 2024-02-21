import pandas as pd
from Pdf_generation.profile import Profile_generation_config
from Pdf_generation.trust_certificate import scannedPdfConverter

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
                print(row)
                if row['Mobile Phone'] == Mobile_Phone:
                    print(row['Mobile Phone'])
                    upi_list.extend([row['Original join date'],
                                     row['Current club join date'], row['Years of service'], 
                                     row['Roles'],
                                     row['Sponser'], row['Member ID'], row['Address'], row['Mobile Phone'],
                                     row['Personal email'], row['Classification']])
            (Original_join_date, Current_club_join_date, Years_of_service, 
            ROLES_Coimbatore_North_Rotary_Club, Sponser, Member_ID, Address, Mobile_Phone,
            Personal_email, Classification) = upi_list# Unpacked the list correctly
            print(upi_list)
            search_text["RI"] = str(Member_ID)
            search_text["Ph.No:"] = str(Mobile_Phone)
            search_text["Mail"] = Personal_email
            search_text["Profession"] = Classification 
            search_text["Original"] = Original_join_date
            search_text['Current'] = Current_club_join_date
            search_text["Years"] = Years_of_service
            search_text["ROLES"] = ROLES_Coimbatore_North_Rotary_Club
            search_text['MEMBER'] = str(Sponser)
            
            return search_text
            
        except FileNotFoundError:
            print("Error: CSV file not found")
            return None

class PdfPipelineConfig:
    def __init__(self):
        pass
    
    def main(self, Mobile_number,save_path):
        pdf = PdfPipeline()
        search_text = pdf.get_data(Mobile_number)
        if search_text:
            profile_config = Profile_generation_config()
            pdf = profile_config.main(save_path,search_text)

save_path = "output.pdf"
file_path=r"Data\Members profile sample.pdf"
print("ok")
scannedPdfConverter(file_path,save_path)     
profile = PdfPipelineConfig()
pdf = profile.main("9791339999",save_path)