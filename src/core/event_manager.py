"""EventManager - Core Event System for AI Incident Management System.

This module provides a reusable event dispatcher system that supports:
- Subscribing to events with callbacks
- Triggering events with data payloads
- Multiple listeners per event
"""

from typing import Callable, Dict, List, Any


class EventManager:
    """Event manager for publish-subscribe pattern implementation.

    Provides methods to subscribe to events and trigger events with data.
    Multiple callbacks can be registered for the same event name.

    Usage:
        event_manager = EventManager()
        event_manager.subscribe('on_incident_created', callback_function)
        event_manager.trigger('on_incident_created', {'id': 1, 'title': 'Test'})
    """

    def __init__(self):
        """Initialize the event manager with an empty subscriptions dictionary."""
        self._subscriptions: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to an event with a callback function.

        Args:
            event_name: Name of the event to subscribe to
            callback: Function to call when the event is triggered
        """
        if event_name not in self._subscriptions:
            self._subscriptions[event_name] = []
        self._subscriptions[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Unsubscribe a callback from an event.

        Args:
            event_name: Name of the event to unsubscribe from
            callback: Callback function to remove
        """
        if event_name in self._subscriptions:
            try:
                self._subscriptions[event_name].remove(callback)
            except ValueError:
                pass

    def trigger(self, event_name: str, data: Any = None) -> None:
        """Trigger an event, calling all subscribed callbacks with the provided data.

        Args:
            event_name: Name of the event to trigger
            data: Optional data to pass to the callback functions
        """
        if event_name in self._subscriptions:
            for callback in self._subscriptions[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"[EVENT ERROR] Error in callback for '{event_name}': {e}")

    def get_subscriptions(self, event_name: str) -> List[Callable]:
        """Get all callbacks subscribed to an event.

        Args:
            event_name: Name of the event

        Returns:
            List of callback functions
        """
        return self._subscriptions.get(event_name, [])

    def clear_event(self, event_name: str) -> None:
        """Clear all subscriptions for a specific event.

        Args:
            event_name: Name of the event to clear
        """
        if event_name in self._subscriptions:
            del self._subscriptions[event_name]

    def clear_all(self) -> None:
        """Clear all event subscriptions."""
        self._subscriptions.clear()

    def list_events(self) -> List[str]:
        """List all registered event names.

        Returns:
            List of event names that have subscribers
        """
        return list(self._subscriptions.keys())