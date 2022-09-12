LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
FREQ_LETTERS = "ОЕАИНТСРВЛКМДПУЯЫЬГЗБЧЙХЖШЮЦЩЭФЪЁ"

def getLetterCount(message):
    letterCount = {'А' : 0, 'Б' : 0, 'В' : 0, 'Г' : 0,
                   'Д' : 0, 'Е' : 0, 'Ё' : 0, 'Ж' : 0,
                   'З' : 0, 'И' : 0, 'Й' : 0, 'К' : 0,
                   'Л' : 0, 'М' : 0, 'Н' : 0, 'О' : 0,
                   'П' : 0, 'Р' : 0, 'С' : 0, 'Т' : 0,
                   'У' : 0, 'Ф' : 0, 'Х' : 0, 'Ц' : 0,
                   'Ч' : 0, 'Ш' : 0, 'Щ' : 0, 'Ъ' : 0,
                   'Ы' : 0, 'Ь' : 0, 'Э' : 0, 'Ю' : 0,
                   'Я' : 0}
    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1
    return letterCount

def getInemAtIndexZero(items):
    return inems[0]

def getFrequencyOrder(message):
    letterToFreq = getLetterCount(message)
    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[lettreToFreq[letter]].append(letter)

    for freq in freqToLetter:
        freqToLetter[freq].sort(key=FREQ_LETTERS.find, reverse = True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse = True)

    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)

def russianFreqMatchScore(message):
    freqOrder = getFrequencyOrder(message)

    matchScore = 0

    for commonLetter in FREQ_LETTERS[0:6]:
        if commonLetter in freqOrder[0:6]:
            matchScore += 1
    for uncommonLetter in FREQ_LETTERS[-6:0]:
        if uncommonLetter in freqOrder[-6:0]:
            matchScore += 1

    return matchScore
