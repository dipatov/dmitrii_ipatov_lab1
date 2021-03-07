import socket

correct_mistakes = 0
incorrect_mistakes = 0
correct_words = 0

def change_letter(word, let, i):
    return word[:i] + let + word[i + 1:]

def encode_word(word):
    k = 0
    while 2**k <= len(word):
        word = word[:2**k-1] + '0' + word[2**k-1:]
        k += 1
    k = 0
    while 2**k <= len(word):
        ones = 0
        for j in range(2**k-1, len(word), 2**(k+1)):
            for x in range(j, min(j+(2**k), len(word))):
                if word[x] == '1':
                    ones += 1
        if ones % 2 == 1:
            word = change_letter(word, "1", 2**k-1)
        k += 1
    return word

def correct_mist(word, ind):
    corr = '0'
    if word[ind] == '0':
        corr = '1'
    return change_letter(word, corr, ind)

def del_crt(word):
    k = 0
    while 2**(k+1) <= len(word):
        k += 1
    tmp_word = word
    while (k >= 0):
        tmp_word = change_letter(tmp_word, "", 2**k - 1)
        k -= 1
    return tmp_word

def decode_word(word):
    tmp_word = encode_word(del_crt(word))
    mist = 0
    for i in range(len(word)):
        if word[i] != tmp_word[i]:
            mist += (i+1)
    if 0 < mist <= len(word):
        return del_crt(correct_mist(word, mist-1)), 1, 0, 0
    elif mist > len(word) and len(word) > 0:
        return del_crt(word), 0, 1, 0
    else:
        return del_crt(word), 0, 0, 1


server = '192.168.8.112', 6121
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sor.bind(('192.168.8.112', 12396))
sor.sendto(b'', server)

received_message = ''
resc_s = bytearray()

try:
    while 1:
        data = sor.recv(1024)
        enc_mes, cor, incor, words = decode_word(data.decode('utf-8'))
        received_message += enc_mes
        correct_mistakes += cor
        incorrect_mistakes += incor
        correct_words += words
        if(len(received_message) == 41250):
            break
    res = 'Кол-во исправленных ошибок: ' + str(correct_mistakes) + '\n' + \
          'Кол-во правильных слов: ' + str(correct_words) + '\n' + \
          'Кол-во неправильно доставленных слов: ' + str(correct_mistakes + incorrect_mistakes)
    sor.sendto(res.encode('utf-8'), server)
    resc_s = bytearray()
    for i in range(0, len(received_message), 8):
        code = int(received_message[i:i + 8], base=2)
        resc_s.append(code)
    print(resc_s.decode('utf-8'))
except Exception:
    print('Сообщение невозможно раскодировать, в нем допущены множественные ошибки в словах.')
finally:
    sor.close()