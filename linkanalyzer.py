import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import click
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from texttable import Texttable
from textblob import TextBlob
import re
import logging

console = Console()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_welcome_banner():
    banner_text = Text("Welcome to the News Link Analyzer!", style="bold magenta")
    console.print(Panel(banner_text, title="Welcome", title_align="center", border_style="cyan"))

def extract_page_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "No Title"
        description = soup.find("meta", attrs={"name": "description"})
        description_content = description['content'] if description else "No Description"

        paragraphs = soup.find_all('p')
        text_content = ' '.join([para.get_text() for para in paragraphs])

        return {
            "title": title,
            "description": description_content,
            "text": text_content,
            "html": response.text
        }
    except requests.RequestException as e:
        logging.error(f"Error accessing the URL: {e}")
        console.print(f"[bold red]Error accessing the URL:[/bold red] {e}")
        return None

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

def detect_tracking_scripts(html):
    tracking_scripts = [
        r"google-analytics\.com",
        r"facebook\.com",
        r"analytics\.js",
        r"track\.js",
        r"mixpanel\.com",
        r"segment\.com"
    ]

    for script in tracking_scripts:
        if re.search(script, html):
            return True
    return False

def detect_external_links(soup):
    external_links = []
    for link in soup.find_all('a', href=True):
        if not link['href'].startswith('#') and not link['href'].startswith('/'):
            external_links.append(link['href'])

    return external_links

def train_model(data, labels):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data)
    model = MultinomialNB()
    model.fit(X, labels)
    return model, vectorizer

def predict_ip_identification(model, vectorizer, text):
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)
    return prediction[0]

def ask_to_exit():

    console.print("[bold yellow]Do you want to exit the tool? (y/n)[/bold yellow]")
    choice = console.input("Enter your choice: ").strip().lower()
    return choice in ['y', 'yes']

@click.command()
@click.option('--url', prompt='News URL', help='The link to the news article to be analyzed.')
def cli(url):

    display_welcome_banner()

    training_data = [
        "This site collects user data.",
        "We do not track personal information.",
        "We are committed to user privacy.",
        "We collect information to improve our services."
    ]

    labels = [1, 0, 0, 1]  # 1 for tracking, 0 for no tracking

    model, vectorizer = train_model(training_data, labels)

    console.print(f"[bold blue]Extracting information from the URL:[/bold blue] {url}")
    page_info = extract_page_info(url)

    if page_info:
        console.print(f"[bold green]Title:[/bold green] {page_info['title']}")
        console.print(f"[bold green]Description:[/bold green] {page_info['description']}")

        sentiment, subjectivity = analyze_sentiment(page_info['text'])
        sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
        console.print(f"[bold green]Text Sentiment:[/bold green] {sentiment_label} (Polarity: {sentiment:.2f}, Subjectivity: {subjectivity:.2f})")

        if detect_tracking_scripts(page_info['html']):
            console.print("[bold red]The page contains known tracking scripts.[/bold red]")
        else:
            console.print("[bold green]No known tracking scripts found.[/bold green]")

        external_links = detect_external_links(BeautifulSoup(page_info['html'], 'html.parser'))
        if external_links:
            console.print("[bold yellow]External links found:[/bold yellow]")
            for link in external_links:
                console.print(f" - {link}")

        console.print("[bold blue]Analyzing the extracted text...[/bold blue]")
        result = predict_ip_identification(model, vectorizer, page_info['text'])

        if result == 1:
            console.print("[bold red]The IP may be tracked.[/bold red]")
        else:
            console.print("[bold green]No indication of IP tracking.[/bold green]")

    if ask_to_exit():
        console.print("[bold green]Thank you for using the News Link Analyzer! Goodbye![/bold green]")
    else:
        console.print("[bold blue]You can analyze another URL by running the tool again.[/bold blue]")

if __name__ == '__main__':
    cli()
