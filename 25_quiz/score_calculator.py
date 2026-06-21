# score_calculator.py
# Скрипт для автоматизации подсчета результатов веб-квиза на ЛФМШ "Квант"
# Совместим с Python 3.12+

import json
from typing import Dict, List, Tuple

# Структура данных для хранения результатов команд
# Ключ - название команды
# Значение - словарь с баллами по раундам (1-5) и тай-брейку (tb)
teams_data = {
    "Сверхпроводники": {"R1": 4, "R2": 3, "R3": 5, "R4": 4, "R5": 4, "TB": 2},
    "Синтаксический Сахар": {"R1": 5, "R2": 4, "R3": 4, "R4": 3, "R5": 5, "TB": 1},
    "Декораторы Кванта": {"R1": 3, "R2": 5, "R3": 5, "R4": 5, "R5": 3, "TB": 3},
    "Багфиксеры": {"R1": 4, "R2": 4, "R3": 3, "R4": 4, "R5": 4, "TB": 2}
}

def calculate_results(data: Dict[str, Dict[str, int]]) -> List[Tuple[str, int, int]]:
    """
    Рассчитывает сумму баллов для каждой команды.
    Возвращает отсортированный список кортежей: (Название команды, Сумма основных раундов, Балл тай-брейка).
    Сортировка идет сначала по сумме основных раундов (по убыванию),
    затем по баллам тай-брейка (по убыванию).
    """
    results = []
    for team, scores in data.items():
        # Сумма баллов по основным раундам 1-5
        main_score = sum(scores[r] for r in ["R1", "R2", "R3", "R4", "R5"])
        tb_score = scores.get("TB", 0)
        results.append((team, main_score, tb_score))
    
    # Сортировка: основной балл приоритетнее, тай-брейк - вспомогательный
    results.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return results

def print_leaderboard(leaderboard: List[Tuple[str, int, int]]):
    print("=" * 60)
    print(f"{'ТАБЛИЦА ЛИДЕРОВ КВИЗА ПО ВЕБ-РАЗРАБОТКЕ':^60}")
    print("=" * 60)
    print(f"{'Место':<6} | {'Название команды':<25} | {'Осн. раунды':<12} | {'Тай-брейк':<10}")
    print("-" * 60)
    
    for idx, (team, main, tb) in enumerate(leaderboard, start=1):
        # Выделяем победителя
        medal = "🏆" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f" {idx}."
        print(f"{medal:<6} | {team:<25} | {main:<12} | {tb:<10}")
    
    print("=" * 60)

if __name__ == "__main__":
    leaderboard = calculate_results(teams_data)
    print_leaderboard(leaderboard)
