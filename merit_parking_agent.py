import os
import anthropic
from phoenix.otel import register

tracer_provider = register(
    project_name="Coffee_shop_parking_assistant",
    auto_instrument=True,
)

tracer = tracer_provider.get_tracer(__name__)

PARKING_CONTEXT = """
You are a parking assistant for Merit Coffee South Lamar in Austin, TX.
- Address: 1105 S Lamar Blvd, Austin, TX 78704
- Parking: Free dedicated lot, limited spots (~10-15)
- Street parking: Available on S Lamar, Bouldin Ave, and Kinney Ave
- Peak times: Weekdays 11am-1pm, weekend mornings before noon
- Best times to park: Before 8am or after 2pm on weekdays
- Hours: Mon-Fri 7am-7pm, Sat-Sun 7am-7pm
"""

client = anthropic.Anthropic()

@tracer.chain
def ask_parking_question(question: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        system=PARKING_CONTEXT,
        messages=[{"role": "user", "content": question}],
    )
    return message.content[0].text

QUESTIONS = [
    "Is there parking available at Merit Coffee South Lamar right now?",
    "What's the best time to visit to avoid parking issues?",
    "Are there any alternatives if the lot is full?",
    "How many parking spots are there and is there a parking garage nearby?",
    "Is parking free or do I need to pay?",
    "Can I park overnight at Merit Coffee?",
    "Is there valet parking at Merit Coffee South Lamar?",
    "What's the address of the nearest parking garage?",
    "Is there accessible parking for people with disabilities?",
    "How long can I park in the lot before getting towed?",
    "Is there parking validation if I buy a coffee?",
    "What happens if I park there but don't go to Merit Coffee?",
]

print("Merit Coffee Parking Assistant")
print("Traces will appear in your Phoenix dashboard")
print("=" * 60)

for question in QUESTIONS:
    print(f"\nQuestion: {question}")
    print("-" * 50)
    answer = ask_parking_question(question)
    print(f"Answer: {answer}")

print("\nDone! Check your Phoenix dashboard for live traces.")
