def calculate_scores(total_words, filler_count, sentiment_score):

    confidence_score = max(0, 100 - (filler_count * 2))

    communication_score = min(100, total_words)

    sentiment_percentage = abs(sentiment_score * 100)

    overall_score = (
        confidence_score +
        communication_score +
        sentiment_percentage
    ) / 3

    return {
        "confidence": round(confidence_score, 2),
        "communication": round(communication_score, 2),
        "sentiment": round(sentiment_percentage, 2),
        "overall": round(overall_score, 2)
    }