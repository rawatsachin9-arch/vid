import os
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration from environment variables
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL')
SMTP_FROM_NAME = os.environ.get('SMTP_FROM_NAME', 'VideoAI')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

async def send_email(to_email: str, subject: str, html_content: str, text_content: str = None):
    """
    Send an email using SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text fallback (optional)
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        raise Exception("Email configuration not set. Please configure SMTP settings.")
    
    # Create message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    message['To'] = to_email
    
    # Add plain text version
    if text_content:
        text_part = MIMEText(text_content, 'plain')
        message.attach(text_part)
    
    # Add HTML version
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)
    
    # Send email
    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        raise


async def send_password_reset_email(to_email: str, reset_token: str, user_name: str = None):
    """
    Send password reset email with reset link
    
    Args:
        to_email: User's email address
        reset_token: Password reset token
        user_name: User's name (optional)
    """
    # Create reset link
    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"
    
    # Email subject
    subject = "Reset Your VideoAI Password"
    
    # HTML email template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 8px;
            }}
            h1 {{
                color: #667eea;
                margin-top: 0;
                font-size: 24px;
            }}
            .button {{
                display: inline-block;
                padding: 14px 32px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .warning {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 12px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: white;
                font-size: 14px;
            }}
            .logo {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .logo-text {{
                color: white;
                font-size: 28px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <div class="logo-text">🎬 VideoAI</div>
            </div>
            
            <div class="content">
                <h1>Reset Your Password</h1>
                
                <p>Hi{' ' + user_name if user_name else ''},</p>
                
                <p>We received a request to reset your password for your VideoAI account. Click the button below to create a new password:</p>
                
                <div style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </div>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #667eea; font-size: 14px;">{reset_link}</p>
                
                <div class="warning">
                    <strong>⏰ Important:</strong> This link will expire in 15 minutes for security reasons.
                </div>
                
                <p><strong>Didn't request this?</strong><br>
                If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
                
                <p style="margin-top: 30px; color: #666; font-size: 14px;">
                    Best regards,<br>
                    The VideoAI Team
                </p>
            </div>
            
            <div class="footer">
                <p>This is an automated message, please do not reply.</p>
                <p>&copy; 2024 VideoAI. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_content = f"""
    Reset Your VideoAI Password
    
    Hi{' ' + user_name if user_name else ''},
    
    We received a request to reset your password for your VideoAI account.
    
    Click this link to reset your password:
    {reset_link}
    
    This link will expire in 15 minutes for security reasons.
    
    If you didn't request a password reset, you can safely ignore this email.
    
    Best regards,
    The VideoAI Team
    """
    
    # Send the email
    await send_email(to_email, subject, html_content, text_content)


async def send_password_changed_notification(to_email: str, user_name: str = None):
    """
    Send notification email when password is successfully changed
    
    Args:
        to_email: User's email address
        user_name: User's name (optional)
    """
    subject = "Your VideoAI Password Was Changed"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                padding: 40px 30px;
                border-radius: 10px;
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 8px;
            }}
            h1 {{
                color: #28a745;
                margin-top: 0;
            }}
            .success-icon {{
                text-align: center;
                font-size: 48px;
                margin-bottom: 20px;
            }}
            .alert {{
                background: #d1ecf1;
                border-left: 4px solid #0c5460;
                padding: 12px;
                margin: 20px 0;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <div class="success-icon">✅</div>
                <h1>Password Changed Successfully</h1>
                
                <p>Hi{' ' + user_name if user_name else ''},</p>
                
                <p>This is to confirm that your VideoAI account password was successfully changed.</p>
                
                <div class="alert">
                    <strong>🔒 Security Notice:</strong> If you didn't make this change, please contact our support team immediately.
                </div>
                
                <p>You can now log in to your account using your new password.</p>
                
                <p style="margin-top: 30px; color: #666; font-size: 14px;">
                    Best regards,<br>
                    The VideoAI Team
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Password Changed Successfully
    
    Hi{' ' + user_name if user_name else ''},
    
    This is to confirm that your VideoAI account password was successfully changed.
    
    If you didn't make this change, please contact our support team immediately.
    
    Best regards,
    The VideoAI Team
    """
    
    await send_email(to_email, subject, html_content, text_content)
