"""IncidentClassifier - AI Placeholder for Priority Prediction.

This module provides a mock AI component that classifies incidents
based on rule-based logic to predict priority levels.

In a real system, this would use machine learning models to predict priority.
"""

from typing import List


class IncidentClassifier:
    """Classifier for predicting incident priority levels.

    Uses simple rule-based logic to determine priority:
    - High: If description contains 'server', 'crash', 'down', 'critical', 'emergency'
    - Medium: If description contains 'slow', 'delay', 'performance', 'lag'
    - Low: All other cases

    In a production system, this would be replaced with actual ML model inference.
    """

    HIGH_KEYWORDS = [
        "server", "crash", "down", "critical", "emergency",
        "failure", "outage", "breach", "hack", "attack",
        "dead", "broken", "not working", "unavailable",
        "сървър", "срив", "не работи", "критичен",
        "авария", "хакер", "attack", "down", "failure"
    ]

    MEDIUM_KEYWORDS = [
        "slow", "delay", "performance", "lag", "glitch",
        "intermittent", "unstable", "error", "issue", "problem",
        "бавен", "забавяне", "бавна", "проблем", "грешка",
        "лоша", "лошо", "неефективност"
    ]

    def predict_priority(self, incident) -> str:
        """Predict the priority level for an incident based on its description.

        Args:
            incident: Incident object with description attribute

        Returns:
            Priority level as string: 'Low', 'Medium', or 'High'
        """
        description = incident.description.lower()

        for keyword in self.HIGH_KEYWORDS:
            if keyword in description:
                return "High"

        for keyword in self.MEDIUM_KEYWORDS:
            if keyword in description:
                return "Medium"

        return "Low"

    def batch_predict(self, incidents: List) -> List[str]:
        """Predict priorities for multiple incidents.

        Args:
            incidents: List of Incident objects

        Returns:
            List of priority strings
        """
        return [self.predict_priority(inc) for inc in incidents]

    def get_confidence(self, incident) -> float:
        """Get mock confidence score for the prediction.

        In a real ML system, this would return actual model confidence.

        Args:
            incident: Incident object

        Returns:
            Mock confidence score between 0 and 1
        """
        import random
        return round(random.uniform(0.7, 0.95), 2)