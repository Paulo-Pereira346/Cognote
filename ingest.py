import os
from dotenv import load_dotenv

load_dotenv()

def load_notes(folder="data"):
    file_list = []
   
    for file in os.listdir(folder):
        data_dict = {}
        root, ext = os.path.splitext(file)
        if(ext == '.txt'):
            with open(f"{folder}/{file}",'r') as f:
                content = f.read()
                print("File:",file)
                print("Character Count:",len(content))
            data_dict["filename"] = file
            data_dict["text"] = content
            file_list.append(data_dict)
        
    return file_list
            

if __name__ == "__main__":
    print(load_notes())   