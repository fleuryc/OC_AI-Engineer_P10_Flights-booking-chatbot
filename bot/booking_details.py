"""Booking details."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class BookingDetails:
    """Booking details."""

    or_city: Optional[str] = None
    dst_city: Optional[str] = None
    str_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[str] = None
