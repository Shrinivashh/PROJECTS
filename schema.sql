CREATE USER 'v'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON v.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;


CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Student_info (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE
);

CREATE TABLE IF NOT EXISTS Students_subject (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Student_marks (
    mark_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    subject_id INT,
    marks INT,
    FOREIGN KEY (student_id) REFERENCES Student_info(student_id),
    FOREIGN KEY (subject_id) REFERENCES Students_subject(subject_id)
);

DELIMITER //
CREATE PROCEDURE AddStudent(IN fname VARCHAR(50), IN lname VARCHAR(50), IN dob DATE)
BEGIN
    INSERT INTO Student_info (first_name, last_name, date_of_birth) VALUES (fname, lname, dob);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddSubject(IN sname VARCHAR(100))
BEGIN
    INSERT INTO Students_subject (subject_name) VALUES (sname);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddStudentMark(IN stid INT, IN subid INT, IN mark INT)
BEGIN
    INSERT INTO Student_marks (student_id, subject_id, marks) VALUES (stid, subid, mark);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetStudentDetails(IN stid INT)
BEGIN
    SELECT s.student_id, s.first_name, s.last_name, s.date_of_birth, 
           ss.subject_name, sm.marks
    FROM Student_info s
    LEFT JOIN Student_marks sm ON s.student_id = sm.student_id
    LEFT JOIN Students_subject ss ON sm.subject_id = ss.subject_id
    WHERE s.student_id = stid
