from mycroft import MycroftSkill, intent_file_handler


class MycroftAkinator(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('akinator.mycroft.intent')
    def handle_akinator_mycroft(self, message):
        self.speak_dialog('akinator.mycroft')


def create_skill():
    return MycroftAkinator()

