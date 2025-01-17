import mysql.connector as connector
import json
import google.generativeai as genai
import json
from tkinter.filedialog import askopenfilename

class Snap2SQL:
    def __init__(self, api_key,model_name="gemini-1.5-pro"):
        self.api_key=api_key
        self.__model_name=model_name
        genai.configure(api_key=self.api_key)
        generation_config = {
            "temperature": 0.3,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4096,
            "response_mime_type": "application/json",}
        self.__model = genai.GenerativeModel(
            model_name= self.__model_name,
            generation_config=generation_config,)

    def execute_sql_script(self,sql_connector, script):
            
            self.__connector=sql_connector
            cursor=self.__connector.cursor()
            for _ in cursor.execute(script, multi=True):
                pass
            cursor.close()
        
    def write_to_file(self, script, schema ,file_name):
        script = script.replace(";", ";\n")
        file_name=file_name+".sql"

        with open(file_name,"w") as f:
            f.write(script)
        with open("schema.txt", "w") as f:
            f.write(schema)
    
    def ERD_to_SQL(self, image_path, info=""):
        prompt= """
        You are a specialized database management expert tasked with converting any provided Entity-Relationship Diagram (ERD) into a valid MySQL SQL script. IMPORTANT: DO NOT GENERATE ANY OUTPUT UNLESS A VALID ERD IS PROVIDED IN THE INPUT. If no ERD is provided, respond with `{"response": false, "script": null, "explanation": null, "confidence": null}`.

        If and only if a valid ERD is provided, follow these instructions and provide the output in the specified format:

        1. **response**: Return `True` if a valid SQL script can be generated from the ERD; otherwise, return `False`.

        2. **script**: Generate a single-line, syntactically correct SQL script that strictly adheres to the following:
        - Table and column names must not contain slashes (`/`). For example, `teacher_subject` is valid, but `teacher/subject` is invalid.
        - For ambiguous table or column names, select the most logical and relevant term based on context.
        - Ensure strict compliance with MySQL syntax and best practices.
        - Use INT instead of INTEGER for better MySQL compatibility.
        - Always check for and properly escape MySQL reserved words with backticks (e.g., `groups`, `order`, `date`, etc.).
        - Follow a consistent naming convention:
        * Use snake_case for table and column names
        * Avoid spaces in names
        * Use singular form for table names
        * Use lowercase for all identifiers unless escaping is required
        - Include proper spacing and formatting in the generated SQL for better readability.
        - When creating foreign key constraints, ensure the referenced table name is properly escaped if it's a reserved word.

        3. **explanation**: Format the output as ASCII tables for each database table, followed by a relationships table. Each table should follow this format:
        +----------+---------------+------+-----+---------+----------------+
        | Field | Type | Null | Key | Default | Extra |
        +----------+---------------+------+-----+---------+----------------+
        | id | int | NO | PRI | NULL | auto_increment|
        | name | varchar(255) | NO | | NULL | |
        +----------+---------------+------+-----+---------+----------------+

        Followed by a relationships table:
        +---------------+---------------+---------------+-------------------+-------------+
        | Table | Foreign Key | References | Relationship Type| Cardinality |
        +---------------+---------------+---------------+-------------------+-------------+
        | table_name | foreign_key | ref_table | One-to-Many | 1:N |
        +---------------+---------------+---------------+-------------------+-------------+

        4. **confidence**: Indicate your confidence level in the generated SQL script as a percentage between 0 and 100.

        Before generating the final output:
        - Verify all table and column names against MySQL reserved words list.
        - Ensure proper escaping of all reserved words with backticks.
        - Validate all data types are MySQL-compatible.
        - Verify referential integrity in all foreign key constraints.
        - Check for proper use of primary and foreign keys.
        - Ensure all multi-word identifiers follow consistent naming conventions.

        STRICT REQUIREMENT: This prompt must only generate output when provided with a valid ERD input. If no ERD is provided in the input, respond only with `{"response": false, "script": null, "explanation": null, "confidence": null}`.

        Your response must never include sample or example output unless working with an actual provided ERD.
        """
        chat_session = self.__model.start_chat(
            history=[
                {"role": "user", "parts": [prompt],},
                {
                    "role": "model",
                    "parts": [
                        "```json\n{\"response\": false, \"script\": null, \"explanation\": null, \"confidence\": null}\n\n```",],
                        },])
        erd_image = genai.upload_file(path=image_path)
        response = chat_session.send_message([info ,erd_image])
        response = json.loads(response.text)  

        if response["response"] == False:
            raise Exception("Unable To Process Image, ERD Not Detected")  
                  
        return response['script'], response['explanation'], response['confidence']


