- This tool uses advanced machine learning and natural language processing techniques to provide valuable insights into the content and privacy practices of news sites.

![lino_AI](https://github.com/user-attachments/assets/fd146e64-4ef1-4d77-be21-30650e947b0a)

# Main Features
- Extracting information from web pages
- Content sentiment analysis
- Detection of known tracking scripts
- Identification of potentially suspicious external links
- IP Tracking Prediction Using Machine Learning

Requirements

- Python 3.7 or higher

# Installation

Clone this repository:

        git clone https://github.com/mrfelpa/LinkAnalyzer.git
        

        cd news-link-analyzer

- Install dependencies:

        pip install -r requirements.txt

# Use

- To analyze a news link, run the following command:

        python linkanalyzer.py --url https://exemplo.com/news

  - You can also run the script without arguments, and it will request the URL interactively:

        python linkanalyzer.py

# Machine Learning Model

- The script uses ***a Naive Bayes Multinomial classifier*** trained with an example dataset, this model is used to predict whether a page might be tracking the user's IP based on the extracted text.

- You can tune the machine learning model by modifying the training data in the ***train_model functio***, add more examples to improve prediction accuracy.

# Contributions

- We value contributions from the community, if you have any questions or suggestions, please open an issue
