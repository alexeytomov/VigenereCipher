import itertools, re
import detectRussian, freqAnalysis, vigenereCipher

LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮ"
MAX_KEY_LENGTH = 16 # ограничение максимально-возможной длины ключа
NUM_MOST_FREQ_LETTERS = 8 #ограничения количества буква на подключ
NONLETTERS_PATTERN = re.compile('[^А-Я]')

def main():
	with open('bunin_encrypted.txt', 'r') as f:
		ciphertextList = f.readlines()
	f.close()

	ciphertext = ''.join(ciphertextList)
	hackedMessage = hackVigenere(ciphertext)

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

def getNthSubkeysLetters(nth, keyLength, message):
	# Возвращает каждую n-ю букву из каждого набора длиной keyLength

	# Используем функцию удаления небуквенных символов
	message = NONLETTERS_PATTERN.sub('', message)

	i = nth - 1
	letters = []
	while i < len(message):
		letters.append(message[i])
		i += keyLength 
	
	return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
	# Определяем наиболее вероятные буквы для подключа
	ciphertextUp = ciphertext.upper()
	# allFreqScores - список длиной mostLikelyKeyLength,
	# элементами которого являются списки freqScores
	allFreqScores = []
	#Собираем строки, зашифрованные подключами предпологаемого ключа
	for nth in range(1, mostLikelyKeyLength + 1):
		nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

		#Список кортежей вида ( <буква>, <оценка частотного соответствия> )
		freqScores = [] 
		for possibleKey in LETTERS:
			decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
			keyAndFreqMatchTuple = (possibleKey, freqAnalysis.russianFreqMatchScore(decryptedText))
			freqScores.append(keyAndFreqMatchTuple)

		#Сортировка по оценкам частотного соответсвия
		freqScores.sort(key=getItemAtIndexOne, reverse=True)

		allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

	
	for i in range(len(allFreqScores)):
		print('Possible letters for letter %s of the key: ' % (i + 1), end='')
		for freqScore in allFreqScores[i]:
			print('%s ' % freqScore[0], end='')	
		print()

	#Сопоставляем наборы букв каждый с каждым через метод product
	#Пример: product('ABC', repeat=3) --> ['AAA', 'AAB', AAC' ... , 'DDD']
	for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
		possibleKey = ''
		for i in range(mostLikelyKeyLength):
			possibleKey += allFreqScores[i][indexes[i]][0] #???

		print('Attempting with key: %s' % (possibleKey))

		decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertextUp)

		if detectRussian.isRussian(decryptedText):
				#Возвращаем исходный регистр букв во взломанном шифротексте
			origCase = []
			for i in range(len(ciphertext)):
				if ciphertext[i].isupper():
					origCase.append(decryptedText[i].upper())
				else:
					origCase.append(decryptedText[i].lower())
			decryptedText = ''.join(origCase)

			print('Possible encryption hack with key %s:' % (possibleKey))
			print(decryptedText[:200]) # выводим первые 200 символов
			print()
			print('Enter D if done, anything else to continue hacking:')
			response = input('> ')
			if response.strip().upper().startswith('D'):
				return decryptedText
	return None

def hackVigenere(ciphertext):
	#Во-первых, применяем метод Касиски для выяснения возможной длины ключа
	allLikelyKeyLengths = kasiskiExamination(ciphertext)
	keyLengthStr = ''
	for keyLength in allLikelyKeyLengths:
		keyLengthStr += '%s ' % (keyLength)
	print('Kasiski examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
	hackedMessage = None 
	for keyLength in allLikelyKeyLengths:
		print('Attempting hack with key length %s (%s possible keys) ...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
		hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
		if hackedMessage != None:
			break

	# Если ни один из найденных вариантов ключа не сработал, начать атаку 
	# методом грубой силы
	if hackedMessage == None:
		print('Unable to hack message with likely key length(s). Brute-forcing key length...')
		for keyLength in range(1, MAX_KEY_LENGTH + 1):
			#Не проверять уже опробованные ключи
			if keyLength not in allLikelyKeyLengths:
				print('Attempting hack with key length %s (%s possuble keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
				hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
				if hackedMessage != None:
					break
	return hackedMessage

if __name__ == '__main__':
	main()		
