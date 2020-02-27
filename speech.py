#!/usr/bin/env python
# coding: utf-8

# In[10]:


import random
import time
#pip install speechrecognition
#pip install pyaudio
import speech_recognition as sr

#returns 1 or 0. 1 => word detected matches inputted spell. 0 => fail
def speech_spell(spell):
    def recognize_speech_from_mic(recognizer, microphone):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response


    if __name__ == "__main__":
        # debug: set the list of words, maxnumber of guesses, and prompt limit. default should be 1, with no word bank
        #WORDS = ["Expelliarmus", "wingardium levoisa", "catfish", "sesame", "wang"]
        NUM_GUESSES = 1
        PROMPT_LIMIT = 1

        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        # correct word
        word = spell

        # debug: print the instructions string
    #     instructions = (
    #         "Wordbank:\n"
    #         "{words}\n"
    #         "You have {n} tries.\n"
    #     ).format(words=', '.join(WORDS), n=NUM_GUESSES)

        #print(instructions)
        #time.sleep(1)

        for i in range(NUM_GUESSES):
            # get the guess from the user
            # if a transcription is returned, break out of the loop and
            #     continue
            # if no transcription returned and API request failed, break
            #     loop and continue
            # if API request succeeded but no transcription was returned,
            #     we treat it as a fail, since PROMPT_LIMIT is set to 1
            #    
            for j in range(PROMPT_LIMIT):
                #print('Guess {}. Go!'.format(i+1))
                guess = recognize_speech_from_mic(recognizer, microphone)
                if guess["transcription"]:
                    break
                if not guess["success"]:
                    break
                #print("Didn't catch that. Try again\n")

            # if there was an error, stop the game
            if guess["error"]:
                #print(0)
                return 0
                break

            # debug: show what user said
            #print("You said: {}".format(guess["transcription"]))

            # determine if guess is correct and if any attempts remain
            guess_is_correct = guess["transcription"].lower() == word.lower()
            user_has_more_attempts = i < NUM_GUESSES - 1

            # determine if the user has won the game
            # if not, repeat the loop if user has more attempts
            # if no attempts left, the user loses the game
            if guess_is_correct:
                return 1
                break
#             elif user_has_more_attempts:
#                 print("Incorrect. Try again.\n")
            else:
                return 0
                break





