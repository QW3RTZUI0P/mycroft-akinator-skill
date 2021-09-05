from mycroft import MycroftSkill, intent_file_handler
import akinator

class MycroftAkinator(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('start.akinator.intent')
    def handle_akinator_mycroft(self, message):
        aki = akinator.Akinator()
        q = aki.start_game()
        while aki.progression <= 80:
            a = self.ask_yesno(q)
            q = aki.answer(a)
        aki.win()


def create_skill():
    return MycroftAkinator()

