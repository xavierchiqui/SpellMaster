from collections import ChainMap
import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner


class SpellEntry:
    def __init__(self, name, sp_type, archetype, equipment, school, sp_range, incant, materials, effects, limits, notes):
        self.name = name
        self.sp_type = sp_type
        self.archetype = archetype
        self.equipment = equipment
        self.school = school
        self.sp_range = sp_range
        self.incant = incant
        self.materials = materials
        self.effects = effects
        self.limits = limits
        self.notes = notes

    def __str__(self):
        return self.name


class SpellListEntry:
    def __init__(self, spell, level, cost, max_buy, frequency, list_range):
        self.spell = spell
        self.level = level
        self.cost = cost
        # self.cost_override = None
        self.max_buy = max_buy
        # self.max_buy_override = None
        self.frequency = frequency
        # self.frequency_override = None
        self.list_range = list_range
        # self.range_override = None
        # self.limit_override = None
        # self.color_override = None
        self.visible = True
        # self.visible_override = None


class SpellList:
    def __init__(self):
        player_classes = ['Bard', 'Druid', 'Healer', 'Wizard']
        self.spell_list = {class_type: SpellList.build_list(class_type) for class_type in player_classes}

    @staticmethod
    def build_list(class_type):
        #TODO construct dict from DB
        default_list = {}
        override_list = {}
        return ChainMap(override_list, default_list)


def change_screen(self, screen_name):
        self.manager.current = screen_name


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)

        main_frame = BoxLayout()
        button_frame = BoxLayout(orientation='vertical')
        button_frame.add_widget(Widget())
        button_frame.add_widget(Button(text="New Spell List", font_size='30dp',
                                       on_press=lambda x: change_screen(self, 'new_list')))
        button_frame.add_widget(Button(text="Load Spell List", font_size='30dp',
                                       on_press=lambda x: change_screen(self, 'load_list')))
        button_frame.add_widget(Button(text='Edit Spell Database', font_size='30dp',
                                       on_press=lambda x: change_screen(self, 'edit_spell_screen')))
        button_frame.add_widget(Button(text='Exit', font_size='30dp',
                                       on_press=lambda x: App.get_running_app().stop()))
        button_frame.add_widget(Widget())
        main_frame.add_widget(Widget())
        main_frame.add_widget(button_frame)
        main_frame.add_widget(Widget())
        self.add_widget(main_frame)


