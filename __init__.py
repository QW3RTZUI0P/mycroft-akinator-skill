from mycroft import MycroftSkill, intent_file_handler
from mycroft.api import DeviceApi

import akinator

class MycroftAkinator(MycroftSkill):

    """ The two letter country code of the Mycroft device
    """
    language_code = ""

    def __init__(self):
        """ Constructor method
        """
        MycroftSkill.__init__(self)

    def initialize(self):
        """ Initialization method
        """
        MycroftAkinator.language_code = str(DeviceApi().get_location()["city"]["state"]["country"]["code"]).lower()

    def ask_akinator(self, aki, first_question, probability):
        """ Handle the questions and answers during the akinator game
        
        :param self: the current instance of this skill
        :param aki: the current instance of Akinator
        :param first_question: the first question to be answered by the user
        :param probability: the percentage Akinator needs to guess the person. The higher the greater probability of the right choice
        """
        question = first_question
        while aki.progression <= probability:
            answer = self.ask_yesno(question + "\n\t")
            question = aki.answer(answer)
        return aki.win()



    @intent_file_handler('start.akinator.intent')
    def handle_akinator_mycroft(self, message):
        """ Start the Akinator game and handle its end
        """
        aki = akinator.Akinator()
        first_question = aki.start_game(language = MycroftAkinator.language_code)
        win_data = MycroftAkinator.ask_akinator(self, aki, first_question, 80)
        self.speak_dialog("guess", {"name": win_data["name"]})
        final_answer = self.ask_yesno("was.i.correct")

        if final_answer == "yes":
            self.speak_dialog("success")
        elif final_answer == "no":
            self.speak_dialog("failure")
            #TODO: implement ability to continue the game and let akinator guess again
        #TODO: let Mycroft suggest to play another round
        


def create_skill():
    return MycroftAkinator()

