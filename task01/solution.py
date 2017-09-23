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

file = codecs.open("answer.txt", "w", "utf-8")
file.write(u'\ufeff')

morph = pymorphy2.MorphAnalyzer()

ruki = "руки"
tri = "три"
stat = "стать"

write_normal_forms_to_file(ruki, morph, file)
write_gram_meaning_and_scores_to_file(ruki, morph, file)
write_normal_forms_and_scores_to_file(tri, morph, file)
write_first_lexeme_to_file(stat, morph, file)

file.close()
