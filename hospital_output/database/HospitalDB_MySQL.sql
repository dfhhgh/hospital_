-- ============================================================
--  HospitalDB  –  MySQL 8+ compatible script
--  Converted from SQL Server (HospitalDB_2)
--  For use with Flask / SQLAlchemy
-- ============================================================

-- Create & select the database
CREATE DATABASE IF NOT EXISTS HospitalDB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE HospitalDB;

-- Disable FK checks during table creation to avoid ordering issues
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- 1. Person
--    Root table; no FK dependencies.
-- ============================================================
CREATE TABLE Person (
    PersonID    INT            NOT NULL AUTO_INCREMENT,
    FirstName   VARCHAR(100)   NOT NULL,
    LastName    VARCHAR(100)   NOT NULL,
    Gender      VARCHAR(10)    NULL,
    Email       VARCHAR(150)   NULL,
    Phone       VARCHAR(20)    NULL,
    Address     VARCHAR(255)   NULL,
    PRIMARY KEY (PersonID),
    INDEX idx_person_email (Email),
    INDEX idx_person_phone (Phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 2. Department
-- ============================================================
CREATE TABLE Department (
    DepartmentID INT           NOT NULL AUTO_INCREMENT,
    Name         VARCHAR(100)  NOT NULL,
    Location     VARCHAR(100)  NULL,
    PRIMARY KEY (DepartmentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 3. Specialties
-- ============================================================
CREATE TABLE Specialties (
    SpecialtyID INT           NOT NULL AUTO_INCREMENT,
    Name        VARCHAR(100)  NULL,
    PRIMARY KEY (SpecialtyID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 4. Medicine
-- ============================================================
CREATE TABLE Medicine (
    MedicineID  INT           NOT NULL AUTO_INCREMENT,
    Name        VARCHAR(100)  NULL,
    Description TEXT          NULL,
    PRIMARY KEY (MedicineID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 5. AppointmentStatus
-- ============================================================
CREATE TABLE AppointmentStatus (
    StatusID   INT          NOT NULL AUTO_INCREMENT,
    StatusName VARCHAR(50)  NULL,
    PRIMARY KEY (StatusID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 6. Patient   (references Person)
-- ============================================================
CREATE TABLE Patient (
    PersonID    INT         NOT NULL,
    DateOfBirth DATE        NULL,
    BloodType   VARCHAR(5)  NULL,
    PRIMARY KEY (PersonID),
    INDEX idx_patient_dob   (DateOfBirth),
    INDEX idx_patient_blood (BloodType),
    CONSTRAINT fk_patient_person FOREIGN KEY (PersonID)
        REFERENCES Person (PersonID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 7. Employee  (references Person, Department)
-- ============================================================
CREATE TABLE Employee (
    EmployeeID   INT            NOT NULL AUTO_INCREMENT,
    PersonID     INT            NOT NULL,
    DepartmentID INT            NULL,
    HireDate     DATE           NULL,
    Salary       DECIMAL(10,2)  NULL,
    JobTitle     VARCHAR(100)   NULL,
    PRIMARY KEY (EmployeeID),
    UNIQUE KEY uq_employee_person (PersonID),
    INDEX idx_employee_department (DepartmentID),
    INDEX idx_employee_person     (PersonID),
    CONSTRAINT fk_employee_person     FOREIGN KEY (PersonID)
        REFERENCES Person     (PersonID),
    CONSTRAINT fk_employee_department FOREIGN KEY (DepartmentID)
        REFERENCES Department (DepartmentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 8. Doctor    (references Employee, Specialties)
--    NOTE: NVARCHAR → VARCHAR(500); BIT → TINYINT(1)
--    ProfileImage: VARBINARY(MAX) → LONGBLOB
-- ============================================================
CREATE TABLE Doctor (
    EmployeeID      INT            NOT NULL,
    SpecialtyID     INT            NULL,
    Bio             VARCHAR(500)   NULL,
    ExperienceYears INT            NULL,
    Rating          DECIMAL(2,1)   NULL,
    IsAvailable     TINYINT(1)     NULL DEFAULT 1,
    ProfileImage    LONGBLOB       NULL,
    PRIMARY KEY (EmployeeID),
    INDEX idx_doctor_specialty (SpecialtyID),
    CONSTRAINT fk_doctor_employee  FOREIGN KEY (EmployeeID)
        REFERENCES Employee   (EmployeeID),
    CONSTRAINT fk_doctor_specialty FOREIGN KEY (SpecialtyID)
        REFERENCES Specialties (SpecialtyID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 9. Nurse     (references Employee)
-- ============================================================
CREATE TABLE Nurse (
    EmployeeID INT          NOT NULL,
    Shift      VARCHAR(50)  NULL,
    PRIMARY KEY (EmployeeID),
    INDEX idx_nurse_shift (Shift),
    CONSTRAINT fk_nurse_employee FOREIGN KEY (EmployeeID)
        REFERENCES Employee (EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 10. Room     (references Department)
-- ============================================================
CREATE TABLE Room (
    RoomID       INT          NOT NULL AUTO_INCREMENT,
    RoomNumber   VARCHAR(20)  NULL,
    Type         VARCHAR(50)  NULL,
    Status       VARCHAR(50)  NULL,
    DepartmentID INT          NULL,
    PRIMARY KEY (RoomID),
    INDEX idx_room_department (DepartmentID),
    INDEX idx_room_status     (Status),
    CONSTRAINT fk_room_department FOREIGN KEY (DepartmentID)
        REFERENCES Department (DepartmentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 11. Users    (references Person)
-- ============================================================
CREATE TABLE Users (
    UserID       INT           NOT NULL AUTO_INCREMENT,
    PersonID     INT           NULL,
    Email        VARCHAR(150)  NOT NULL,
    PasswordHash VARCHAR(255)  NOT NULL,
    Role         VARCHAR(50)   NOT NULL,
    IsActive     TINYINT(1)    NULL DEFAULT 1,
    CreatedAt    DATETIME      NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (UserID),
    UNIQUE KEY uq_users_email    (Email),
    UNIQUE KEY uq_users_personid (PersonID),
    INDEX idx_users_email  (Email),
    INDEX idx_users_person (PersonID),
    CONSTRAINT fk_users_person FOREIGN KEY (PersonID)
        REFERENCES Person (PersonID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 12. Appointment  (references Patient, Doctor, AppointmentStatus)
--     NOTE: SQL Server TEXT → MySQL TEXT (compatible)
-- ============================================================
CREATE TABLE Appointment (
    AppointmentID   INT           NOT NULL AUTO_INCREMENT,
    PatientID       INT           NULL,
    DoctorID        INT           NULL,
    AppointmentDate DATETIME      NULL,
    StatusID        INT           NULL,
    Notes           TEXT          NULL,
    PatientName     VARCHAR(150)  NULL,
    PatientEmail    VARCHAR(150)  NULL,
    VisitReason     VARCHAR(500)  NULL,
    AppointmentTime VARCHAR(20)   NULL,
    PRIMARY KEY (AppointmentID),
    INDEX idx_appointment_patient (PatientID),
    INDEX idx_appointment_doctor  (DoctorID),
    INDEX idx_appointment_date    (AppointmentDate),
    INDEX idx_appointment_status  (StatusID),
    CONSTRAINT fk_appointment_patient FOREIGN KEY (PatientID)
        REFERENCES Patient          (PersonID),
    CONSTRAINT fk_appointment_doctor  FOREIGN KEY (DoctorID)
        REFERENCES Doctor           (EmployeeID),
    CONSTRAINT fk_appointment_status  FOREIGN KEY (StatusID)
        REFERENCES AppointmentStatus (StatusID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 13. Admission  (references Patient, Room, Doctor)
-- ============================================================
CREATE TABLE Admission (
    AdmissionID   INT          NOT NULL AUTO_INCREMENT,
    PatientID     INT          NULL,
    RoomID        INT          NULL,
    DoctorID      INT          NULL,
    AdmissionDate DATETIME     NULL,
    DischargeDate DATETIME     NULL,
    Status        VARCHAR(50)  NULL,
    PRIMARY KEY (AdmissionID),
    INDEX idx_admission_patient (PatientID),
    INDEX idx_admission_room    (RoomID),
    INDEX idx_admission_doctor  (DoctorID),
    INDEX idx_admission_date    (AdmissionDate),
    CONSTRAINT fk_admission_patient FOREIGN KEY (PatientID)
        REFERENCES Patient (PersonID),
    CONSTRAINT fk_admission_room    FOREIGN KEY (RoomID)
        REFERENCES Room    (RoomID),
    CONSTRAINT fk_admission_doctor  FOREIGN KEY (DoctorID)
        REFERENCES Doctor  (EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 14. Bill  (references Patient, Appointment)
-- ============================================================
CREATE TABLE Bill (
    BillID        INT            NOT NULL AUTO_INCREMENT,
    PatientID     INT            NULL,
    AppointmentID INT            NULL,
    Amount        DECIMAL(10,2)  NULL,
    BillDate      DATE           NULL,
    Status        VARCHAR(50)    NULL,
    PRIMARY KEY (BillID),
    INDEX idx_bill_patient     (PatientID),
    INDEX idx_bill_appointment (AppointmentID),
    INDEX idx_bill_date        (BillDate),
    CONSTRAINT fk_bill_patient      FOREIGN KEY (PatientID)
        REFERENCES Patient     (PersonID),
    CONSTRAINT fk_bill_appointment  FOREIGN KEY (AppointmentID)
        REFERENCES Appointment (AppointmentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 15. Diagnosis  (references Patient, Doctor)
-- ============================================================
CREATE TABLE Diagnosis (
    DiagnosisID   INT   NOT NULL AUTO_INCREMENT,
    PatientID     INT   NULL,
    DoctorID      INT   NULL,
    DiagnosisText TEXT  NULL,
    DiagnosisDate DATE  NULL,
    PRIMARY KEY (DiagnosisID),
    INDEX idx_diagnosis_patient (PatientID),
    INDEX idx_diagnosis_doctor  (DoctorID),
    INDEX idx_diagnosis_date    (DiagnosisDate),
    CONSTRAINT fk_diagnosis_patient FOREIGN KEY (PatientID)
        REFERENCES Patient (PersonID),
    CONSTRAINT fk_diagnosis_doctor  FOREIGN KEY (DoctorID)
        REFERENCES Doctor  (EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 16. LabTest  (references Patient, Doctor)
-- ============================================================
CREATE TABLE LabTest (
    TestID    INT           NOT NULL AUTO_INCREMENT,
    PatientID INT           NULL,
    DoctorID  INT           NULL,
    TestName  VARCHAR(100)  NULL,
    Result    TEXT          NULL,
    TestDate  DATE          NULL,
    PRIMARY KEY (TestID),
    INDEX idx_labtest_patient (PatientID),
    INDEX idx_labtest_doctor  (DoctorID),
    INDEX idx_labtest_date    (TestDate),
    CONSTRAINT fk_labtest_patient FOREIGN KEY (PatientID)
        REFERENCES Patient (PersonID),
    CONSTRAINT fk_labtest_doctor  FOREIGN KEY (DoctorID)
        REFERENCES Doctor  (EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 17. MedicalRecord  (references Patient, Doctor)
-- ============================================================
CREATE TABLE MedicalRecord (
    RecordID  INT   NOT NULL AUTO_INCREMENT,
    PatientID INT   NULL,
    DoctorID  INT   NULL,
    VisitDate DATE  NULL,
    Notes     TEXT  NULL,
    PRIMARY KEY (RecordID),
    INDEX idx_medicalrecord_patient (PatientID),
    INDEX idx_medicalrecord_doctor  (DoctorID),
    INDEX idx_medicalrecord_date    (VisitDate),
    CONSTRAINT fk_medicalrecord_patient FOREIGN KEY (PatientID)
        REFERENCES Patient (PersonID),
    CONSTRAINT fk_medicalrecord_doctor  FOREIGN KEY (DoctorID)
        REFERENCES Doctor  (EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 18. MedicineStock  (references Medicine)
-- ============================================================
CREATE TABLE MedicineStock (
    MedicineID INT            NOT NULL,
    Quantity   INT            NULL,
    Price      DECIMAL(10,2)  NULL,
    ExpireDate DATE           NULL,
    PRIMARY KEY (MedicineID),
    INDEX idx_medicinestock_expire (ExpireDate),
    CONSTRAINT fk_medicinestock_medicine FOREIGN KEY (MedicineID)
        REFERENCES Medicine (MedicineID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 19. Prescription  (references Appointment, Doctor, Patient)
-- ============================================================
CREATE TABLE Prescription (
    PrescriptionID INT   NOT NULL AUTO_INCREMENT,
    AppointmentID  INT   NULL,
    DoctorID       INT   NULL,
    PatientID      INT   NULL,
    DateIssued     DATE  NULL,
    PRIMARY KEY (PrescriptionID),
    INDEX idx_prescription_appointment (AppointmentID),
    INDEX idx_prescription_doctor      (DoctorID),
    INDEX idx_prescription_patient     (PatientID),
    CONSTRAINT fk_prescription_appointment FOREIGN KEY (AppointmentID)
        REFERENCES Appointment (AppointmentID),
    CONSTRAINT fk_prescription_doctor      FOREIGN KEY (DoctorID)
        REFERENCES Doctor      (EmployeeID),
    CONSTRAINT fk_prescription_patient     FOREIGN KEY (PatientID)
        REFERENCES Patient     (PersonID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- 20. PrescriptionMedicine  (references Prescription, Medicine)
--     Composite PK preserved exactly.
-- ============================================================
CREATE TABLE PrescriptionMedicine (
    PrescriptionID INT           NOT NULL,
    MedicineID     INT           NOT NULL,
    Dosage         VARCHAR(100)  NULL,
    Duration       VARCHAR(100)  NULL,
    PRIMARY KEY (PrescriptionID, MedicineID),
    INDEX idx_prescriptionmedicine_prescription (PrescriptionID),
    INDEX idx_prescriptionmedicine_medicine     (MedicineID),
    CONSTRAINT fk_pm_prescription FOREIGN KEY (PrescriptionID)
        REFERENCES Prescription (PrescriptionID),
    CONSTRAINT fk_pm_medicine     FOREIGN KEY (MedicineID)
        REFERENCES Medicine     (MedicineID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- Re-enable FK checks
-- ============================================================
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- Seed: AppointmentStatus  (required for FK integrity)
-- ============================================================
INSERT INTO AppointmentStatus (StatusName) VALUES
    ('Scheduled'),
    ('Confirmed'),
    ('Completed'),
    ('Cancelled'),
    ('No Show');
