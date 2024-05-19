# Email-Filtering-App
The purpose of this project is to filter incoming emails to a specific email address by recipient, process emails containing specific keywords, and save them to a MongoDB database with appropriate tags. A user interface has been created using the Flask web framework, and ETL (Extract, Transform, Load) operations have been performed based on the information provided by the user through this interface.

2. Method Explanation and Details
The project has been developed using the Python programming language and includes the following steps:

Data Extraction (Extract): Connects to the email server to retrieve all incoming emails.
Data Transformation (Transform): Filters and tags the email content based on specified keywords.
Data Loading (Load): Saves the tagged emails to the MongoDB database.
3. Application Steps
Setting Up the Flask Application: A web application has been created using the Flask, Flask-WTF, and Flask-PyMongo libraries.
Form Input: The user fills out a form with their email address, password, and keywords.
Downloading Emails: Emails are downloaded from the email server using the IMAP protocol.
ETL Operations: Emails are filtered based on the specified keywords and saved to MongoDB.
Displaying Results: A notification is shown to the user when the process is complete.
4. Pipeline Flow
The pipeline consists of the following steps:

Input: Collects the email address, password, and keywords from the user.
Data Extraction: Connects to the email server to retrieve emails.
Data Transformation: Filters and tags the emails based on the specified keywords.
Data Loading: Saves the tagged emails to the MongoDB database.
Output: Shows a notification to the user when the process is complete.
5. Data Input and Output at Each Pipeline Step
Input: User information (email address, password, keywords)
Data Extraction: Emails downloaded via IMAP
Data Transformation: Filtered and tagged emails
Data Loading: Emails saved to MongoDB
Output: Notification shown to the user
