import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf = PyPDF2.PdfFileReader(file)
            text = ""
            for i in range(pdf.getNumPages()):
                text += pdf.getPage(i).extract_text()
            return text
        
        except Exception as e:
            print(f"Error reading pdf file: {e}")
            return None
    
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "File type not supported. Please upload a pdf or txt file"
        )
    
def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " || ".join(value['options'])

            correct = value['correct']
            quiz_table_data.append({"MCQ":mcq, "Choices":options, "Correct":correct})
        return quiz_table_data
    except Exception as e:
        print(f"Error getting table data: {e}")
        return None