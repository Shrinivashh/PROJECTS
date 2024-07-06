# Students Information System

## Overview

Welcome to the Students Information System! This web application is built using Flask, HTML, and CSS to help you manage student records efficiently. The system allows you to add, remove, and search for students by their roll number, making it a comprehensive solution for handling student data.

## Features

- **Add Student**: Easily add new student records with relevant details.
- **Remove Student**: Remove student records as needed.
- **Search Student**: Search for student information using their roll number.
- **View All Students**: Display a list of all students currently in the system.
- **Update Student**: Modify existing student records with new information.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/students-information-system.git
   cd students-information-system
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## Usage

### Home Page

The home page provides an overview of the system and navigation links to different functionalities.

### Add Student

Navigate to the "Add Student" page to enter the details of a new student. The form will require fields such as:
- Roll Number
- Name
- Class
- Age
- Address

### Remove Student

Go to the "Remove Student" page and enter the roll number of the student you wish to remove from the system.

### Search Student

Use the "Search Student" functionality to find a student by their roll number. This will display the student's details if they are in the system.

### View All Students

The "View All Students" page lists all students currently stored in the system, along with their details.

### Update Student

Navigate to the "Update Student" page to modify the information of an existing student by providing their roll number and the new details.

## Project Structure

```
students-information-system/
├── app.py
├── static/
│   └── styles.css
├── templates/
│   ├── add_student.html
│   ├── base.html
│   ├── home.html
│   ├── remove_student.html
│   ├── search_student.html
│   └── view_all_students.html
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com).

---

Thank you for using the Students Information System!
