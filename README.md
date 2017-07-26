# ORM_Database
This assessment aims at modelling the reports, users, and loans that exist in the system and their relationship to one another, using SQLAlchemy, in __less than 3 hours__.

The amount of time spent on this assessment, and more, can be seen in [WakaTime](https://wakatime.com/@87c944a3-0f51-4430-a9b3-a0166c995bb5/projects/bqfmzrummg?start=2017-07-20&end=2017-07-26)

## Documentation
See the documentation [here](docs/index.md).

## About
The goal of this exercise is to see:
1. What your "production" level code looks like (OO, Documentation, etc)
2. How you ensure that the code actually works as expected (Testing)
3. How you respond to tight deadlines (Which sacrifices you make)
4. Your approach and creativity to crafting a solution

## The Task
Model the reports, users, and loans that exist in the system and their relationship to one another, using SQLAlchemy (or any
ORM you prefer). As a starting point, your PM has given you the following attributes that belong to these items:

### User
#### Name
The first and last name of the user
Max 255 characters
Cannot be empty

### Loan
#### Currency
Can only have a value of USD, GBP, or JPY
#### Balance
The amount of money that the loan is for
Must always have a value of zero or higher


### Report
#### Title
A short description of the report, max 255 characters, cannot be empty
#### Body
The actual report text, Max 5MB
#### Author
A user who created the report, cannot be empty
#### Loans
A list of loans that are associated with this particular report
- N.B. A loan may be referenced by multiple reports

## Milestones
1. Create suitable SQLA models to represent the objects listed above and their relationships to one another
2. Write unit-test that seeds a database (SQLite) with sample data for each type
3. Write a test case that ensures the relationships work as expected
4. Write a test case for finding all reports that a loan belongs to
5. Write a test case for calculating the sum of all loans that went into a specific report
