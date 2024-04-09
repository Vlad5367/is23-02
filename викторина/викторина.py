import time, os
def ansa(ans,count):
    if ans == 'a' or ans == '1':
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)
def mis(mistake,count):
    if mistake == '3' or mistake == 'три' :
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)
def mis1(mistake,count):
    if mistake == '1'or mistake == 'один'or mistake == 'одна':
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)
def mis2(mistake,count):
    if mistake == '2'or mistake == 'два'or mistake == 'две':
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)
def ansb(ans,count):
    if ans == 'b'or ans == '2':
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)
def ansc(ans,count):
    if ans == 'c'or ans == '3':
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)
def ansd(ans,count):
    if ans == 'd'or ans == '4':
        print('Правильный ответ')
        count+=1
    else:
        print('Неправильный ответ')
    time.sleep(2)
    os.system('cls||clear')
    return (count)

def viktoryna():
    count=0
    print('Добрый день, уважаемые участники!')
    print('Сегодня мы проводим викторину по программированию, которая поможет вам проверить  ваши знания в этой области.')
    print('Викторина затрагивает следующие темы: "Списки", "Строки", "Циклы", "Числовые типы данных", "Условный оператор", "Ввод-вывод данных"')
    print('Правила просты: на экране будут выводиться различные вопросы и вы должны будете дать правильные ответы. Ответив правильно, вы получаете балл. В конце викторины подводятся итоги и выводится итоговый балл.')
    print('У вас есть лишь несколько секунд на раздумья, так что будьте быстры и внимательны. Желаю всем удачи!')
    print('Готовы начать?')
    input('Для начала нажмите ENTER')
    print('вопрос №1')
    print('Какой оператор в языке программирования Python используется для ввода данных с клавиатуры?')
    print('A) input()')#right
    print('B) print()')
    print('C) read()')
    print('D) scan()')
    ans = input().lower()
    count=ansa(ans,count)

    print('вопрос №2')
    print('Какой оператор используется для вывода данных на экран в языке программирования Python?')
    print('A) output()')
    print('B) print()')#right
    print('C) display()')
    print('D) cout')
    ans = input().lower()
    count=ansb(ans,count)

    print('вопрос №3')
    print('Какой символ используется для обозначения равенства в условном операторе в языке программирования Python?')
    print('A) ==')#right
    print('B) =')
    print('C) :=')
    print('D) !=')
    ans = input().lower()
    count=ansa(ans,count)

    print('вопрос №4')
    print('Какой оператор используется для выполнения определенного блока кода, если условие верно, иначе выполнить другой блок кода?')
    print('A) for')
    print('B) while')
    print('C) switch')
    print('D) if-else')#right
    ans = input().lower()
    count=ansd(ans,count)

    print('вопрос №5')
    print('Какой тип данных используется для представления целых чисел в Python?')
    print('A) integer')
    print('B) int')#right
    print('C) num')
    print('D) whole')
    ans = input().lower()
    count=ansb(ans,count)

    print('вопрос №6')
    print('Какой тип данных используется для представления чисел с плавающей запятой (дробей) в Python?')
    print('A) dec')
    print('B) float')#right
    print('C) point')
    print('D) fraction')
    ans = input().lower()
    count=ansb(ans,count)

    print('вопрос №7')
    print('Какой вид цикла в Python выполняется определенное количество раз?')
    print('A) for')#right
    print('B) while')
    print('C) repeat')
    print('D) loop')
    ans = input().lower()
    count=ansa(ans,count)

    print('вопрос №8')
    print('Какой оператор используется для выхода из цикла в Python?')
    print('A) break')#right
    print('B) end')
    print('C) exit')
    print('D) stop')
    ans = input().lower()
    count=ansa(ans,count)

    print('вопрос №9')
    print('Каков правильный способ создания пустого списка в Python?')
    print('A) list()')
    print('B) []')#right
    print('C) new_list()')
    print('D) empty_list()')
    ans = input().lower()
    count=ansb(ans,count)

    print('вопрос №10')
    print('Как добавить элемент в конец списка в Python?')
    print('A) add()')
    print('B) insert()')
    print('C) append()')#right
    print('D) extend()')
    ans = input().lower()
    count=ansc(ans,count)

    print('вопрос №11')
    print('Какой метод строки в Python позволяет разбить строку на подстроки по заданному разделителю?')
    print('A) split()')#right
    print('B) join()')
    print('C) replace()')
    ans = input().lower()
    count=ansa(ans,count)

    print('вопрос №12')
    print('Код, который должен выводить чила от 1 до 5')
    print('num = 1')
    print('while num < 5:')
    print('     print(num)')
    print('    num = 1')
    print('Введите кол-во ошибок в приведенном коде')
    mistake = input().lower()
    count=mis2(mistake,count)

    print('вопрос №13')
    print('Код для нахождения 5!')
    print('result=0')
    print('for i in range(1, 6):')
    print('    result = result*i')
    print('print("result")')
    print('Введите кол-во ошибок в приведенном коде')
    mistake = input().lower()
    count=mis1(mistake,count)

    print('вопрос №14')
    print('Код для нахождения максимального числа')
    print('numbers = [10, 5, 8, 20, 3]')
    print('max_number = numbers(0)')
    print('for num in numbers')
    print('    if num > max_number:')
    print('        max_number == num')
    print('print(max_number)')
    print('Введите кол-во ошибок в приведенном коде')
    mistake = input().lower()
    count=mis(mistake,count)


    print('вопрос №15')
    print('Главный вопрос: на каком языке написан код данной викторины?')
    print('A) MATlab')
    print('B) Python')#right
    print('C) С++')
    print('D) С#')
    ans = input().lower()
    count=ansb(ans,count)

    print('Тест закончен у вас', count, 'правильных отетов из 15')
    print('Это ', count/15*100, '%')