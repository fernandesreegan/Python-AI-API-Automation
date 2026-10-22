from openai import OpenAI
from dotenv import load_dotenv
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env
load_dotenv()
client = OpenAI()

print("Generating daily AI news summary...")

# 1. Generate the AI News Summary
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a tech journalist who provides concise, bulleted daily briefings on artificial intelligence developments."},
        {"role": "user", "content": "Give me a brief summary of the latest trends, agentic workflows, or major model releases in AI from the past day."}
    ]
)
news_summary = response.choices[0].message.content
today_date = datetime.date.today().isoformat()

# 2. Set up email details
sender_email = os.getenv("GMAIL_USER")
app_password = os.getenv("GMAIL_APP_PASSWORD")
receiver_email = sender_email  # Sending it to yourself

# Build the email structure
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = f"🤖 Daily AI News Briefing - {today_date}"

# Combine the text body
body = f"Here is your automated daily AI news briefing:\n\n{news_summary}"
msg.attach(MIMEText(body, "plain"))

# 3. Connect to Gmail and send the email
try:
    print("Sending email via Gmail...")
    # Connect securely to Gmail's SMTP server using SSL on port 465
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Success! Daily AI news email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")