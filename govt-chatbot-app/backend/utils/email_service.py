import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from datetime import datetime

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.sender_email = os.getenv('SENDER_EMAIL')

    def send_email(self, to_email, subject, template_name, template_data):
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Load and render email template
            template_path = os.path.join('templates', 'emails', f'{template_name}.html')
            with open(template_path, 'r') as file:
                template = Template(file.read())
                html_content = template.render(**template_data)

            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))

            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_welcome_email(self, user):
        template_data = {
            'username': user.username,
            'login_url': f"{os.getenv('FRONTEND_URL')}/login"
        }
        return self.send_email(
            user.email,
            'Welcome to Government Schemes Portal',
            'welcome',
            template_data
        )

    def send_password_reset_email(self, user, reset_token):
        template_data = {
            'username': user.username,
            'reset_url': f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"
        }
        return self.send_email(
            user.email,
            'Password Reset Request',
            'password_reset',
            template_data
        )

    def send_new_scheme_notification(self, user, scheme):
        template_data = {
            'username': user.username,
            'scheme_name': scheme.name,
            'scheme_description': scheme.description,
            'scheme_url': f"{os.getenv('FRONTEND_URL')}/schemes/{scheme._id}"
        }
        return self.send_email(
            user.email,
            f'New Government Scheme: {scheme.name}',
            'new_scheme',
            template_data
        )

# Create email templates directory and files
def create_email_templates():
    templates_dir = os.path.join('templates', 'emails')
    os.makedirs(templates_dir, exist_ok=True)

    # Welcome email template
    welcome_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .button { 
                display: inline-block;
                padding: 10px 20px;
                background-color: #1976d2;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Welcome to Government Schemes Portal!</h2>
            <p>Dear {{ username }},</p>
            <p>Thank you for registering with the Government Schemes Portal. We're excited to have you on board!</p>
            <p>You can now:</p>
            <ul>
                <li>Browse available government schemes</li>
                <li>Get instant answers through our chatbot</li>
                <li>Receive notifications about new schemes</li>
            </ul>
            <p>
                <a href="{{ login_url }}" class="button">Login to Your Account</a>
            </p>
            <p>Best regards,<br>Government Schemes Portal Team</p>
        </div>
    </body>
    </html>
    """

    # Password reset template
    password_reset_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .button { 
                display: inline-block;
                padding: 10px 20px;
                background-color: #1976d2;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Password Reset Request</h2>
            <p>Dear {{ username }},</p>
            <p>We received a request to reset your password. Click the button below to create a new password:</p>
            <p>
                <a href="{{ reset_url }}" class="button">Reset Password</a>
            </p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>Best regards,<br>Government Schemes Portal Team</p>
        </div>
    </body>
    </html>
    """

    # New scheme notification template
    new_scheme_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .button { 
                display: inline-block;
                padding: 10px 20px;
                background-color: #1976d2;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>New Government Scheme Available</h2>
            <p>Dear {{ username }},</p>
            <p>A new government scheme has been added that might interest you:</p>
            <h3>{{ scheme_name }}</h3>
            <p>{{ scheme_description }}</p>
            <p>
                <a href="{{ scheme_url }}" class="button">Learn More</a>
            </p>
            <p>Best regards,<br>Government Schemes Portal Team</p>
        </div>
    </body>
    </html>
    """

    # Write templates to files
    with open(os.path.join(templates_dir, 'welcome.html'), 'w') as f:
        f.write(welcome_template)
    
    with open(os.path.join(templates_dir, 'password_reset.html'), 'w') as f:
        f.write(password_reset_template)
    
    with open(os.path.join(templates_dir, 'new_scheme.html'), 'w') as f:
        f.write(new_scheme_template)

# Create email templates when module is imported
create_email_templates() 