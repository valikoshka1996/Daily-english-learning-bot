import nltk
from nltk.corpus import words
import random

# Завантаження корпусу слів
nltk.download("words")

# Отримання списку всіх слів
word_list = words.words()

# Випадкове слово
print(word_list)

input()