# Merit Coffee Parking Assistant 🚗☕

A simple AI-powered parking assistant for Merit Coffee South Lamar (Austin, TX), instrumented with [Arize Phoenix](https://arize.com/docs/phoenix) for full LLM observability.

## What it does
Answers natural language questions about parking at Merit Coffee South Lamar — availability, timing, alternatives, and more — with every Claude call traced live in Phoenix.

## Why Phoenix?
Without observability, LLM apps are a black box. Phoenix gives you full visibility into every call: latency, token usage, inputs, outputs, and hallucinations — all in one dashboard.

## Setup

### 1. Install dependencies
```bash
pip install anthropic openinference-instrumentation-anthropic arize-phoenix-otel
```

### 2. Set environment variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

```
PHOENIX_API_KEY=your-phoenix-api-key
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/your-space
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### 3. Run
```bash
export $(cat .env | xargs)
python merit_parking_agent.py
```

### 4. View traces
Open your Phoenix dashboard and watch traces arrive in real time.

## Stack
- [Anthropic Claude](https://anthropic.com) — LLM reasoning
- [Arize Phoenix](https://arize.com/docs/phoenix) — observability & tracing
- [OpenInference](https://github.com/Arize-ai/openinference) — auto-instrumentation
