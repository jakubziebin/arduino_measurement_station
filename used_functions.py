from __future__ import annotations


def get_value_from_measure(measure: str) -> float:  
    splitted_measure = measure.split(":")
    value = float(splitted_measure[1])

    return value
