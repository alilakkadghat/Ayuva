from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
# A secret key is needed for flash messages and session management
app.config['SECRET_KEY'] = 'a_very_secure_and_random_string_here'

@app.route('/')
def home():
    """Renders the main landing page."""
    return render_template('app.html')

@app.route('/join_waitlist', methods=['POST'])
def join_waitlist():
    """Handles the waitlist form submission."""
    
    # Get the email from the form data
    email = request.form.get('email')
    
    if email:
        # A simple file-based "database" to log emails
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('waitlist.log', 'a') as f:
            f.write(f'Email: {email}, Timestamp: {timestamp}\n')
            
        flash("Thanks for joining the waitlist! We'll be in touch.")
    else:
        flash("Please enter a valid email address.", "error") # You can add a class for error styling
        
    return redirect(url_for('home'))

# This is for running the app.
if __name__ == '__main__':
    # Running in debug mode reloads the server automatically on code changes
    # Set debug=False in production
    app.run(debug=True)