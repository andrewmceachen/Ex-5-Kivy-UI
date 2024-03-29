import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.animation import Animation
from kivy.clock import Clock

from pidev.Joystick import Joystick
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
NEW_SCREEN_NAME = 'balls'

buttonstate = "On"
buttonstate2 = "Motor On"
joypos = "0.0, 0.0"
pos = "waiting"

joy = Joystick(0, True)

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    buttonstate = ObjectProperty()
    joypos = ObjectProperty()

    def __init__(self,**kwargs):
        Clock.schedule_interval(self.joyclock,.1)
        print("clock schedule created")
        super(MainScreen,self).__init__(**kwargs)
    def pressed(self,buttonstate):
        if buttonstate == "On":
            buttonstate = "Off"
            print("Button Toggled")
        else:
            buttonstate = "On"
            print("Button Toggled")
        return str(buttonstate)

    def counter(self,val):
        return str(int(val)+1)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def joystick(self,joypos):
        joypos = joy.get_axis('x'), joy.get_axis('y')
        return "Position:" + str(joypos)

    def joyclock(self,pos):
        self.x_val,self.y_val = joy.get_both_axes()
        self.ids.x.text = "x: " + str(round(self.x_val,2))
        self.ids.y.text = "y: " + str(round(self.y_val, 2))



    def motor(self,buttonstate2):
        if buttonstate2 == "Motor On":
            buttonstate2 = "Motor Off"
        else:
            buttonstate2 = "Motor On"
        return str(buttonstate2)

    def balls(self):
        SCREEN_MANAGER.current = NEW_SCREEN_NAME

class NewScreen(Screen):
    def mainbutton(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def glagas(self, *args):
        animate = Animation(x=100) + Animation(y=100) + Animation(x=900) + Animation(y=400)
        widget = self.ids.anim1
        animate.start(widget)


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name=NEW_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()