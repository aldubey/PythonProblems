import re, string, logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter


class DebateReader:
    @staticmethod
    def read_debate(speaker_name: str) -> str:
        with open('debate.txt') as debate_lines:
            is_speaker_statement = False
            statement = ""
            for line in debate_lines:
                match = re.match(r'^{0}+:'.format(speaker_name), line)
                if re.match(r'^\w+:', line) and not match:
                    is_speaker_statement = False
                if match or is_speaker_statement and not re.match(r'^\(', line):
                    line = re.sub(r'\(\w+\)', '', line)
                    statement += line.replace(speaker_name + ':', ' ').replace('\n', ' ')
                    is_speaker_statement = True
        return statement

    def read_debate_stem(speaker_name: str) -> str:
        logging.info('Speaker: {0}', speaker_name)
        statement = DebateReader.read_debate(speaker_name)

        # Discard punctuation
        statement = statement.translate(dict((ord(char), None) for char in string.punctuation))

        # Remove capitalization
        statement = statement.lower()

        # Remove stop words
        word_tokens = word_tokenize(statement)
        stop_words = set(stopwords.words('english'))
        final_words = []
        for w in word_tokens:
            if w not in stop_words:
                final_words.append(w)
        # Stemmed
        stemmed_words = []
        #  wnl = WordNetLemmatizer()
        ps = PorterStemmer()
        for word in final_words:
            # stemmed_words.append(wnl.lemmatize(word))
            stemmed_words.append(ps.stem(word))
        return stemmed_words

    def most_common_words_by_speaker(speaker_name: str, num: int):
        stemmed_words = DebateReader.read_debate_stem(speaker_name)
        return DebateReader.most_common_words(stemmed_words, num)

    def most_common_words(word_list: [], num: int):
        word_count_dict = {}
        for word in word_list:
            if word not in word_count_dict:
                word_count_dict[word] = 1
            else:
                word_count_dict[word] += 1
        word_counter = Counter(word_count_dict)
        return word_counter.most_common(num)

    # Most commnon positive words
    def most_frequent_positive_words(speaker_name: str, num: int):
        stemmed_words = DebateReader.read_debate_stem(speaker_name)
        positive_word_list = []
        with open('positive.txt') as positive_words:
            for line in positive_words:
                line = line.replace('\n', '')
                if line in stemmed_words:
                    positive_word_list.append(line)
        return DebateReader.most_common_words(positive_word_list, num)


# First Task: Read debate and assign statements
print("\n First Task output:")
print('LEHRER: ', DebateReader.read_debate('LEHRER'))
print('OBAMA: ', DebateReader.read_debate('OBAMA'))
print('ROMNEY: ', DebateReader.read_debate('ROMNEY'))

# Second Task: Stemming
print("\n Second Task output:")
print('LEHRER: ', DebateReader.read_debate_stem('LEHRER'))
print('OBAMA: ', DebateReader.read_debate_stem('OBAMA'))
print('ROMNEY: ', DebateReader.read_debate_stem('ROMNEY'))

# Third Task: Most common words
print("\n Third Task output:")
print('LEHRER: ', DebateReader.most_common_words_by_speaker('LEHRER', 10))
print('OBAMA: ', DebateReader.most_common_words_by_speaker('OBAMA', 10))
print('ROMNEY: ', DebateReader.most_common_words_by_speaker('ROMNEY', 10))

# Fourth Task: Most frequent postive  words
print("\n Third Task output:")
print('LEHRER: ', DebateReader.most_frequent_positive_words('LEHRER', 10))
print('OBAMA: ', DebateReader.most_frequent_positive_words('OBAMA', 10))
print('ROMNEY: ', DebateReader.most_frequent_positive_words('ROMNEY', 10))
