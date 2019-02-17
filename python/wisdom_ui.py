"""
A UI for randomly generating inspirational phrases
displayed over ridiculously beautiful images.
You can even save the images for use on you favourite device.

"""

__author__ = 'James Robison'


import json
import os
import random
import sys
from functools import partial

# Qt.py from https://github.com/mottosso/Qt.py
from Qt import QtCore, QtGui, QtWidgets

import constants

_LAUNCHDIR = os.path.abspath(os.path.dirname(__file__))


class GetWisdom(QtWidgets.QWidget):
    def __init__(self):
        super(GetWisdom, self).__init__()

        self.bg_images_list = []
        self.current_font = None
        self.current_font_size = 60
        self.font_list = []
        self.font_sizes = constants.FONT_SIZES
        self.random_wisdom = ''
        self.first_run = False

        self._setup_fonts()
        self._setup_bg_images()
        self.load_prefs()
        self._setup_ui()
        self.get_random_wisdom()
        self.set_random_bg_image()
        self.update_ui()

    def _setup_ui(self):
        """ Main ui creation and assembly """
        # controls
        self.frame_image = QtWidgets.QFrame(self)
        self.frame_image.setObjectName('ImageFrame')
        self.frame_controls = QtWidgets.QFrame(self)
        self.label_display = QtWidgets.QLabel('Input Wisdom', self)
        self.label_display.setWordWrap(True)
        self.label_display.setAlignment(QtCore.Qt.AlignCenter)
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(2)
        shadow.setOffset(2.0)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.label_display.setGraphicsEffect(shadow)
        self.label_remaining = QtWidgets.QLabel('', self)
        self.label_remaining.setAlignment(QtCore.Qt.AlignRight)
        self.line_edit_wisdom = QtWidgets.QLineEdit(self)
        self.line_edit_wisdom.setMaxLength(140)
        random_phrase_button = QtWidgets.QPushButton('Randomise Phrase', self)
        random_image_button = QtWidgets.QPushButton('Randomise Image', self)
        save_button = QtWidgets.QPushButton('Save Wisdom Image', self)
        menubar = QtWidgets.QMenuBar(self)
        menubar.setNativeMenuBar(False)
        self.status_bar = QtWidgets.QStatusBar(self)

        # font family
        menu_font = menubar.addMenu('Font')
        menu_font_group = QtWidgets.QActionGroup(self)
        for font in self.font_list:
            action_font = menu_font.addAction(font, partial(self.set_font_family, font))
            action_font.setCheckable(True)
            if str(font) == self.current_font:
                action_font.setChecked(True)
            menu_font_group.addAction(action_font)

        # font size
        menu_font_size = menubar.addMenu('Font Size')
        menu_font_size_group = QtWidgets.QActionGroup(self)
        for size in self.font_sizes:
            action_font_size = menu_font_size.addAction(str(size), partial(self.set_font_size, size))
            action_font_size.setCheckable(True)
            if size == self.current_font_size:
                action_font_size.setChecked(True)
            menu_font_size_group.addAction(action_font_size)

        # layouts
        layout_v_main = QtWidgets.QVBoxLayout()
        layout_v_main.setContentsMargins(0, 0, 0, 0)
        layout_v_main.setSpacing(0)
        layout_v_image = QtWidgets.QVBoxLayout()
        layout_v_controls = QtWidgets.QVBoxLayout()
        layout_v_controls.setContentsMargins(130, 5, 130, 5)
        layout_h_buttons = QtWidgets.QHBoxLayout()
        layout_h_buttons.setContentsMargins(0, 2, 0, 2)

        # set layouts
        self.setLayout(layout_v_main)
        self.frame_image.setLayout(layout_v_image)
        self.frame_controls.setLayout(layout_v_controls)

        # add to layouts
        layout_v_main.addWidget(menubar)
        layout_v_main.addWidget(self.frame_image)
        layout_v_main.addWidget(self.frame_controls)
        layout_v_main.addWidget(self.status_bar)
        layout_v_image.addWidget(self.label_display)
        layout_v_controls.addWidget(self.line_edit_wisdom)
        layout_v_controls.addWidget(self.label_remaining)
        layout_v_controls.addLayout(layout_h_buttons)
        layout_h_buttons.addWidget(random_phrase_button)
        layout_h_buttons.addWidget(random_image_button)
        layout_h_buttons.addWidget(save_button)

        # layout settings
        layout_v_main.setStretch(0, 0)
        layout_v_main.setStretch(1, 1)
        layout_v_main.setStretch(2, 0)

        # connections
        self.line_edit_wisdom.textChanged.connect(self.update_ui)
        random_phrase_button.clicked.connect(self.get_random_wisdom)
        random_image_button.clicked.connect(self.set_random_bg_image)
        save_button.clicked.connect(self.take_screenshot)

        # style
        if self.current_font and self.current_font_size:
            self.set_font_style(self.current_font, self.current_font_size)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Wisdom")

        controls_style = """
            QWidget {background-color: white; padding: 7px;} 
            QPushButton {border-radius: 6px; border: 2px solid #E0E0E0; height: 30;}
        """
        self.frame_controls.setStyleSheet(controls_style)

        self.status_bar.showMessage("Click to randomise or type to alter text", 5000)

    def _setup_fonts(self):
        font_dir = os.path.join(_LAUNCHDIR, 'fonts')
        for font in os.listdir(font_dir):
            if font.endswith('ttf') or font.endswith('otf'):
                font_id = QtGui.QFontDatabase.addApplicationFont(os.path.join(font_dir, font))
                font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
                self.font_list.append(font_family)
                if not self.current_font:
                    self.current_font = font_family

    def _setup_bg_images(self):
        bg_image_dir = os.path.join(_LAUNCHDIR, 'images')
        for bg_image in os.listdir(bg_image_dir):
            if bg_image.endswith('.jpg'):
                self.bg_images_list.append(os.path.join(bg_image_dir, bg_image))

    def update_ui(self):
        """ Update the main display label and the remaining characters label """
        text_usage = 'Total characters: {0} - Remaining characters: {1}'
        current_text = self.line_edit_wisdom.text()
        current_text_length = len(current_text)
        remaining = 140-current_text_length
        self.label_remaining.setText(text_usage.format(current_text_length, remaining))
        self.label_display.setText(current_text if current_text else self.random_wisdom)

    def get_random_wisdom(self):
        """ Generate a new phrase from randomly chosen phrase and replacement key words """
        if self.first_run:
            phrase = constants.PHRASES[-2]
            key_word_0 = 'road'
            key_word_1 = 'chicken'
            self.first_run = False
        else:
            phrase = random.choice(constants.PHRASES)
            key_word_0 = random.choice(constants.SUB_0)
            key_word_1 = random.choice(constants.SUB_1)
        phrase_formatted = phrase.format(key_word_0, key_word_1)
        self.random_wisdom = phrase_formatted
        self.line_edit_wisdom.setText(self.random_wisdom if self.random_wisdom else '')
        self.status_bar.showMessage('Random wisdom you have chosen... or has it chosen you', 5000)

    def set_random_bg_image(self):
        """ Randomly choose and set a new bg image """
        bg_image = random.choice(self.bg_images_list)
        style = 'QFrame#ImageFrame {border-image: url("%s");}' % bg_image
        self.frame_image.setStyleSheet(style)
        self.status_bar.showMessage('A picture tells a thousand words... depending on the '
                                    'resolution', 5000)

    def set_font_family(self, font_family):
        self.current_font = str(font_family)
        self.set_font_style(font_family, self.current_font_size)

    def set_font_size(self, font_size):
        self.current_font_size = font_size
        self.set_font_style(self.current_font, font_size)

    def set_font_style(self, font_name, font_size):
        font_style = """
            font-family:"%s";
            font-size:%spx;
            color: rgb(250, 250, 250)
        """ % (font_name, font_size)
        self.label_display.setStyleSheet(font_style)

    def take_screenshot(self):
        """ Render the image frame and save to disk """
        image = QtGui.QImage(
            self.frame_image.width(),
            self.frame_image.height(),
            QtGui.QImage.Format_ARGB32
        )
        painter = QtGui.QPainter(image)
        self.frame_image.render(painter)
        painter.end()

        image_path = self.get_unique_image_path()
        image.save(image_path, 'jpg')
        self.status_bar.showMessage('Wisdom image saved to: %s' % image_path, 5000)
        QtWidgets.QMessageBox.information(self, 'Saved', 'Wisdom Image Saved!')

    def get_unique_image_path(self):
        image_name_base = str(self.label_display.text()).lower().replace(' ', '_') + '%s.jpg'
        image_path = os.path.join(constants.SAVED_IMAGES_DIR, image_name_base)
        i = 1
        while os.path.exists(image_path % i):
            i += 1
        return image_path % i

    def save_prefs(self):
        geo = self.geometry()
        pref_data = {
            'geo': (geo.x(), geo.y(), geo.width(), geo.height()),
            'font': {
                'family': self.current_font,
                'size': self.current_font_size
            }
        }
        with open(constants.PREFS_FILE_PATH, 'w') as js_file:
            json.dump(pref_data, js_file, indent=4)

    def load_prefs(self):
        prefs_data = constants.DEFAULT_PREFS
        if os.path.exists(constants.PREFS_FILE_PATH):
            with open(constants.PREFS_FILE_PATH, 'r') as js_file:
                prefs_data = json.load(js_file)
        else:
            self.first_run = True
        self.apply_prefs(prefs_data)

    def apply_prefs(self, prefs_data):
        if 'geo' in prefs_data:
            self.setGeometry(*prefs_data['geo'])
        if 'font' in prefs_data:
            self.current_font = prefs_data['font']['family']
            self.current_font_size = prefs_data['font']['size']

    def closeEvent(self, event):
        self.save_prefs()
        event.accept()


def run_get_wisdom():
    app = QtWidgets.QApplication(sys.argv)
    wisdom_widget = GetWisdom()
    wisdom_widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_get_wisdom()