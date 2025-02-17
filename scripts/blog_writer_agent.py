import os
from dotenv import load_dotenv
from browser_use import Browser
from datetime import datetime

from linkedin_best_post import LinkedinBestPost
from blog_writer import BlogWriter
from emailing import Email

## LinkedIn & OpenAI Configurations

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_SEARCH_TOPIC = os.getenv("LINKEDIN_SEARCH_TOPIC")

# Email/SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_LOGIN = os.getenv("EMAIL_LOGIN")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")



def main():

    print("Browser Initiated....!")
    # Initialize the browser (using browser-use)
    # browser = Browser(headless=True)  # Headless mode; set to False if you need to debug
    browser = Browser()

    print("linkedin_best_post Initiated....!")
    # Initialize the LinkedinBestPost (To login to linkedin and get the best post)
    linkedin_best_post = LinkedinBestPost(browser,
    LINKEDIN_USERNAME, LINKEDIN_PASSWORD, LINKEDIN_SEARCH_TOPIC)

    # # --- Step 1: Log in to LinkedIn ---
    # login_linkedin(browser, LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    #
    # # --- Step 2: Search for GenAI/LLM posts ---
    # search_topic = "Genai LLM"
    # best_post = search_linkedin_for_topic(browser, search_topic)

    if not linkedin_best_post:
        print("No suitable LinkedIn post found.")
        browser.quit()
        return

    print("BlogWriter Initiated....!")
    # Initialize BlogWriter (To write the blog post)
    blog_writer = BlogWriter(OPENAI_API_KEY)
    blog_article = blog_writer.generate_blog_article("Genai and LLM", linkedin_best_post)

    # # --- Step 3: Generate the blog article using OpenAI ---
    # article = generate_blog_article("Genai and LLM", best_post)

    # --- Step 4: Convert the article to PDF ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf = f"blog_article_{timestamp}.pdf"
    blog_writer.convert_article_to_pdf(article, output_pdf)
    print("PDF Saved....!")

    # --- Step 5: Email the PDF ---
    emailing = Email()

    email_subject = "Your Generated Blog Article"
    email_body = "Attached is the in-depth blog article generated from your LinkedIn post."
    emailing.send_email_with_attachment(
        sender=SENDER_EMAIL,
        recipient=RECIPIENT_EMAIL,
        subject=email_subject,
        body=email_body,
        attachment_path=output_pdf,
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        login=EMAIL_LOGIN,
        password=EMAIL_PASSWORD,
    )

    print("Blog article generated and emailed successfully.")
    browser.quit()

if __name__ == "__main__":
    main()
