## PDF Data Extraction Script

### Features
- Extracts:
  - Full names, first names, and last names.
  - Age and gender from strings like `24F` or `37M`.
  - Addresses, including street number, street name, and street type.
  - City, state, and ZIP code.
  - Other customizable fields like "Preferred" and "Cell."
- Supports multi-page PDFs.
- Exports extracted data into a structured CSV file.

### Prerequisites
Ensure you have the following installed:

- **Python** (>=3.6)

- **Required Python Libraries**  
   Install the libraries using pip:
   ```bash
   pip install PyPDF2
   ```

### How to Use

- **Clone or Download the Repository**  
   Clone the repository to your local machine using:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

- **Place Your PDF File**  
   Save the PDF file you want to process in the same directory as the script. For example, `prec1_2.pdf`.

- **Run the Script**  
   Execute the script with:
   ```bash
   python script_name.py
   ```
   Replace `script_name.py` with the actual name of the script file.

- **Extracted Data**  
   The extracted data will be saved in a CSV file named `extracted_data.csv` in the same directory.

### Modifiable Sections

- **Fields to Extract**  
To modify or add new data patterns to extract (e.g., "Preferred:" or "Cell:"), update the logic in the main loop where patterns are detected:

     ```python
     if complete_word == "Preferred:":
         preferred_recorder_flag = True
     ```



Sample output:

| Name      | First Name | Last Name | Age | Gender | City   | State | Zip     |
|-----------|------------|-----------|-----|--------|--------|-------|---------|
| John Doe  | John       | Doe       | 24  | F      | Boston | MA    | 02118   |
| Jane Smith| Jane       | Smith     | 37  | M      | Denver | CO    | 80203   |

### Contributing
Feel free to open issues or submit pull requests for improvements or additional features.
