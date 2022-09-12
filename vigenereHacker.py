import detectRussian, freqAnalysis, vigenereCipher
#ans = isRussian.Russian(message) #True/False

LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮ"
MAX_KEY_LENGTH = 16 # ограничение максимально-возможной длины ключа
NUM_MOST_FREQ_LETTERS = 4 # ограничения количества буква на подключ
SILENT_MODE = False # True
NONLETTERS_PATTERN = re.compile('[^А-Я]')

def main():
	ciphertext = """  """

	if hackedMessage != None:
		print(hackedMessage)
	else:
		print("Failed to hack encryption")

def findRepeatSequencesSpacing(message):
	# Находит в сообщении любые 3-, 4-, 5-буквенные повторяющиеся 
	# последовательности. Возвращает словарь, где ключи - 
	# это последовательности, а значения - списки интервалов повторения.
	
	# Используем регулярное выражение для удаление небуквенных символов
	message = NONLETTERS_PATTERN.sub('', message.upper())

	seqSpacings = {}

	for seqLen in range(3,6):
		for seqStart in range(len(message) - seqLen):
			seq = message[seqStart:seqStart + seqLen]
			# Поиск по заданной последовательности
			for i in range(seqStart + seqLen, len(message) - seqLen):
				if message[i:i + seqLen] == seq:
					#Найдена повторяющаяся последовательность
					if seq not in seqSpacings:
						seqSpacings[seq] = []
					seqSpacings[seq].append(i - seqStart)
	return seqSpacings

def getUsefulFactors(num):
	#Возвращает список возможных значений ключа (от 2 до MAX_KEY_LENGTH)
	
	if num < 2:
		return []

	factors = []

	for i in range(2, MAX_KEY_LENGTH + 1):
		if num % i == 0:
			factors.append(i)
		# В книге еще блок кода - убрал, тк возможно ненужный

	return factors

def getItemAtIndexOne(x):
	return x[1]

def getMostCommonFactors(seqFactors):
	# Во-первых, подсчитываем повторы множителей в словаре seqFactors
	factorCounts = {}

	# Ключ - множитель, значение - сколько раз встречается
	for seq in seqFactors:
		factorList = seqFactors[seq]
		for factor in factorList:
			if factor not in factorCounts:
				factorCounts[factor] = 0
			factorCounts[factor] += 1

	# Во-вторых, объединяем множители и счетчики в кортежи,
	# чтобы их отсортировать
	factorsByCount = []
	for factor in factorCounts:
		if factor <= MAX_KEY_LENGTH:
			factorsByCount.append( (factor, factorCounts[factor]) )

	# Сортировка по ключам повторений
	factorsByCount.sort(key = getItemAtIndexOne, reverse = True)

	return factorsByCount

def kasiskiExamination(ciphertext):
	# Находим последовательности длиной от 3 до 5 букв,
	# встречающиеся некоднократно               
	repeatedSeqSpacings = findRepeatSequencesSpacing(ciphertext)

	# Ключ - последовательность, значение - возможные длины ключа
	seqFactors = {}
	for seq in repeatedSeqSpacings:
		seqFactors[seq] = []
		for spacing in repeatedSeqSpacings[seq]:
			seqFactors[seq].extend(getUsefulFactors(spacing)) 

	# Получаем список кортежей (множитель, количество повторений),
	# отсортированный по убыванию
	factorsByCount = getMostCommonFactors(seqFactors)
	
	# Исключаем информацию о количестве повторений, получаем список
	# множителей, отсортированный по убыванию
	allLikelyKeyLengths = []
	for twoIntTuple in factorsByCount:
		allLikelyKeyLengths.append(twoIntTuple[0])

	return allLikelyKeyLengths




