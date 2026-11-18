import os
from datetime import datetime
import pandas as pd

# 1. Read emails from a folder
email_folder = "/data/emails/"
all_emails = []

for filename in os.listdir(email_folder):
    with open(os.path.join(email_folder, filename), "r") as file:
        content = file.read()
        all_emails.append({"filename": filename, "content": content})

# 2. Process each email (this is where AI would go)
processed_data = []
for email in all_emails:
    # In a real system, you'd use an AI model or API here
    sentiment = analyze_sentiment(
        email["content"]
    )  # Returns "positive" or "negative"
    topic = extract_topic(email["content"])  # Returns topic category

    processed_data.append(
        {
            "filename": email["filename"],
            "sentiment": sentiment,
            "topic": topic,
            "date": datetime.now(),
        }
    )

# 3. Create a DataFrame for analysis
df = pd.DataFrame(processed_data)

# 4. Generate a weekly summary report
summary = df.groupby("topic")["sentiment"].value_counts().unstack()
summary.to_csv(f"report_{datetime.now().strftime('%Y-%m-%d')}.csv")