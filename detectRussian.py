lettersUpper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
Letters_and_Space = lettersUpper + lettersUpper.lower() + ' \t\n'

def loadDictionary():
    dictionaryObject = open("dictionary.txt")
    dictionaryString = dictionaryObject.read()
    russianWords = {}
    for word in dictionaryString.split("\n"):
        russianWords[word] = None
    dictionaryObject.close()
    return russianWords

dictionaryWords = loadDictionary()

def coutWords(message):
    message = message.upper()
    message = noneSymbols(message)
    possibleWords = message.split()
    if possibleWords == []:
        return 0.0

    matches = 0
    #changes for testing
    for word in possibleWords:
        if word in dictionaryWords:
            matches += 1
    return float(matches) / len(possibleWords)

def noneSymbols(message): #deleting other symbols (but 'space' is here)
    clearString = []
    for symbol in message:
        if symbol in Letters_and_Space:
            clearString.append(symbol)
    return ''.join(clearString)

def Russian(message, wordPercentage = 20, letterPercentage = 85):
    wordChecking = coutWords(message) * 100 >= wordPercentage
    letterChecking = len(noneSymbols(message)) / float(len(message)) * 100 >= letterPercentage

    return wordChecking and letterChecking
