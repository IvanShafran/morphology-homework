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
        self.parent = None
        self.parent_char = None

def add_word_to_bor(bor, word):
    node = bor
    for char in word:
        if char not in node.edges.keys():
            new_node = Node()
            new_node.parent = node
            new_node.parent_char = char
            node.edges[char] = new_node

        node = node.edges[char]

    node.is_terminal = True

def build_bor():
    bor = Node()
    for word in get_words():
        add_word_to_bor(bor, word)
    return bor

def get_word_up_to_node(node):
    word = ""
    while node.parent != None:
        word += node.parent_char
        node = node.parent

    word = word[::-1]
    return word

from queue import Queue
def extra_predict_word(bor, word):
    hypothsys = Queue()
    hypothsys.put([bor, 0, 0]) # node, position in word, penalty
    best_word = 'Not found'
    best_penalty = 3 # Иначе будет комб взрыв

    while not hypothsys.empty():
        node, position, penalty = hypothsys.get()

        if position == len(word):
            if node.is_terminal and best_penalty > penalty:
                best_word = get_word_up_to_node(node)
                best_penalty = penalty
            continue

        # Остановка, если есть ответ получше
        if penalty > best_penalty:
            continue

        word_char = word[position]

        # Просто проход по букве
        if word_char in node.edges.keys():
            hypothsys.put([node.edges[word_char], position + 1, penalty])

        # Удаление
        hypothsys.put([node, position + 1, penalty + 1])

        # Перестановка
        if len(word) - position >= 2:
            next_char = word[position]
            next_next_char = word[position + 1]

            next_node = node.edges.get(next_next_char, None)
            if next_node != None:
                next_next_node = next_node.edges.get(next_char, None)
                if next_next_node != None:
                    hypothsys.put([next_next_node, position + 2, penalty + 1])

        # Вставка и замена
        for char in node.edges.keys():
            if word_char != char:
                # Вставка
                hypothsys.put([node.edges[char], position, penalty + 1])
                # Замена
                hypothsys.put([node.edges[char], position + 1, penalty + 1])

    return best_word, best_penalty


def test_extra_predict(bor, ofile):
    test_words = ['стул', 'сутл', 'сту', 'стулец', 'стел', 'овраг', 'челов', 'хооо', 'рывлфв', 
            'вылод', 'орв', 'змен', 'олы', 'матан', 'годнота', 'бор', 'иван', 'смузи', 'дорогостоящий', 'предводитель']
    for word in test_words:
        predict, dist = extra_predict_word(bor, word)
        ofile.write("Ближайшее к слову '" + word + "': " + predict + " dist: " + str(dist) + "\n")


ofile = open('second_extra_answer.txt', 'w', encoding="utf-8")

bor = build_bor()
    
test_extra_predict(bor, ofile)

ofile.close()
