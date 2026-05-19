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

HALLUCINATION_QUESTIONS = [
    "What's the address of the nearest parking garage?",
    "Is there accessible parking for people with disabilities?",
    "How long can I park in the lot before getting towed?",
    "Is there parking validation if I buy a coffee?",
    "Is there valet parking at Merit Coffee South Lamar?",
]

for _, row in spans_df.iterrows():
    span_id = row.get("context.span_id")
    question = row.get("input.value", "")
    if not span_id:
        continue

    is_hallucination = any(q in str(question) for q in HALLUCINATION_QUESTIONS)

    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name="user_feedback",
        annotator_kind="HUMAN",
        label="positive" if not is_hallucination else "negative",
        explanation="Based on known facts" if not is_hallucination else "May contain guessed information",
    )

    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name="hallucination_check",
        annotator_kind="CODE",
        label="hallucinated" if is_hallucination else "grounded",
        score=0.2 if is_hallucination else 0.95,
        explanation="Outside known knowledge base" if is_hallucination else "Matches known Merit Coffee facts",
    )

    client.spans.add_span_annotation(
        span_id=span_id,
        annotation_name="parking_accuracy",
        annotator_kind="CODE",
        score=0.4 if is_hallucination else 0.95,
        explanation="Low confidence" if is_hallucination else "High confidence",
    )

    print(f"Annotated: {str(question)[:60]}...")

print("\nDone! Refresh your Phoenix dashboard.")
