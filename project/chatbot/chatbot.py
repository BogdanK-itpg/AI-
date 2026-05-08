"""Chatbot module for Incident Management System.

Wraps NLU and Router for easy access.
"""

from .nlu import parse_input
from .router import handle_intent as route_intent


def parse_and_handle(user_input: str):
    """Parse user input and return the response string (or 'exit')."""
    intent, params = parse_input(user_input)
    return route_intent(intent, params)


def parse_input_wrapper(user_input: str):
    """Parse input and return (intent, params)."""
    intent, params = parse_input(user_input)
    return intent, params


def handle_intent(intent: str, params):
    """Handle intent with params."""
    return route_intent(intent, params)