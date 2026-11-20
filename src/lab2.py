# -*- coding: utf-8 -*-
# Квест: Научная станция в Антарктиде
# Только базовые конструкции: переменные, if/elif/else, while, break, continue.

# ---------- Состояние игры ----------
module = "living"
temp = 10
heating = False
fuel_taken = False       # подобрано ли топливо
fuel_used = False        # использовано ли топливо
running = True

print("=" * 60)
print("НАУЧНАЯ СТАНЦИЯ В АНТАРКТИДЕ")
print("=" * 60)
print("Вы очнулись в жилом модуле. Температура падает.")
print("Включите отопление и доберитесь до вездехода!")
print("Введите 'help' для списка команд.")
print("Текущий модуль: " + module + " | Температура: " + str(temp) + "C")

# ---------- Главный цикл ----------
while running:
    command = input("\n> ").strip().lower()

    # Пустая строка — просто пропускаем ход без штрафа
    if command == "":
        print("Введите команду (help — список команд).")
        continue

    # ---------- help ----------
    if command == "help":
        print("Доступные команды:")
        print("  help              - показать помощь")
        print("  look              - осмотреть модуль")
        print("  go <направление>  - перейти (north/south/east/west)")
        print("  take <предмет>    - подобрать предмет")
        print("  use <предмет>     - использовать предмет")
        print("  exit              - покинуть станцию (только в exit)")
        continue

    # ---------- look ----------
    if command == "look":
        if module == "living":
            print("Жилой модуль. Койки, стол, слабый свет. Выходы: north, east.")
        elif module == "lab":
            print("Лаборатория. Приборы, мигающий монитор. Выходы: south, east.")
        elif module == "storage":
            if fuel_taken:
                print("Склад. Пустые ящики. Выходы: west, north.")
            else:
                print("Склад. Ящики, среди них канистра с топливом. Выходы: west, north.")
        elif module == "diesel":
            if heating:
                print("Дизельная. Генератор работает, отопление включено. Выходы: west, south, east.")
            else:
                print("Дизельная. Генератор, топливный бак. Нужно топливо. Выходы: west, south, east.")
        elif module == "hangar":
            print("Ангар. Стоит вездеход. Выходы: west, north.")
        elif module == "exit":
            print("Шлюз и выход к вездеходу. Выходы: south.")
        print("Текущий модуль: " + module + " | Температура: " + str(temp) + "C")
        continue

    # ---------- go ----------
    if command.startswith("go"):
        parts = command.split()
        if len(parts) < 2:
            print("Укажите направление: go north/south/east/west")
            continue
        direction = parts[1]
        moved = False

        if module == "living":
            if direction == "north":
                module = "lab"; moved = True
            elif direction == "east":
                module = "storage"; moved = True
            else:
                print("Нельзя пойти на " + direction + " из living.")
        elif module == "lab":
            if direction == "south":
                module = "living"; moved = True
            elif direction == "east":
                module = "diesel"; moved = True
            else:
                print("Нельзя пойти на " + direction + " из lab.")
        elif module == "storage":
            if direction == "west":
                module = "living"; moved = True
            elif direction == "north":
                module = "diesel"; moved = True
            else:
                print("Нельзя пойти на " + direction + " из storage.")
        elif module == "diesel":
            if direction == "west":
                module = "lab"; moved = True
            elif direction == "south":
                module = "storage"; moved = True
            elif direction == "east":
                module = "hangar"; moved = True
            else:
                print("Нельзя пойти на " + direction + " из diesel.")
        elif module == "hangar":
            if direction == "west":
                module = "diesel"; moved = True
            elif direction == "north":
                module = "exit"; moved = True
            else:
                print("Нельзя пойти на " + direction + " из hangar.")
        elif module == "exit":
            if direction == "south":
                module = "hangar"; moved = True
            else:
                print("Нельзя пойти на " + direction + " из exit.")

        if moved:
            print("Вы перешли в модуль: " + module + ".")
            # --- ход: уменьшение температуры ---
            if not heating:
                temp = temp - 1
            print("Температура: " + str(temp) + "C | Отопление: " + ("ВКЛ" if heating else "ВЫКЛ"))
            if temp <= 0:
                print("Температура упала ниже нуля. Вы замёрзли...")
                print("ПОРАЖЕНИЕ.")
                running = False
                break
        continue

    # ---------- take ----------
    if command.startswith("take"):
        parts = command.split()
        if len(parts) < 2:
            print("Укажите предмет: take <item>")
            continue
        item = parts[1]
        if item == "fuel" and module == "storage" and not fuel_taken:
            fuel_taken = True
            print("Вы подобрали: fuel.")
            # --- ход ---
            if not heating:
                temp = temp - 1
            print("Температура: " + str(temp) + "C | Отопление: " + ("ВКЛ" if heating else "ВЫКЛ"))
            if temp <= 0:
                print("Температура упала ниже нуля. Вы замёрзли...")
                print("ПОРАЖЕНИЕ.")
                running = False
                break
        else:
            print("Здесь нет предмета: " + item + ".")
        continue

    # ---------- use ----------
    if command.startswith("use"):
        parts = command.split()
        if len(parts) < 2:
            print("Укажите предмет: use <item>")
            continue
        item = parts[1]
        if item == "fuel":
            if module != "diesel":
                print("Топливо можно использовать только в дизельной (diesel).")
                continue
            if fuel_used:
                print("Топливо уже использовано.")
                continue
            if not fuel_taken:
                print("У вас нет топлива. Сначала подберите его в storage.")
                continue
            fuel_used = True
            heating = True
            print("Вы залили топливо в генератор и включили отопление! Стало теплее.")
            print("Температура: " + str(temp) + "C | Отопление: ВКЛ")
        else:
            print("Непонятно, как использовать: " + item + ".")
        continue

    # ---------- exit ----------
    if command == "exit":
        if module != "exit":
            print("Выйти из станции можно только из шлюза (exit).")
            continue
        if not heating:
            print("Отопление не включено! Вездеход не заведётся, вы замёрзнете.")
            continue
        print("Вы добрались до вездехода и уехали в безопасное место!")
        print("ПОБЕДА!")
        running = False
        break

    # ---------- неизвестная команда ----------
    print("Неизвестная команда: " + command + ". Введите help.")