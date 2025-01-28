from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
)

text = """
Course Code Course Title Category Faculty Name Slot Hours Conducted Hours Absent Attn % University Practical Details
21MAB102T Regular Advanced Calculus and Complex Analysis Theory Dr.B.Vijayakumar (100431) B 8 2 75.00 -
21EES101T Regular Electrical and Electronics Engineering Theory Dr. Selva Bharathi D (102193) C 8 3 62.50 -
21PYB102J Regular Semiconductor Physics and Computational Methods Theory Dr. Arul Varman Kesavan (102741) D 8 4 50.00 -
21LEH101T Regular Communicative English Theory Dr.Uma Maheswari M.M (102381) F 8 4 50.00 -
21CSC101T Regular Object Oriented Design and Programming Theory Dr.B.Lakshmi Dhevi (103097) G 7 1 85.71 -
21MES102L Regular Engineering Graphics and Design Practical Mr.S.Arul Kumar (101554) LAB 8 0 100.00 -
21CYM101T Regular Environmental Science Practical Panneerselvam P (101449) LAB 3 0 100.00 -
21LEM101T Regular Constitution of India Practical Dr.Uma Maheswari M.M (102381) LAB 3 1 66.67 -
21PYB102J Regular Semiconductor Physics and Computational Methods Practical Dr.Sujit Kumar (103499) LAB 4 2 50.00 -
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that converts tabular text into JSON format."
        },
        {
            "role": "user",
            "content": f"Convert the following tabular data into a JSON array:\n{text}"
        }
    ]
)

choices = response.choices  # Access the choices attribute
json_output = choices[0].message.content.strip()
print(json_output)