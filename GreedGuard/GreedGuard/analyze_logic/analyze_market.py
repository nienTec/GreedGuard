from data.fear_and_greed import fetch_fear_and_greed_index
from data.indices import fetch_index_changes
from data.vix import vix_value
from utils.email_sender import send_html_email


# from utils.database import insert_market_analysis  # optional for saving results

def analyze_market():
    """
    Conducts a market analysis based on Fear and Greed Index, major indices, and VIX.
    """
    score = 0
    results = {}

    # 1. Analyze Fear and Greed Index
    fear_and_greed_data = fetch_fear_and_greed_index()
    if fear_and_greed_data:
        current_value = fear_and_greed_data.get("current", 50)
        if current_value < 20:
            score += 4
            results["Fear and Greed"] = f"Extreme fear ({current_value}) → +4 point"
        elif current_value > 80:
            score -= 4
            results["Fear and Greed"] = f"Extreme greed ({current_value}) → -4 point"
        else:
            results["Fear and Greed"] = f"Neutral sentiment ({current_value}) → 0 points"

    # 2. Analyze major indices
    index_changes = fetch_index_changes()
    for index, data in index_changes.items():
        index_score = calculate_index_score(data)
        score += index_score

        if index_score > 0:
            results[index] = f"Negative trend → +{index_score} point(s)"
        elif index_score < 0:
            results[index] = f"Positive trend → {index_score} point(s)"
        else:
            results[index] = f"Neutral trend → 0 points"

    # 3. Analyze VIX
    vix_data = vix_value()

    if vix_value is not None:
        if vix_data > 30:
            score += 4
            results["VIX"] = f"High volatility ({vix_data}) → +4 point"
        elif vix_data < 20:
            score -= 4
            results["VIX"] = f"Low volatility ({vix_data}) → -4 point"
        else:
            results["VIX"] = f"Normal volatility ({vix_data}) → 0 points"

    # Summary
    print("=== Market Analysis Report ===")
    for category, evaluation in results.items():
        print(f"{category}: {evaluation}")

    print(f"\nTotal Score: {score}")

    # Optional: Save to database
    # insert_market_analysis(results, score)

    return score, results

def calculate_index_score(index_data: dict) -> int:
    """
    Calculates a smart score for a single index based on its short-term and long-term movements.
    Returns an integer score.
    """
    score = 0

    # 1-day change (short-term shock detection)
    if index_data["value_change_24h"] is not None:
        if index_data["value_change_24h"] <= -2:
            score += 1  # Sharp drop in 1 day → positive for buying
        elif index_data["value_change_24h"] >= 2:
            score -= 1  # Sharp rise in 1 day → negative for buying

    # 7-day change (short-term trend)
    if index_data["value_change_week"] is not None:
        if index_data["value_change_week"] <= -3:
            score += 1  # Downtrend over 1 week → more panic
        elif index_data["value_change_week"] >= 3:
            score -= 1  # Uptrend over 1 week → more greed

    # 30-day change (medium-term trend)
    if index_data["value_change_month"] is not None:
        if index_data["value_change_month"] <= -5:
            score += 1  # Market crashed last month → opportunity
        elif index_data["value_change_month"] >= 5:
            score -= 1  # Strong rally → maybe overheated

    # Optional: Compare current value to 120-day average
    if index_data.get("average_120d") and index_data["value"] is not None:
        if index_data["value"] < index_data["average_120d"]:
            score += 1  # Trading below long-term average → market is cheap
        else:
            score -= 1  # Trading above long-term average → expensive

    return score

def build_html_email(score, results):
    html = """
    <html>
      <body>
        <h2 style="color: #4CAF50;">🚀 Daily Market Analysis Report</h2>
        <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse;">
          <tr>
            <th>Category</th>
            <th>Result</th>
          </tr>
    """
    for category, evaluation in results.items():
        html += f"""
          <tr>
            <td>{category}</td>
            <td>{evaluation}</td>
          </tr>
        """
    html += f"""
        </table>
        <p><b>Total Score:</b> {score}</p>
    """

    # Add a final comment
    if score >= 20:
        html += "<p>📈 <i>Summary: Very Good buying opportunity detected!</i></p>"
    elif score >= 14:
        html += "<p>📉 <i>Summary: Good buying opportunity detected!</i></p>"
    elif score <= -14:
        html += "<p>📉 <i>Summary: Medium risk, be cautious!</i></p>"
    elif score <= -20:
        html += "<p>📉 <i>Summary: High risk, be cautious!</i></p>"
    else:
        html += "<p>😐 <i>Summary: Neutral market conditions.</i></p>"

    html += """
      </body>
    </html>
    """
    return html

if __name__ == "__main__":
    score, results = analyze_market()
    html_content = build_html_email(score, results)

    subject = "🚀 Daily Market Analysis Report"
    send_html_email(subject, html_content, "xxx@gmx.de")
