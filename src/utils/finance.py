"""Financial math utilities."""

from typing import List


def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0) -> float:
    if not returns:
        return 0.0
    average_return = sum(returns) / len(returns)
    variance = sum((r - average_return) ** 2 for r in returns) / len(returns)
    volatility = variance ** 0.5
    if volatility == 0:
        return 0.0
    return (average_return - risk_free_rate) / volatility
