from mycroft import MycroftSkill, intent_file_handler
from mycroft.api import DeviceApi

import akinator

class MycroftAkinator(MycroftSkill):

    # The two letter country code of the Mycroft device
    language_code = ""
    # whether to set Akinator to child mode (can be changed in skill settings on home.mycroft.ai)
    child_mode = True

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        # gets the two-letter country code of the user's Mycroft device
        MycroftAkinator.language_code = self.lang[:2]
        # gets the option for child mode from the Mycroft settings
        MycroftAkinator.child_mode = self.settings.get("child_mode")

    def ask_akinator(self, aki, first_question, probability):
        """ Handle the questions and answers during the akinator game
        
        :param self: the current instance of this skill
        :param aki: the current instance of Akinator
        :param first_question: the first question to be answered by the user
        :param probability: the percentage Akinator needs to guess the person. The higher the greater probability of the right choice
        """
        question = first_question
        while aki.progression <= probability:
            answer = self.ask_yesno(question)
            if answer == "yes" or answer == "no":
                answer = answer
            elif self.voc_match(answer, "stop") == True:
                # TODO: is there a better way to stop the execution of the skill
                return "stop"
            # TODO: maybe put the last two clauses together?
            elif self.voc_match(answer, "i.dont.know") == True:
                answer = "idk"
            else:
                answer = "idk"
            question = aki.answer(answer) 
        return aki.win()



    @intent_file_handler('start.akinator.intent')
    def handle_akinator_mycroft(self, message):
        """ Start the Akinator game and handle its end
        """
        self.speak_dialog("starting.akinator")
        self.speak_dialog("think.of.a.character")
        aki = akinator.Akinator()
        first_question = aki.start_game(language = MycroftAkinator.language_code, child_mode = MycroftAkinator.child_mode)
        # starts the process of asking the questions
        # 80 is the probability at which Akinator will take his guess as to who the user thought of (Akinator is 80% sure that he has the right person)
        # this value is recommended by the API
        win_data = MycroftAkinator.ask_akinator(self, aki, first_question, 80)
        if win_data == "stop":
            return
        self.speak_dialog("guess", {"name": win_data["name"]})
        final_answer = self.ask_yesno("am.i.correct")

        if final_answer == "yes":
            self.speak_dialog("success")
        elif final_answer == "no":
            self.speak_dialog("failure")
        else:
            return
        


def create_skill():
    return MycroftAkinator()

