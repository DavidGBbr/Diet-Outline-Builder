# Diet Outline Builder

Python + LangGraph diet outline calculator.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Run Locally In Your Browser

```bash
diet-builder-web
```

Then open:

```text
http://127.0.0.1:8000
```

You can also run it with Python directly:

```bash
python -m diet_outline_builder.web
```

## Run The CLI

```bash
python -m diet_outline_builder
```

## Run Tests

```bash
pytest
```

## Use As A Library

```python
from diet_outline_builder import build_diet_outline

result = build_diet_outline(
    {
        "sex": "male",
        "age": 22,
        "heightCM": 178,
        "weightKG": 87.4,
        "activityLevel": "moderate",
        "goal": "lose_fat",
    }
)
```

The graph accepts `heightCM`/`weightKG` and also the misspelled aliases `heighCM`/`weighKG` used in the original prompt.