class EditSpellScreen(Screen):
    def __init__(self, **kwargs):
        super(EditSpellScreen, self).__init__(**kwargs)
        spell_name_box = BoxLayout()
        spell_name_box.add_widget(Label(text='Name', font_size='30dp'))
        spell_name_input = TextInput(text="None", font_size='30dp', multiline=False)
        spell_name_box.add_widget(spell_name_input)

        spell_type_box = BoxLayout()
        spell_type_box.add_widget(Label(text='Type', font_size='30dp'))
        spell_type_input = Spinner(
            text='Verbal',
            values=('Verbal', 'Enchantment', 'Magic Ball', 'Meta-Magic',
                    'Archetype', 'Equipment', 'Neutral', 'Specialty Arrow'),
            font_size='30dp'
        )
        spell_type_box.add_widget(spell_type_input)

        spell_school_box = BoxLayout()
        spell_school_box.add_widget(Label(text='School', font_size='30dp'))
        spell_school_input = Spinner(
            text='Command',
            values=('Command', 'Death', 'Flame', 'Neutral', 'Protection', 'Sorcery', 'Spirit', 'Subdual'),
            font_size='30dp'
        )
        spell_school_box.add_widget(spell_school_input)

        spell_range_box = BoxLayout()
        spell_range_box.add_widget(Label(text='Range', font_size='30dp'))
        spell_range_input = Spinner(
            text='20ft',
            values=('20ft', '50ft', 'Self', 'Touch', 'Self-Touch', 'Ball', '-'),
            font_size='30dp'
        )
        spell_range_box.add_widget(spell_range_input)

        spell_incant_box = BoxLayout()
        spell_incant_box.add_widget(Label(text='Incantation', font_size='30dp'))
        spell_incant_input = TextInput(text="None", font_size='30dp')
        spell_incant_box.add_widget(spell_incant_input)

        spell_materials_box = BoxLayout()
        spell_materials_box.add_widget(Label(text='Materials', font_size='30dp'))
        spell_materials_input = TextInput(text='None', font_size='30dp')
        spell_materials_box.add_widget(spell_materials_input)

        spell_effects_box = BoxLayout()
        spell_effects_box.add_widget(Label(text='Effects', font_size='30dp'))
        spell_effects_input = TextInput(text='None', font_size='30dp')
        spell_effects_box.add_widget(spell_effects_input)

        spell_limits_box = BoxLayout()
        spell_limits_box.add_widget(Label(text='Limits and Restrictions', font_size='30dp'))
        spell_limits_input = TextInput(text='None', font_size='30dp')
        spell_limits_box.add_widget(spell_limits_input)

        spell_notes_box = BoxLayout()
        spell_notes_box.add_widget(Label(text='Notes', font_size='30dp'))
        spell_notes_input = TextInput(text='None', font_size='30dp')
        spell_notes_box.add_widget(spell_notes_input)

        def save_list(*_):
            name = spell_name_input.text
            spell_type = spell_type_input.text
            school = spell_school_input.text
            archetype = False
            equipment = False
            if spell_type == 'Archetype':
                spell_type = 'Neutral'
                school = 'Neutral'
                archetype = True
            if spell_type == 'Equipment':
                spell_type = 'Neutral'
                school = 'Neutral'
                equipment = True
            spell_range = spell_range_input.text
            incant = spell_incant_input.text
            materials = spell_materials_input.text
            effects = spell_effects_input.text
            limits = spell_limits_input.text
            notes = spell_notes_input.text

            con = sqlite3.connect('spells.db')
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO spell VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                            (name,
                             spell_type,
                             equipment,
                             archetype,
                             school,
                             spell_range,
                             incant,
                             materials,
                             effects,
                             limits,
                             notes
                             ))
            clear_list()

        def clear_list(*_):
            spell_name_input.text = 'None'
            spell_type_input.text = 'Verbal'
            spell_school_input.text = 'Command'
            spell_range_input.text = '20'
            spell_incant_input.text = 'None'
            spell_materials_input.text = 'None'
            spell_effects_input.text = 'None'
            spell_limits_input.text = 'None'
            spell_notes_input.text = 'None'

        button_box = BoxLayout()
        button_box.add_widget(Button(
                text='Save',
                font_size='30dp',
                on_press=save_list
        ))
        button_box.add_widget(Button(
                text="Clear",
                font_size='30dp',
                on_press=clear_list
        ))
        button_box.add_widget(Button(
                text='Main Menu',
                font_size='30dp',
                on_press=lambda x: change_screen(self, 'main_menu_screen')
        ))
        button_box.add_widget(Button(
                text='Exit',
                font_size='30dp',
                on_press=lambda x: App.get_running_app().stop()
        ))

        inner_box = BoxLayout(orientation='vertical')
        inner_box.add_widget(Widget())
        inner_box.add_widget(spell_name_box)
        inner_box.add_widget(spell_type_box)
        inner_box.add_widget(spell_school_box)
        inner_box.add_widget(spell_range_box)
        inner_box.add_widget(spell_incant_box)
        inner_box.add_widget(spell_materials_box)
        inner_box.add_widget(spell_effects_box)
        inner_box.add_widget(spell_limits_box)
        inner_box.add_widget(spell_notes_box)
        inner_box.add_widget(Widget())
        inner_box.add_widget(button_box)
        inner_box.add_widget(Widget())

        outer_box = BoxLayout()
        outer_box.add_widget(Widget())
        outer_box.add_widget(inner_box)
        outer_box.add_widget(Widget())

        self.add_widget(outer_box)


class SpellMasterApp(App):

    def build(self):
       # Window.size = (1920, 1080)
       # Window.fullscreen = True
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainMenuScreen(name='main_menu_screen'))
        screen_manager.add_widget(EditSpellScreen(name='edit_spell_screen'))
        return screen_manager


if __name__ == '__main__':
    SpellMasterApp().run()
