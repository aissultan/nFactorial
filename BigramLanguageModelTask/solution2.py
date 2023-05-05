import string 
import random 
import matplotlib.pyplot as plt 
import pandas as pd 
 
# Читаем данные из файла и сохраняем их в списке 
with open('names.txt', 'r') as f: 
    names = [name.strip().lower() for name in f.readlines()] 
 
# Создаем список букв, которые мы будем использовать для генерации имен 
alphabet = list(string.ascii_lowercase) + ['^', '$'] 
 
# Создаем словарь, в котором будем хранить частоты каждого биграмма 
bigram_counts = {} 
 
# Проходимся по каждому имени в списке и считаем частоты каждого биграмма 
for name in names: 
    # Добавляем начальный и конечный символы к имени 
    name = '^' + name + '$' 
 
    # Разбиваем имя на биграммы 
    bigrams = [name[i:i+2] for i in range(len(name)-1)] 
     
    # Считаем частоты каждого биграмма 
    for bigram in bigrams: 
        if bigram in bigram_counts: 
            bigram_counts[bigram] += 1 
        else: 
            bigram_counts[bigram] = 1 
 
# Вычисляем общее количество биграмм 
total_bigrams = sum(bigram_counts.values()) 
 
# Создаем словарь, в котором будем хранить вероятности каждого биграмма 
bigram_probs = {} 
 
# Вычисляем вероятности каждого биграмма 
for bigram, count in bigram_counts.items(): 
    bigram_probs[bigram] = count / total_bigrams 
 
def generate_name(): 
    # Выбираем случайную первую букву из списка алфавита 
    first_letter = random.choice(alphabet[:-2]) # Исключаем "^" и "$" 
 
    # Инициализируем имя начальной буквой 
    name = first_letter 
 
    # Пока последняя буква имени не является конечным символом "$" 
    while name[-1] != '$': 
        # Получаем все возможные биграммы для последней буквы имени 
        possible_bigrams = [bigram for bigram in bigram_probs.keys() if bigram.startswith(name[-1])] 
 
        # Вычисляем вероятности для каждого возможного биграмма 
        probabilities = [bigram_probs[bigram] for bigram in possible_bigrams] 
 
        # Выбираем случайный биграмм на основе вероятностей 
        next_bigram = random.choices(possible_bigrams, weights=probabilities)[0] 
 
        # Добавляем следующую букву к имени 
        name += next_bigram[1] 
 
    # Удаляем начальный и конечный символы из имени и возвращаем его 
    return name[:-1] 
 
# Выводим сгенерированное
print(generate_name()) 
 
# Создаем пустой DataFrame для хранения данных о вероятностях биграмм 
df = pd.DataFrame(columns=alphabet, index=alphabet) 
 
# Заполняем DataFrame вероятностями для каждого биграмма 
for bigram, prob in bigram_probs.items(): 
    df.loc[bigram[0], bigram[1]] = prob 
 
# Заполняем пропущенные значения нулями 
df.fillna(0, inplace=True) 
 
# Выводим таблицу 
print(df) 
 
# Создаем список биграмм и соответствующих вероятностей 
bigrams = list(bigram_probs.keys()) 
probs = list(bigram_probs.values()) 
 
# Рисуем график 
plt.bar(bigrams, probs) 
plt.title("Bigram probabilities") 
plt.xlabel("Bigram") 
plt.ylabel("Probability") 
plt.show() 
 
# Создаем heatmap на основе DataFrame 
plt.imshow(df.values, cmap='viridis') 
 
# Настраиваем оси и заголовок 
plt.xticks(range(len(df.columns)), df.columns) 
plt.yticks(range(len(df.index)), df.index) 
plt.xlabel('Second letter') 
plt.ylabel('First letter') 
plt.title('Bigram probabilities') 
 
# Выводим картинку 
plt.show()