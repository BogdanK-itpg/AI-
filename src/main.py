"""Main entry point for AI Incident Management System - CLI Chatbot."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot.chatbot import parse_and_handle
from core.event_manager import EventManager
from services import incident_service, technician_service, statistics_service


event_manager = EventManager()


def on_incident_created(data):
    print(f"\n[СЪБИТИЕ] Нов инцидент създаден: ID={data['id']}, Задание='{data['title']}'")


def on_priority_changed(data):
    print(f"\n[СЪБИТИЕ] Промяна на приоритет: Инцидент {data['id']}, {data['old_priority']} -> {data['new_priority']}")


def on_critical_detected(data):
    print(f"\n[ВНИМАНИЕ] КРИТИЧЕН ИНЦИДЕНТ! ID={data['id']}, Задание='{data['title']}'")


event_manager.subscribe("on_incident_created", on_incident_created)
event_manager.subscribe("on_priority_changed", on_priority_changed)
event_manager.subscribe("on_critical_detected", on_critical_detected)


def main():
    print("=" * 60)
    print("AI Система за управление на инциденти")
    print("Чатбот интерфейс")
    print("=" * 60)
    print("\nНапишете 'помощ' за списък с команди.")
    print("Напишете 'изход' за изход от програмата.\n")

    while True:
        try:
            user_input = input("Вие: ").strip()

            if not user_input:
                continue

            response = parse_and_handle(user_input)

            if response == 'exit':
                print("Бот: Довиждане!")
                break

            print(f"Бот: {response}")

        except KeyboardInterrupt:
            print("\nБот: Довиждане!")
            break
        except Exception as e:
            print(f"Бот: Грешка: {str(e)}")


if __name__ == "__main__":
    main()