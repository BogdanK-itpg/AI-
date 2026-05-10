"""Test script for AI Incident Management System."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reset global state
import services.incident_service as incidents
incidents._global_db = None
incidents._global_classifier = None
incidents._global_event_manager = None

import services.technician_service as technicians
technicians._global_db = None

from chatbot.chatbot import parse_and_handle


def test_command(cmd):
    print(f"\n>>> Тест: {cmd}")
    response = parse_and_handle(cmd)
    print(f"Отговор: {response}")
    return response


print("=" * 60)
print("Тестване на AI Система за управление на инциденти")
print("=" * 60)

test_command("помощ")

test_command("създай инцидент Срив на сървъра описание Сървърът не работи категория Хардуер")

test_command("създай инцидент Бавна мрежа описание Мрежата е много бавна категория Мрежа")

test_command("създай инцидент Проблем с паролата описание Потребителът не може да влезе категория Софтуер")

test_command("покажи инциденти")

test_command("покажи инциденти с приоритет висок")

test_command("покажи техници")

test_command("добави техник Стефан Сигурност")

test_command("назначи техник 1 за инцидент 1")

test_command("затвори инцидент 1")

test_command("покажи статистика")

test_command("средно време за решаване")

test_command("покажи история")

test_command("изход")

print("\n" + "=" * 60)
print("Тестването завърши успешно!")
print("=" * 60)