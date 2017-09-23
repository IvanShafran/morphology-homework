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

file = codecs.open("answer.txt", "w", "utf-8")
file.write(u'\ufeff')

morph = pymorphy2.MorphAnalyzer()

arms = "руки"

write_normal_forms_to_file(arms, morph, file)

file.close()