def main():
    api_key="Enter_API_KEY"
    erd_converter = Snap2SQL(api_key=api_key)
    
    banner = r"""
                            ____                       ____   ____    ___   _     
                            / ___|  _ __    __ _  _ __ |___ \ / ___|  / _ \ | |    
                            \___ \ | '_ \  / _` || '_ \  __) |\___ \ | | | || |    
                            ___) || | | || (_| || |_) |/ __/  ___) || |_| || |___ 
                            |____/ |_| |_| \__,_|| .__/|_____||____/  \__\_\|_____|
                                                |_|                              
            """
    
    
    guidelines = """\033[36m
Suggestions for Accurate ERD Conversion:

1. Clear Structure: Label all entities, attributes, and relationships distinctly.
2. Consistent Naming:
    - Avoid special characters like /.
    - Use singular form and lowercase for entity names.
3. Explicit Relationships: Define relationships clearly (e.g., one-to-many).
4. Avoid Ambiguities: Ensure names are precise and avoid unclear abbreviations.
5. Reserved Words: Don\'t use MySQL reserved words for names unless escaped (e.g., `date`, `order`).
\033[0m
"""
    menu = """\033[1;33m
Menu Options:
1. Write Script to File
2. Deploy Database
3. Write to File and Deploy
0. Exit
\033[0m      
"""

    print("\033[1;33m"+banner+"\033[0m")
    print("\033[1;41m**Important**\033[0m")
    print(guidelines)
    input("Press Enter To Continue....")
    
    try: 
        file_path=askopenfilename()
        print("[+] File Selected ")
    except Exception as Err:
        print("[-] File Not Selected... Try Again ")
        exit()

    if not file_path.endswith(('.jpg','.png','.jpeg')):
        print("\n\033[41m[-]File Format Not Supported\033[40m")
        print("Supported File Format: JPG, PNG, JPEG")
        input("Press Enter to Exit")
        exit()

    print("[+] Converting ERD Image into SQL Script... ")    
    
    try:    
        script, schema, accuracy = erd_converter.ERD_to_SQL(file_path)
        print("[+] Converted Successfully ")
    except Exception as err:
        print(f"Error: {err}")
        print("Either The Image Doesn't Contain ERD OR Try Again with a More Clear Image")
        exit()

    print(schema,end='\n')
    
    if accuracy >= 95:
        print("Accuracy: \033[44m"+str(accuracy)+"\033[40m\n")
    else:
         print("Accuracy: \033[41m"+str(accuracy)+"\033[40m\n")

    ques = input("Would you like to make any changes to the Schema(y/N):")
    
    if ques == 'y' or ques == 'Y':
        changes = input('Enter the changes you wish to apply to the schema (leave blank to exit): ')
        while changes != "":
            script, schema, accuracy = erd_converter.ERD_to_SQL(file_path, info=changes)
            print(schema,end='\n')
            if accuracy >= 95:
                print("Accuracy: \033[44m"+str(accuracy)+"\033[40m\n")
            else:
                print("Accuracy: \033[41m"+str(accuracy)+"\033[40m\n")
            changes = input('Enter the changes you wish to apply to the schema (leave blank to exit): ')
                    
    print(menu)
    
    option = str(input("Select One Option (Default:1): "))

    if option == '0':
        exit()
    
    if option == '1' or option == '3':
        file_name = input("Enter File Name: ")
        while file_name == "":
            file_name = input("Enter File Name: ")

        erd_converter.write_to_file(file_name=file_name, schema=schema, script=script)
        print("[+] Writen To File Succesfully :)")
        
    if option == '2' or option == '3':
        host = input("Enter Host Address (Default:localhost): ")
        if host == "":
            host="localhost"
        user = input("Enter User for The Database (Default:root): ")
        if user == "":
            user="root"

        passwd = input("Enter Password For MySQL Server: ")

        while passwd == "":
            passwd = input("Enter Password For MySQL Server: ")
        
        database=input("Enter Database Name (Database will be created if doesn't Exist): ")
        
        while database == "":
            database=input("Enter Database Name (Database will be created if doesn't Exist): ")
        
        try:
            print("[+] Trying to Connect to Database...")
            connection = connector.connect(host=host,user=user,passwd=passwd, database=database)
            print("[+]Connected to Database Succesfully ")
        except connector.Error as err:
            if err.errno == 1049:
                print("[-] Database Doesn't Exist ")
                print("[+] Creating Database " + database)
                connection = connector.connect(host=host,user=user,passwd=passwd)
                query = "CREATE DATABASE " + database
                erd_converter.execute_sql_script(connection, query)
                print("[+] Database created succesfully ")
                connection.close()
            else: 
                print(f"A Error Has Occured: {err}")
                print("[-] Unable to Create Database")
                exit()
        connection = connector.connect(host=host,user=user,passwd=passwd, database=database)  

        try:
            erd_converter.execute_sql_script(sql_connector=connection, script=script)
            print("[+] Database Deployed Successfully :) ")
            input("Press Enter to Exit")
        except Exception as err:
            print(f"Unable to Execute Script: {err}")
    exit()

if __name__ == "__main__":
    main()        

    

        






    
