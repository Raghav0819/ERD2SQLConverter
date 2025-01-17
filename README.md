
# Snap2SQL

Snap2SQL is a Python-based project that converts Entity-Relationship Diagram (ERD) images into SQL scripts and deploys the database directly to a MySQL server. This tool simplifies the database creation process by automating the conversion of ER diagrams into a functional MySQL database.

## Features

- Converts ERD images (JPG, PNG, JPEG) into valid MySQL scripts.
- Ensures MySQL compatibility with proper escaping of reserved words.
- Supports file export for SQL scripts and schemas.
- Allows deployment of databases directly to MySQL servers.
- Includes customizable schema modifications and real-time updates.

## Prerequisites

- Python 3.8+
- MySQL server
- Required Python libraries:
  - `mysql-connector-python`
  - `google-generativeai`
  - `tkinter`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Snap2SQL.git
   cd Snap2SQL
   ```

2. Install dependencies:
   ```bash
   pip install mysql-connector-python google-generativeai
   ```

## Usage

1. Open the `Snap2SQL.py` file and replace the placeholder `api_key` value with your own API key. Look for the following code snippet:
   ```python
   api_key = "YOUR_API_KEY_HERE"
   ```

   You need to replace `YOUR_API_KEY_HERE` with your valid API key for the Google Generative AI service.


1. Run the script:
   ```bash
   python Snap2SQL.py
   ```

2. Follow the interactive menu to:
   - Convert an ERD image into a SQL script.
   - Modify the generated schema if needed.
   - Save the SQL script to a file.
   - Deploy the database to a MySQL server.

### Menu Options
- **Write Script to File:** Save the SQL script to a `.sql` file.
- **Deploy Database:** Deploy the generated SQL script directly to a MySQL server.
- **Write to File and Deploy:** Save the script and deploy the database simultaneously.
- **Exit:** Exit the application.

## Supported Image Formats

- JPG
- PNG
- JPEG

## Guidelines for Accurate Conversion

1. **Clear Structure:** Label all entities, attributes, and relationships distinctly.
2. **Consistent Naming:**
   - Avoid special characters (e.g., `/`).
   - Use singular form and lowercase for entity names.
3. **Explicit Relationships:** Define relationships clearly (e.g., one-to-many).
4. **Avoid Ambiguities:** Ensure names are precise and avoid unclear abbreviations.
5. **Reserved Words:** Don’t use MySQL reserved words for names unless escaped (e.g., `date`, `order`).

## Example Output

After processing a valid ERD image, Snap2SQL will generate:

- **SQL Script:**
  ```sql
  CREATE TABLE `example_table` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `name` VARCHAR(255) NOT NULL,
      PRIMARY KEY (`id`)
  );
  ```

- **Schema Explanation:**
  ```
  +----------+---------------+------+-----+---------+----------------+
  | Field    | Type          | Null | Key | Default | Extra          |
  +----------+---------------+------+-----+---------+----------------+
  | id       | INT           | NO   | PRI | NULL    | auto_increment |
  | name     | VARCHAR(255)  | NO   |     | NULL    |                |
  +----------+---------------+------+-----+---------+----------------+
  ```

- **Accuracy Confidence:** Indicates confidence in the generated schema (e.g., 95%).

- ## License

This project is licensed under the MIT License. See the LICENSE file for details.



## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any changes or enhancements.

## Contact

For any issues or inquiries, feel free to reach out:
- **Email:** ragh192005@gmail.com
- **GitHub:** [Raghav0819](https://github.com/Raghav0819)

---

Happy coding!
