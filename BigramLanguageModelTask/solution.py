import string
import random
import matplotlib.pyplot as plt
import pandas as pd

# Прочитайте данные с файла в структуры данных удобных для высчитывания вероятностей
with open('names.txt', 'r') as f:
    names = [name.strip().lower() for name in f.readlines()]

alphabet = list(string.ascii_lowercase) + ['^', '$']

bigram_counts = {}

for name in names:
    name = '^' + name + '$'
    bigrams = [name[i:i+2] for i in range(len(name)-1)]

    for bigram in bigrams:
        if bigram in bigram_counts:
            bigram_counts[bigram] += 1
        else:
            bigram_counts[bigram] = 1

total_bigrams = sum(bigram_counts.values())

bigram_probs = {}

# Высчитайте вероятность всех существующих биграмм (строим выборку) 
for bigram, count in bigram_counts.items():
    bigram_probs[bigram] = count / total_bigrams

# Возьмите букву из выборки которое может придти как первая буква имени (рандомно)
# Продолжать тянуть следующую букву из выборки, таким образом генерируя имя. Это нужно делать пока вы не вытянули конец имени
# Generate function - возможность создавать имя.
def generate_name():
    first_letter = random.choice(alphabet[:-2]) 

    name = first_letter

    while name[-1] != '$':
        possible_bigrams = [bigram for bigram in bigram_probs.keys() if bigram.startswith(name[-1])]
        probabilities = [bigram_probs[bigram] for bigram in possible_bigrams]
        next_bigram = random.choices(possible_bigrams, weights=probabilities)[0]
        name += next_bigram[1]

    return name[:-1]

print(generate_name())

# Получить таблицу визуализирующие вероятности биграмм
df = pd.DataFrame(columns=alphabet, index=alphabet)

for bigram, prob in bigram_probs.items():
    df.loc[bigram[0], bigram[1]] = prob

df.fillna(0, inplace=True)

print(df)

# Бонус 
# Визуализация таблицы в картинку 
plt.imshow(df.values, cmap='viridis')

plt.xticks(range(len(df.columns)), df.columns)
plt.yticks(range(len(df.index)), df.index)
plt.xlabel('Second letter')
plt.ylabel('First letter')
plt.title('Bigram probabilities')

plt.show()