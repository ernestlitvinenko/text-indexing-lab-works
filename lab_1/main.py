import difflib

import nltk
import pymorphy3
from nltk.corpus import stopwords
from lab_1.models import Request, Synonym
from lab_1.database import session_maker
from sqlalchemy import insert, select, Result

# DOWNLOAD NLTK DATA
nltk.download('popular')


class LangProcessing:
    def __init__(self):
        self.analyzer = pymorphy3.MorphAnalyzer()

    def punkt(self, data: list[str]):
        """
        Filters out certain characters from a list of strings.

        Args:
            data (list[str]): A list of strings.

        Returns:
            list[str]: A new list of strings where certain characters have been filtered out.
        """
        return [x for x in data if x not in ",.- !? ;: () [] {} «»"]

    def lowerize(self, data: list[str]):
        """
        Converts a list of strings to lowercase.

        Args:
            data (list[str]): The list of strings to be converted to lowercase.

        Returns:
            list[str]: The list of strings with all elements converted to lowercase.
        """
        return [x.lower() for x in data]

    def tokenize_words(self, sentence):
        """
        Tokenizes a given sentence into individual words using the specified language tokenizer.

        Parameters:
            sentence (str): The sentence to be tokenized.

        Returns:
            list: A list of tokenized words.
        """
        return self.lowerize(
            self.punkt(
                nltk.word_tokenize(sentence, language="russian")
            )
        )

    def set_answer(self, question: str, answer: str):
        """
        Set the answer for a given question in the database.

        Args:
            question (str): The question to set the answer for.
            answer (str): The answer to set for the question.
        """
        question = ' '.join(
            [self.normalize_word(x) for x in self.tokenize_words(question) if x not in stopwords.words("russian")])

        with session_maker() as session:
            stmt = insert(Request).values(request=question, answer=answer)
            session.execute(stmt)
            session.commit()

    def replace_with_synonyms(self, data: list[str]) -> list[str]:
        """
        Replaces words in the given list with their synonyms.

        Args:
            data (list[str]): The list of words to replace.

        Returns:
            list[str]: The list of words with synonyms replaced.

        """
        stmt = select(Synonym).where(Synonym.core_word.in_(data))
        with session_maker() as sesssion:
            result: Result = sesssion.execute(stmt)
            synonyms = result.scalars().all()
            for synonym in synonyms:
                data = [x.replace(synonym.core_word, synonym.synonym) for x in data]
        return data

    def normalize_word(self, word: str) -> str:
        """
        Normalize a word.

        Args:
            word (str): The word to be normalized.

        Returns:
            str: The normalized form of the word.

        Raises:
            TypeError: If the input word is not a string.
        """
        if not isinstance(word, str):
            print(word)
            raise TypeError("Word must be a string")
        return self.analyzer.parse(word)[0].normal_form

    def get_answer(self, question: str):
        """
        Retrieves the answer(s) to a given question.

        Args:
            question (str): The question to be answered.

        Returns:
            list: A list of answer(s) to the question, sorted by relevance.

        Raises:
            None
        """
        question = [self.normalize_word(x) for x in self.tokenize_words(question) if
                    x not in stopwords.words("russian")]
        question = self.replace_with_synonyms(question)
        question = [x for x in question if x != ""]

        print(question)

        with session_maker() as session:
            stmt = select(Request)
            result: Result = session.execute(stmt)
            data = result.scalars().all()

        returned = sorted([x for x in map(lambda x: [x.answer, difflib.SequenceMatcher(None, question,
                                                                                       x.request.split(' ')).ratio()],
                                          data) if x[1] > 0.75], key=lambda x: x[1], reverse=True)
        return returned

    def add_synonym(self, core_word: str, synonym: str):
        core_word = [self.normalize_word(x) for x in self.tokenize_words(core_word) if
                     x not in stopwords.words("russian")]

        synonym = [self.normalize_word(x) for x in self.tokenize_words(synonym) if x not in stopwords.words("russian")]

        if len(core_word) == 0:
            core_word = ""
        else:
            core_word = core_word[0]
        if len(synonym) == 0:
            synonym = ""
        else:
            synonym = synonym[0]

        with session_maker() as session:
            stmt = insert(Synonym).values(core_word=core_word, synonym=synonym)
            session.execute(stmt)
            session.commit()


if __name__ == '__main__':
    from pprint import pprint as pp

    proc = LangProcessing()
    proc.add_synonym("чтоже", "что")
    pp(proc.get_answer("чтоже такое nltk"))
