from textblob import TextBlob

def analyze_sentiment(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive", polarity

    elif polarity < 0:
        return "Negative", polarity

    else:
        return "Neutral", polarity