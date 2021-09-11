from mycroft import MycroftSkill, intent_file_handler
from mycroft.api import DeviceApi
import akinator

class MycroftAkinator(MycroftSkill):

    language_code = ""

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        MycroftAkinator.language_code = str(DeviceApi().get_location()["city"]["state"]["country"]["code"]).lower()

    @intent_file_handler('start.akinator.intent')
    def handle_akinator_mycroft(self, message):
        aki = akinator.Akinator()
        question = aki.start_game(language = "en")
        while aki.progression <= 85:
            answer = self.ask_yesno(question)
            question = aki.answer(answer)
        self.speak(aki.win())


def create_skill():
    return MycroftAkinator()

