from core.common_types import List

def average(data: List[float]) -> float:
    if not data:
        return float('nan')
    sum_ = sum(data)
    return sum_ / len(data) if sum_ != 0 else 0

def cumulative(data: List[float]) -> float:
    return sum(data) if data else float('nan')

def maximum(data: List[float]) -> float:
    return max(data) if data else float('nan')

def minimum(data: List[float]) -> float:
    return min(data) if data else float('nan')

__all__ = {
    "average": average,
    "cumulative": cumulative,
    "maximum": maximum,
    "minimum": minimum
}