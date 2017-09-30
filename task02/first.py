import codecs
import re

def text_to_wordlist(sentence):
    regexp = "[^а-яА-Яё]"
    sentence = re.sub(regexp, " ", sentence)
    result = sentence.lower().split()
    return result

def get_words():
    text_file = open('text.txt', 'r', encoding="utf8")
    lines = text_file.readlines()
    words = []
    for line in lines:
        words += text_to_wordlist(line)
    text_file.close()

    return words

def get_all_trigrams(word):
    word = "##" + word + "##"
    trigrams = []
    for i in range(len(word) - 2):
        trigrams.append(word[i:i + 3])
    return trigrams

def calculate_trigram_frequencies(words):
    trigram_frequencies = dict()
    for word in words:
        word = "##" + word + "##"
        for trigram in get_all_trigrams(word):
            trigram_frequencies[trigram] = trigram_frequencies.get(trigram, 0) + 1

    return trigram_frequencies

def test_trigram_frequencies(trigram_frequencies, ofile):
    test_trigrams = ['ова', 'нор', '##о', 'к##', 'фыв', 'ннн']
    for trigram in test_trigrams:
        ofile.write("Частота вхождения '" + trigram + "': " + str(trigram_frequencies.get(trigram, 0)) + "\n")

    ofile.write("\n")

def has_misspell(trigram_frequencies, word, threshold_frequency):
    for trigram in get_all_trigrams(word):
        if trigram_frequencies.get(trigram, 0) < threshold_frequency:
            return True
    return False

def test_has_misspel(trigram_frequencies, ofile):
    threshold_frequency = 10
    test_words = ['корова', 'стул', 'голова', 'упел', 'рика', 'циливизация', 'ответ', 'очепятка', 'отце', 
            'нит', 'хз', 'циган', 'йцукен', 'цветок', 'шыкарно', 'годнота', 'ноч']

    ofile.write("Тестирование поиска опечаток на триграммах при относительной границе частоты: " + str(threshold_frequency) + "\n")

    for word in test_words:
        ofile.write("Слово '" + word + "' имеет опечатку: " + str(has_misspell(trigram_frequencies, word, threshold_frequency)) + "\n")


ofile = open('first_answer.txt', 'w')

trigram_frequencies = calculate_trigram_frequencies(get_words())

test_trigram_frequencies(trigram_frequencies, ofile)

test_has_misspel(trigram_frequencies, ofile)

ofile.close()
