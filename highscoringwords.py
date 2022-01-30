import itertools
__author__ = 'codesse'


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []
    valid_words_with_scores = {}
    leaderboard = []

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files
        containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

    def build_leaderboard_for_word_list(self) -> list:
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words,
        or a list passed to the method.
        :return: The list of top words.
        """
        # assign the scores to the words in the dict
        for word in self.valid_words:
            # get the words score
            score = self._calc_score_for_word(word)
            # assign the score to the word in the dict
            self.valid_words_with_scores[word] = score
        # get the ordered list as a leaderboard
        self.leaderboard = self._create_ordered_leaderboard(self.valid_words_with_scores)
        return self.leaderboard

    def build_leaderboard_for_letters(self, starting_letters: str) -> list or None:
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters
        contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are
        bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for
        words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the
        contents of the wordlist.txt file.
        :return: The list of top buildable words.
        """
        # ignore starting_letters with less than 3 letters
        if len(starting_letters) < self.MIN_WORD_LENGTH:
            print('Not enough letters, please try again with more than 3.')
            return None
        # the list of possible words
        possible_words = {}
        # first get a list of all the words that have letters in the starting_letters
        for word in self.valid_words:
            # filter out the words longer than the length of the starting letters
            if len(word) > len(starting_letters):
                continue
            else:
                match_count = 0
                altered_starting_letters = starting_letters
                # loop over letters in word and compare to starting_letters.
                for letter in word:
                    # if they match, add one to match count and remove matched letter from starting_letters
                    if letter in altered_starting_letters:
                        match_count += 1
                        altered_starting_letters = altered_starting_letters.replace(letter, '', 1)
                # if match_count is the same as the length of the word, add word to list
                if match_count == len(word):
                    # calc the score for the word
                    score = self._calc_score_for_word(word)
                    possible_words[word] = score
        # get the ordered list as a leaderboard
        possible_words_leaderboard = self._create_ordered_leaderboard(possible_words)
        return possible_words_leaderboard

    # Private methods
    def _calc_score_for_word(self, word: str) -> int:
        """
        calculate the score for a word, based off the scores found in letterValues.txt
        :param: word : the str to calc the score for
        :return: score : the words score.
        """
        score = 0
        # loop over the letters, adding the score to the total
        for letter in word:
            score += self.letter_values[letter]
        return score

    def _create_ordered_leaderboard(self, dict_words: dict) -> list:
        """
        Return a list of words ordered by their score and then alphabetically, capped at the max words.
        :param dict_words: a dict of words and their scores
        :param max_words: the mac number of words to cap the leaderboard at.
        :return:
        """
        # now order the dict based on the score
        dict_words = dict(sorted(dict_words.items(), key=lambda item: item[1],
                                 reverse=True))
        # get top scores as a list of tuples capped at max_words, if max words
        if len(dict_words) > self.MAX_LEADERBOARD_LENGTH:
            leaderboard_tuples = list(itertools.islice(dict_words.items(), self.MAX_LEADERBOARD_LENGTH))
        else:
            leaderboard_tuples = list(itertools.islice(dict_words.items(), len(dict_words)))
        # now get list of top words without scores
        leaderboard = [word_tuple[0] for word_tuple in leaderboard_tuples]
        return leaderboard

