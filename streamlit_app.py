import streamlit as st
import requests
import time

class WordleGame:
    def __init__(self):
        self.word = None
        self.score = 0
        self.guesses = []

    def start_new_game(self):
        self.word = self._get_random_word()
        self.score = 0
        self.guesses = []

    def guess_word(self, word):
        if len(word) != 5:
            return False, "The word must be 5 letters long."

        if not self._is_valid_word(word):
            return False, "Invalid word."

        self.score += 1
        self.guesses.append(word)

        if word == self.word:
            return True, "You won! You guessed the word."

        return False, self._get_wordle_hint(word)

    def _get_random_word(self):
        url = "https://random-word-api.herokuapp.com/word?number=1&length=5"
        response = requests.get(url)
        data = response.json()
        word = data[0]
        return word.lower()

    def _is_valid_word(self, word):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        return response.status_code == 200

    def _get_wordle_hint(self, word):
        hint = ""
        for i, letter in enumerate(word):
            if letter == self.word[i]:
                hint += letter
            elif letter in self.word:
                hint += "*"
            else:
                hint += "_"
        return hint


hide_menu = """
    <style>
    #MainMenu {visibility : hidden;}
    footer {visibility : hidden ; }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html = True)


st.set_page_config(page_title='🦭ANoTHERWoRDLE')

game = WordleGame()
# Timer
start_time = None
elapsed_time = None

st.title("Wordle")

if st.button("Start New Game"):
    game.start_new_game()
    start_time = time.time()

# Guess Word
if game.word:
    st.text("Enter a 5-letter word:")
    word_input = st.text_input("", max_chars=5)

    if st.button("Guess"):
        if word_input:
            result, message = game.guess_word(word_input.lower())
            st.text(f"Result: {message}")
            if result:
                elapsed_time = time.time() - start_time
                st.text(f"Elapsed Time: {int(elapsed_time)} seconds")
                st.text(f"Score: {game.score}")

# Display Score
if elapsed_time:
    st.text("Scoreboard")
    st.text(f"Score: {game.score}")
    st.text(f"Elapsed Time: {int(elapsed_time)} seconds")

