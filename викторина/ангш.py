# Квест "Уважение к матери друга"

# Игрок вводит свое имя
player_name = input("Введите ваше имя: ")

print("Привет", player_name + "! Добро пожаловать в квест 'Уважение к матери друга'.")

# Задаем начальные значения
уважение_к_матери = 0

# Начало квеста
print("Ваш друг позвал вас в гости к своей матери. Вы готовы?")

# Выбор игрока
print("1. Да, я готов.")
print("2. Нет, не сегодня.")

# Игрок выбирает
choice_1 = input("Ваш выбор (1/2): ")

if choice_1 == "1":
    print("Отлично! Поехали...")

    # Задание 1
    print("Вы приехали к дому друга. Вы видите, что его мама устала и занята хозяйством.")
    print("Вы решаете помочь или просто сидеть и ждать...")

    # Выбор игрока
    print("1. Предложить помощь.")
    print("2. Просто сидеть и ждать.")

    # Игрок выбирает
    choice_2 = input("Ваш выбор (1/2): ")

    if choice_2 == "1":
        уважение_к_матери += 1
        print("Отлично! Вы предложили помощь и помогли матери друга.")
        print("Ваше уважение к матери друга повысилось.")
    else:
        print("Вы решили не помогать и просто сидеть и ждать...")

    # Задание 2
    print("Друг и его мама предлагают вам пообедать вместе.")
    print("Вам предлагают выбрать между здоровым обедом и фастфудом.")

    # Выбор игрока
    print("1. Выбрать здоровый обед.")
    print("2. Выбрать фастфуд.")

    # Игрок выбирает
    choice_3 = input("Ваш выбор (1/2): ")

    if choice_3 == "1":
        уважение_к_матери += 1
        print("Отличный выбор! Вы выбрали здоровый обед.")
        print("Ваше уважение к матери друга повысилось.")
    else:
        print("Вы выбрали фастфуд...")

    # Задание 3
    print("Друг и его мама предлагают сыграть вместе в настольную игру.")
    print("Они спрашивают, в какую игру вы хотите играть.")

    # Выбор игрока
    print("1. Выбрать игру, которую предложили они.")
    print("2. Предложить игру, которую знаете вы.")

    # Игрок выбирает
    choice_4 = input("Ваш выбор (1/2): ")

    if choice_4 == "1":
        уважение_к_матери += 1
        print("Хороший выбор! Вы выбрали игру, которую предложили они.")
        print("Ваше уважение к матери друга повысилось.")
    else:
        print("Вы предложили свою игру...")

    # Задание 4
    print("После игры вы решаете поблагодарить друга и его маму.")

    # Выбор игрока
    print("1. Поблагодарить и попрощаться.")
    print("2. Попрощаться")
    choice_4 = input("Ваш выбор (1/2): ")
    if choice_4 == "1":
        уважение_к_матери += 1
        print("Хороший выбор! Вы поблагодарили и ушли со спокойной душой.")
        print("Ваше уважение к матери друга повысилось.")
    else:
        print("Вы просто ушли...")
    if уважение_к_матери>2:
        print('Вы заработали уважение мамы друга, поздравляем!!')
    else:
        print('Вы очень растроили мать друга. Вас больше не позовут в гости')