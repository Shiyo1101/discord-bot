def load_context() -> str:
    with open("contexts/context.txt", "r", encoding="utf-8") as f:
        return f.read()
