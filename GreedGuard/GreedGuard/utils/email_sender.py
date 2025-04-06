import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_html_email(subject, html_content, to_email):
    from_email = "xxx@gmail.com"
    password = "xxxx"

    # Create the email container (multipart)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    # Attach the HTML content
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    # Connect to the Gmail SMTP server and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())


if __name__ == "__main__":
    subject = "🚀 Daily Market Analysis Report"

    html_content = """
    <html>
      <body>
        <h2 style="color: #4CAF50;">Market Analysis Report</h2>
        <p>Here is today's market status:</p>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse;">
          <tr>
            <th>Category</th>
            <th>Result</th>
          </tr>
          <tr>
            <td>Fear and Greed</td>
            <td>Extreme fear (15) → +1 point</td>
          </tr>
          <tr>
            <td>S&P 500</td>
            <td>Negative trend → +2 points</td>
          </tr>
          <tr>
            <td>VIX</td>
            <td>High volatility (32.4) → +1 point</td>
          </tr>
        </table>
        <p><b>Total Score:</b> +4</p>
        <p>📈 <i>Summary: Good buying opportunity detected!</i></p>
      </body>
    </html>
    """

    send_html_email(subject, html_content, "xxx@gmx.de")
