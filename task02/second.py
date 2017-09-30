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


class Node:
    def __init__(self):
        super(Node, self).__init__()
        self.edges = dict() # char to Node
        self.is_terminal = False

def add_word_to_bor(bor, word):
    node = bor
    for char in word:
        if char not in node.edges.keys():
            new_node = Node()
            node.edges[char] = new_node

        node = node.edges[char]

    node.is_terminal = True

def build_bor():
    bor = Node()
    for word in get_words():
        add_word_to_bor(bor, word)
    return bor

def is_in_bor(bor, word):
    node = bor
    for char in word:
        if char in node.edges.keys():
            node = node.edges[char]
        else:
            return False

    return node.is_terminal

def test_bor(bor, ofile):
    test_words = ['сту', 'стул', 'стулец', 'на', 'номер', 'нат', 'снег', 'нег']
    for word in test_words:
        ofile.write('Слово "' + word + '" содержится в боре: ' + str(is_in_bor(bor, word)) + "\n")
    ofile.write("\n")

from queue import Queue
def predict_word(bor, word, ofile, debug=False):
    hypothsys = Queue()
    hypothsys.put([bor, '', 0]) # node, word, change_distance
    best_word = 'Not found'
    best_distance = 1000

    while not hypothsys.empty():
        node, cur_word, change_distance = hypothsys.get()
        #if debug:
        #    ofile.write('cur_word ' + cur_word + ' change_distance ' + str(change_distance) + '\n')
        
        if node.is_terminal:
            distance_with_deletion = change_distance + len(word) - len(cur_word)
            if distance_with_deletion < best_distance:
                best_distance = distance_with_deletion
                best_word = cur_word

        if change_distance > best_distance or len(cur_word) >= len(word):
            # нет смысла искать дальше
            continue

        # проверяем переходы
        for char in node.edges.keys():
            if char == word[len(cur_word)]:
                hypothsys.put([node.edges[char], cur_word + char, change_distance])
            else:
                hypothsys.put([node.edges[char], cur_word + char, change_distance + 1])
        
    return best_word, best_distance


def test_predict(bor, ofile):
    test_words = ['стул', 'сту', 'стулец', 'стел', 'овраг', 'челов', 'хооо', 'рывлфв', 
            'вылод', 'орв', 'змен', 'олы', 'матан', 'годнота', 'бор', 'иван', 'смузи', 'дорогостоящий', 'предводитель']
    for word in test_words:
        predict, dist = predict_word(bor, word, ofile, True)
        ofile.write("Ближайшее к слову '" + word + "': " + predict + " dist: " + str(dist) + "\n")


ofile = open('second_answer.txt', 'w')

bor = build_bor()

test_bor(bor, ofile)
test_predict(bor, ofile)

ofile.close()
