def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(".", ",")