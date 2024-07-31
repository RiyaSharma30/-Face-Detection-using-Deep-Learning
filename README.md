 Face Recognition System for Missing Persons

 Introduction
The exponential growth of face recognition technology has become crucial in addressing global concerns about missing persons. Every day, numerous individuals disappear due to human trafficking, forced labor, and exploitation, necessitating efficient identification systems. Advanced facial recognition techniques compare the facial features of missing individuals with those in a database, generating potential matches ranked by similarity scores. This ensures precise identification, even when individuals have undergone significant changes or disguises. Developed using Flask, a lightweight web application framework, and dlib, a high-performance library for machine learning and computer vision, the system offers scalability, reliability, and real-time responsiveness.

 Installation and Execution Steps
 Prerequisites
- Python 3.9 or later
- Flask
- dlib
- Twilio account
- Other dependencies listed in `requirements.txt`

### Files Provided
- `dlib-19.22.99-cp39-cp39-win_amd64.whl`: The dlib library for Windows.
- `final1.py`: The main Python script for the face recognition system.

Setup Instructions

1. Create a Virtual Environment (Optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

2. Install Flask
   ```sh
   pip install Flask
   ```

3. Install dlib
   ```sh
   pip install /mnt/data/dlib-19.22.99-cp39-cp39-win_amd64.whl
   ```

4. Install Other Dependencies
   Make sure to have a `requirements.txt` file with the necessary dependencies. If not, you can install them manually as needed.
   ```sh
   pip install -r requirements.txt
   ```

5. Run the Application
   ```sh
   python /mnt/data/final1.py
   ```

### Activating Twilio Account

1. Sign Up for Twilio
   - Go to the [Twilio Sign Up page](https://www.twilio.com/try-twilio).
   - Fill in the required details to create an account.

2. Verify Your Account
   - Follow the instructions to verify your email and phone number.
   - You might need to enter a code sent to your phone to complete the verification process.

3. Get Your Twilio Credentials
   - After logging in, go to the [Twilio Console](https://www.twilio.com/console).
   - Find your `Account SID` and `Auth Token` on the dashboard. These credentials will be needed for API calls.

4. Set Up a Twilio Phone Number
   - In the Twilio Console, navigate to `Phone Numbers` and click on `Get a Number`.
   - Follow the prompts to select and configure a phone number.

5. Install Twilio Python Library
   ```sh
   pip install twilio
   ```

6. Configure Twilio in Your Application
   - Add your Twilio `Account SID`, `Auth Token`, and phone number to your application's configuration settings or environment variables.
   - Use the Twilio Python library in your script to send messages or make calls.

Usage
- Open your web browser and navigate to the address provided by Flask (usually `http://127.0.0.1:5000`).
- Use the web interface to upload images or stream live video feeds.
- The system will process the input and provide potential matches from the database, ranked by similarity scores.

Contributing
If you wish to contribute to the project, please fork the repository and submit a pull request.


 Acknowledgments
- Flask: For providing a lightweight web application framework.
- dlib: For offering a robust library for machine learning and computer vision tasks.
- Twilio: For enabling seamless communication capabilities.

