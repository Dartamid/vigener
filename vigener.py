alpha = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def openText(message):
    encryptMessage = message
    for i in encryptMessage:
        if i == 'Ё':
            encryptMessage = encryptMessage.replace(i, 'E')
        if i not in alpha:
            encryptMessage = encryptMessage.replace(i, '')
    return encryptMessage


def add_spaces_every_5_chars(string):
    result = ""
    for i in range(0, len(string), 5):
        result += string[i:i+5] + " "
    return result.strip()


def lenKey(txt):
    index_list = []  # массив индекса совпадений
    lenMsg = len(txt)


    shift_txt = txt[2:] + txt[:2]
    for shift in range(2, len(txt) // 10):
        count = 0
        for i in range(lenMsg):
            if txt[i] == shift_txt[i]: count += 1
        index_list.append(round(count * 100 / lenMsg, 3))  # добавляем индекс сопадений в масив

        shift_txt = shift_txt[1:] + shift_txt[:1]  # снова двигаем строку на 1 символ

    inx = []
    for i in range(1, len(index_list)):
        try:
            if index_list[i - 1] < index_list[i] > index_list[i + 1] and index_list[i] > 4.4:  # определяем скачек
                inx.append(index_list.index(index_list[i]) + 2)  # записываем на каких по счету сдвигах был скачек
        except IndexError:  # обработка границы массиова
            if index_list[i - 1] < index_list[i] and index_list[i] > 4.4:
                inx.append(index_list.index(index_list[i]) + 2)  # прибавляем минмиальную длину ключа
    if inx[1] - inx[0] == inx[2] - inx[1]:  # этого условия достаточно в большинстве случаев
        return inx[1] - inx[0]  # вернет число кратное длине ключа
    else:
        print("обнаружена аномалия, требуется ручной анализ данных автокорреляционного метода")
        print("Вывод индексов на экран:\n")
        print(index_list)
        return input('Введите предпологаемую длину ключа: ')


def textFormat(txt, lenKey):
    l = [""] * lenKey
    for i in range(0, len(txt), lenKey):
        split_txt = txt[i:i + lenKey]
        try:
            for q in range(lenKey):
                l[q] += split_txt[q]
        except IndexError:
            None
    return l


def letterFrequency(line):
    letterFrequencyList = [0] * len(alpha)
    for letterIndex, letter in enumerate(alpha):
        letterFrequencyList[letterIndex] = line.count(letter) / len(line)
    return letterFrequencyList


def caesar(txt, _step):
    result = ''
    for c in txt:
        result += alpha[(alpha.index(c) + _step) % len(alpha)]
    return result


def char_key(line):
    russian_freq = [
        0.062, 0.014, 0.038, 0.013, 0.025, 0.072, 0.007, 0.016,
        0.062, 0.010, 0.028, 0.035, 0.026, 0.053, 0.09, 0.023,
        0.04, 0.045, 0.053, 0.021, 0.002, 0.009, 0.003, 0.012, 0.006,
        0.003, 0.014, 0.016, 0.014, 0.003, 0.006, 0.018
    ]

    score = float('inf')
    shift = 0

    line_freq = letterFrequency(line)

    for i in range(len(alpha)):
        line_score = 0
        for ch in line:
            line_score += (russian_freq[alpha.find(ch)] - line_freq[(alpha.find(ch) + i) % len(alpha)]) ** 2

        if line_score < score:
            score = line_score
            shift = i

    return alpha[shift]


def findKey(lines):
    key = ''

    for line in lines:
        key = key + char_key(line)

    return key


def decryptVigener(encryptMessage, keyWord):
    keyWord *= len(encryptMessage) // len(keyWord) + 1
    message = ""
    for index, letter in enumerate(encryptMessage):
        message += alpha[(alpha.index(letter) - alpha.index(keyWord[index])) % len(alpha)]
    return message


def encrypt_message(encryptMessage, keyWord):
    keyWord *= len(encryptMessage) // len(keyWord) + 1
    message = ""
    for index, letter in enumerate(encryptMessage):
        message += alpha[(alpha.index(letter) + alpha.index(keyWord[index])) % len(alpha)]

    message = add_spaces_every_5_chars(message)

    return message


def decrypt_message(msg, cipher_key=None):
    if cipher_key is not None:
        message = openText(msg)
        message = decryptVigener(message, cipher_key)
        return cipher_key, message
    cipher_message = openText(msg)
    len_key = lenKey(cipher_message)
    columns = textFormat(cipher_message, len_key)
    cipher_key = findKey(columns)
    encrypt_message = decryptVigener(cipher_message, cipher_key)
    return cipher_key, encrypt_message



if __name__ == "main":
    msg = input()
    text = openText(msg)  # читаем и чистим текст от левых символов
    lenKey = lenKey(text)  # вычисляем предпологаемую длину ключа
    print("Предпологаемая длина ключа: ", lenKey)

    lines = textFormat(text, lenKey)  # разбиваем text на lenKey частей и делаем из них массив lines

    key = findKey(lines)
    print(key)
    print(decryptVigener(text, key))
