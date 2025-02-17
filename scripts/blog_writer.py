
import openai
import pdfkit

class BlogWriter():

    def __init__(self, api_key):

        self.api_key = api_key

    def generate_blog_article(self, topic, post_content):
        """
        Use the OpenAI API to generate an in-depth blog article.
        The prompt includes the content from the best LinkedIn post.
        """
        openai.api_key = self.api_key
        prompt = (
            f"Based on the following LinkedIn post content:\n\n{post_content}\n\n"
            f"Write an in-depth blog article about {topic}."
        )
        response = openai.Completion.create(
            engine="text-davinci-003",  # or your chosen model
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7,
        )
        article = response.choices[0].text.strip()
        return article

    def convert_article_to_pdf(article_text, output_pdf):
        """
        Convert the article text to a PDF file using pdfkit.
        This uses an HTML template; ensure wkhtmltopdf is installed.
        """
        html_content = f"""
        <html>
          <head>
            <meta charset="utf-8">
            <title>Blog Article</title>
          </head>
          <body>
            <h1>In-Depth Blog Article</h1>
            <div>{article_text.replace('\n', '<br>')}</div>
          </body>
        </html>
        """
        pdfkit.from_string(html_content, output_pdf)
