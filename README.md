# Coffee Shop Parking Assistant ☕🚗

An AI-powered parking assistant for Merit Coffee South Lamar (Austin, TX), fully instrumented with [Arize Phoenix](https://arize.com/docs/phoenix) for real-time LLM observability, tracing, and evaluation.

## The Problem

When you build an LLM-powered app, you have no visibility into what's happening inside it. When a response is slow, wrong, or hallucinates — you can't tell why. Which step failed? Was it the prompt? The model? The retrieval? The pipeline is a black box.

## The Solution

Instrument with Phoenix. Three lines of code turn every Claude call into a fully traced, annotated, observable pipeline — with latency breakdowns, token counts, hallucination flags, and accuracy scores visible in a live dashboard.

## What It Does

Answers natural language parking questions about Merit Coffee South Lamar:
- Is there parking right now?
- What's the best time to visit?
- Are there alternatives if the lot is full?
- Is there valet parking? (hallucination risk — flagged automatically)

Every question is traced in Phoenix with full span visibility and scored across three annotation dimensions.

## Project Structure

```
coffee_shop_parking_assistant/
├── merit_parking_agent.py   # AI parking assistant instrumented with Phoenix
├── annotate_traces.py       # Annotation pipeline — hallucination detection & accuracy scoring
├── .env.example             # Environment variable template
└── .gitignore
```

## Stack

- [Anthropic Claude](https://anthropic.com) — LLM reasoning (claude-sonnet-4-5)
- [Arize Phoenix](https://arize.com/docs/phoenix) — observability, tracing & evaluation
- [OpenInference](https://github.com/Arize-ai/openinference) — auto-instrumentation
- [arize-phoenix-client](https://pypi.org/project/arize-phoenix-client/) — annotation pipeline

## Setup

### 1. Create environment
```bash
conda create -n parking-demo python=3.11 -y
conda activate parking-demo
```

### 2. Install dependencies
```bash
pip install anthropic openinference-instrumentation-anthropic arize-phoenix-otel arize-phoenix-client pandas
```

### 3. Set environment variables
Copy `.env.example` to `.env` and fill in your keys:
```
PHOENIX_API_KEY=your-phoenix-api-key
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/your-space
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### 4. Run the parking assistant
```bash
export $(cat .env | xargs)
python merit_parking_agent.py
```

### 5. Run the annotation pipeline
```bash
python annotate_traces.py
```

### 6. View live traces and annotations
Open your Phoenix dashboard and see every Claude call traced with:
- **Latency** per span
- **Token usage** (prompt + completion)
- **hallucination_check** — grounded vs. hallucinated (CODE annotator)
- **parking_accuracy** — 0–1 confidence score (CODE annotator)
- **user_feedback** — positive vs. negative (HUMAN annotator)

## Key Insight

Questions the app has no data for (valet parking, overnight parking, parking validation) are automatically flagged as hallucination risks. Questions grounded in real Merit Coffee parking facts score 0.95 accuracy. This is the eval pipeline Phoenix enables — moving from "it works" to "I can prove it works."

## Phoenix Dashboard

Traces, spans, annotations, and metrics visible at your Phoenix Cloud instance in real time.
