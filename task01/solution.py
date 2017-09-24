import pymorphy2
import codecs

def write_normal_forms_to_file(word, morph, file):
	"""
	Выводит леммы слова. Может быть несколько, т.к. одно и то же написание может соответствовать разным словам.
	Например, "стали" -- "сталь" или "стать".
	"""
	file.write('Леммы слова "' + word + '":\n')

	distinct_normal_forms = set()
	for parse_result in morph.parse(word):
		distinct_normal_forms.add(parse_result.normal_form)

	for normal_form in distinct_normal_forms:
		file.write(normal_form + '\n')

	file.write("\n")

def write_gram_meaning_and_scores_to_file(word, morph, file):
	"""
	Выводит грамматические значения и их оценки.
	"""
	file.write('Грамматические значения слова "' + word + '"\n')

	for parse_result in morph.parse(word):
		file.write(parse_result.tag.cyr_repr + " оценка=" + str(parse_result.score) + "\n")

	file.write("\n")

def write_normal_forms_and_scores_to_file(word, morph, file):
	"""
	Выводит леммы слова и оценки с учетом всех грамматических значений. 
	Может быть несколько, т.к. одно и то же написание может соответствовать разным словам.
	Например, "стали" -- "сталь" или "стать".
	"""
	file.write('Леммы слова "' + word + '":\n')

	distinct_normal_forms_and_scores = dict()
	for parse_result in morph.parse(word):
		normal_form = parse_result.normal_form
		if normal_form not in distinct_normal_forms_and_scores:
			distinct_normal_forms_and_scores[normal_form] = 0.0

		distinct_normal_forms_and_scores[normal_form] += parse_result.score

	for normal_form in distinct_normal_forms_and_scores.keys():
		file.write(normal_form + " оценка=" + str(distinct_normal_forms_and_scores[normal_form]) + '\n')

	file.write("\n")

def write_first_lexeme_to_file(word, morph, file):
	"""
	Выводит лексему первого элемента parse в виде слов и их оценок.
	"""
	file.write('Лексема слова "' + word + '"' + "\n")

	lexeme = morph.parse(word)[0].lexeme
	for word_parse in lexeme:
		file.write(word_parse.word + " оценка=" + str(word_parse.score) + "\n")

	file.write("\n")

def write_word_in_plural_and_tvor_to_file(word, morph, file):
	"""
	Выводит множ число твор падежа первого элемента parse.
	"""
	file.write('Множ число и твор пад слова "' + word + '"' + "\n")

	file.write(morph.parse(word)[0].inflect({'plur', 'ablt'}).word + "\n")

	file.write("\n")

def write_part_of_to_file(word, morph, file):
	"""
	Выводит часть речи слова.
	"""
	file.write('Части речи слова "' + word + '"' + "\n")

	for parse_result in morph.parse(word):
		file.write(parse_result.tag.POS + "\n")

	file.write("\n")

import re
def text_to_wordlist(sentence):
	regexp = "[^а-яА-Яё]"
	sentence = re.sub(regexp, " ", sentence)
	result = sentence.lower().split()
	return result

from collections import Counter
def solve_thrird_part(morph, file):
	"""
	Решение третьего пункта на тексте Стругацких.
	Учитываем первые леммы в подсчете.
	"""
	text_file = open('wp.txt', 'r', encoding="utf8")
	lines = text_file.readlines()
	words = []
	for line in lines:
		words += text_to_wordlist(line)
	file.write("Количестов слов: " + str(len(words)) + "\n")

	nouns = []
	verbs = []
	for word in words:
		parse_result = morph.parse(word)[0]

		if "NOUN" in parse_result.tag:
			nouns.append(parse_result.normal_form)
		if "VERB" in parse_result.tag or "INFN" in parse_result.tag:
			verbs.append(parse_result.normal_form)

	file.write("Топ 10 сущ лемм: " + str(Counter(nouns).most_common(10)) + "\n")
	file.write("Топ 10 глаг лемм: " + str(Counter(verbs).most_common(10)))

	text_file.close()


file = codecs.open("answer.txt", "w", "utf-8")
file.write(u'\ufeff')

morph = pymorphy2.MorphAnalyzer()

ruki = "руки"
tri = "три"
stat = "стать"
turok = "турок"
mainu = "майню"

write_normal_forms_to_file(ruki, morph, file)
write_gram_meaning_and_scores_to_file(ruki, morph, file)
write_normal_forms_and_scores_to_file(tri, morph, file)
write_first_lexeme_to_file(stat, morph, file)
write_word_in_plural_and_tvor_to_file(turok, morph, file)
write_part_of_to_file(mainu, morph, file)

solve_thrird_part(morph, file)

file.close()
