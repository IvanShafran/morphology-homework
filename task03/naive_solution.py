test_words = [
	"cat",
	"man",
	"beach",
	"gas",
	"knife",
	"elf",
	"fish",
	"sky",
	"toy",
	"medium"
]

exceptions = {
	"man" : "men",
	"woman" : "women",
	"child" : "children",
	"mouse" : "mice",
	"ox" : "oxen",
	"louse" : "lice",
	"tooth" : "teeth",
	"goose" : "geese",
	"deer" : "deer",
	"fish" : "fish"
}

def exceptionRule(word):
	if word in exceptions.keys():
		return exceptions[word]
	else:
		return None

firstRuleOneLetterSuffixes = ['z', 's', 'x', 'o']
firstRuleTwoLetterSuffixes = ['ch', 'sh']


def firstRule(word):
	if len(word) >= 2 and word[-2:] in firstRuleTwoLetterSuffixes:
		return word + "es"

	if len(word) >= 1 and word[-1:] in firstRuleOneLetterSuffixes:
		return word + "es"

	return None

def secondRule(word):
	if len(word) >= 1 and word[-1] == "f":
		return word[:-1] + "ves"

	if len(word) >= 2 and word[-2:] == "fe":
		return word[:-2] + "ves"
 
	return None

vowels=['a','e','i','o','u']

def thirdRule(word):
	if len(word) >= 2 and word[-1] == "y" and word[-2]:
		if word[-2] in vowels:
			return word + "s"
		else:
			return word[:-1] + "ies"

	return None


def lastRule(word):
	return word + "s"


rules = [exceptionRule, firstRule, secondRule, thirdRule, lastRule]

file = open("answer-naive.txt", "w")

for word in test_words:
	for rule in rules:
		result = rule(word)
		if result is not None:
			file.write(word + " - " + result + "\n")
			break

file.close()
