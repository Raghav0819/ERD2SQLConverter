from tkinter.filedialog import askopenfilename
import google.generativeai as genai
import json 
import mysql.connector as server 
import pymysql

api_key="AIzaSyChrY2_oZRIJbo7RH2e0NrgVzWcUxe4XRU"
genai.configure(api_key=api_key)

prompt = """
You are now a specialized database management expert tasked with converting any provided entity-relationship diagram (ERD) into a valid MySQL SQL script. Follow the instructions strictly and ensure you double-check all aspects of the output:
1. **response**: Return `True` if the SQL script can be successfully generated from the ERD, otherwise return `False` (Boolean).

2. **script**: Generate a single-line, syntactically correct SQL script. Rigorously verify its accuracy, adhering to the following rules:
   - Table and column names must not contain the character `/` (For Example: 'teacher/subject' is invalid table name but `teacher` is a valid table name).
   - If any table or column names are ambiguous, select the most logical and relevant name.
   - Ensure the SQL follows MySQL syntax and best practices.
   - Be aware that MySQL has reserved keywords that cannot be used as table or column names unless enclosed in backticks (`).

3. **explanation**: Provide a detailed breakdown of each table, column, and relationship from the ERD, ensuring clarity and correctness.

4. **confidence**: Provide your confidence level in the generated SQL script as an integer percentage (0-100%).

You must double-check the SQL script for syntactical correctness, ensure that it follows the provided instructions rigorously, and confirm that it accurately represents the ERD data. If there are any issues or the instructions cannot be executed, return `'response': False`. Do not respond if no Image of ERD is provided.
"""

# Create the model
generation_config = {
  "temperature": 1,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [prompt],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"response\": false}\n\n```",
      ],
    },
  ]
)
er_image = genai.upload_file(path=askopenfilename())
response = chat_session.send_message([er_image])

#print(response.text)  

with open('res.json', 'w') as f:
    f.write(response.text)
data=json.loads(response.text)


db = server.connect(host="127.0.0.1", user='root', passwd='1234', database="aisql")
cursor = db.cursor()
cursor.execute(data['script'])
db.close()
print("[+] Database Setup Succesfully ")
print(data['explanation'])
print('Accuracy: ', data['confidence'])

