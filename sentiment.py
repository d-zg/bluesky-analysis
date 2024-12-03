from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_sentiment_analyzer = None

def get_analyzer():
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentIntensityAnalyzer()
    return _sentiment_analyzer

def vader_sentiment(text):
    """
    Analyzes the sentiment of the given text using VADER.

    Parameters:
    text (str): The text to analyze.

    Returns:
    float: The compound sentiment score.
    """
    if not isinstance(text, str) or not text.strip():
        # raise ValueError("Input must be a non-empty string")
        return 0
    analyzer = get_analyzer()
    return analyzer.polarity_scores(text)['compound']
