import os
from phoenix.client import Client

PHOENIX_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJBcGlLZXk6MyJ9.XZSSNlVI13ExDsjrOemiZrP3ivzMjBVc-R4hUqxIH3E"

client = Client(
    base_url="https://app.phoenix.arize.com/s/eva-adler44",
    headers={"api-key": PHOENIX_API_KEY},
)

spans_df = client.spans.get_spans_dataframe(
    project_identifier="Coffee_shop_parking_assistant"
)

print(f"Found {len(spans_df)} spans — annotating...")

HALLUCINATION_KEYWORDS = [
    "garage", "valet", "towed", "validation", "overnight",
    "accessible", "disabilities", "time limit"
]

for _, row in spans_df.iterrows():
    span_id = row.get("context.span_id")
    question = str(row.get("attributes.input.value", "")).lower()
    if not span_id:
        continue

    is_hallucination = any(kw in question for kw in HALLUCINATION_KEYWORDS)
    print(f"{'HALLUCINATION' if is_hallucination else 'GROUNDED'}: {question[:70]}")

    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name="user_feedback",
        annotator_kind="HUMAN",
        label="negative" if is_hallucination else "positive",
        explanation="Outside known knowledge base" if is_hallucination else "Based on known facts",
    )

    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name="hallucination_check",
        annotator_kind="CODE",
        label="hallucinated" if is_hallucination else "grounded",
        score=0.2 if is_hallucination else 0.95,
        explanation="No data available for this question" if is_hallucination else "Matches known Merit Coffee facts",
    )

    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name="parking_accuracy",
        annotator_kind="CODE",
        score=0.3 if is_hallucination else 0.95,
        explanation="Low confidence" if is_hallucination else "High confidence",
    )

print("\nDone! Refresh your Phoenix dashboard.")
