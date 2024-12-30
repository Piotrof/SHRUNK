#!/usr/bin/env python3

import sys
import random
import string
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget

class ShrunkTerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ------------ CONFIGURABLE COLORS / FONTS ------------
        self.bg_color = "#24273A"
        self.fg_color = "#C6A0D7"
        self.address_color = "#ff0000"
        self.font_family = "Courier New"
        self.font_size = 16

        # ------------ FIRST NAME ------------
        self.first_name = self.generate_first_name(8)
        self.first_name_timer = QTimer(self)
        self.first_name_timer.timeout.connect(self.update_first_name)
        self.first_name_timer.start(2000)  # 2s

        # ------------ LAST NAME (FADES) ------------
        self.last_name = ""
        self.last_name_length = 20
        self.last_name_timer = QTimer(self)
        self.last_name_timer.timeout.connect(self.fade_last_name)
        self.last_name_timer.start(200)  # 0.2s

        # ------------ ADDRESS (FLOATING GLYPHS) ------------
        self.address_length = 20
        self.address_chars = []
        self.address_offsets = []
        self.address_directions = []
        self.generate_address()
        self.address_timer = QTimer(self)
        self.address_timer.timeout.connect(self.animate_address)
        self.address_timer.start(100)  # 0.1s

        # ------------ TELEPHONE (GRAFFITI PHRASES) ------------
        self.graffiti_phrases = [
            "CBGB RULES",
            "LISA WAS HERE",
            "OUIJA IS FAKE",
            "CALL 555-GHOST",
            "PUNK ROCK LIVES",
            "PSYCHIC MACHINE",
            "DEAD KENNEDYS",
            "JOEY RAMONE LIVES",
            "THIS PLACE SUCKS",
            "HELLO FROM THE OTHER SIDE",
            "ANARCHY AT CBGB",
        ]
        self.telephone = self.generate_graffiti()
        self.telephone_timer = QTimer(self)
        self.telephone_timer.timeout.connect(self.update_graffiti)
        self.telephone_timer.start(3000)  # 3s

        # ------------ SOCIAL (SUDOKU) ------------
        self.sudoku_puzzle = [
            [0,0,0, 2,6,0, 7,0,1],
            [6,8,0, 0,7,0, 0,9,0],
            [1,9,0, 0,0,4, 5,0,0],
            [8,2,0, 1,0,0, 0,4,0],
            [0,0,4, 6,0,2, 9,0,0],
            [0,5,0, 0,0,3, 0,2,8],
            [0,0,9, 3,0,0, 0,7,4],
            [0,4,0, 0,5,0, 0,3,6],
            [7,0,3, 0,1,8, 0,0,0],
        ]
        self.sudoku_solution = [
            [4,3,5, 2,6,9, 7,8,1],
            [6,8,2, 5,7,1, 3,9,4],
            [1,9,7, 8,3,4, 5,6,2],
            [8,2,6, 1,9,5, 2,4,7],
            [3,7,4, 6,8,2, 9,1,5],
            [9,5,1, 7,4,3, 6,2,8],
            [5,1,9, 3,2,6, 8,7,4],
            [2,4,8, 9,5,7, 1,3,6],
            [7,6,3, 4,1,8, 2,5,9],
        ]
        self.sudoku_empty_cells = []
        for r in range(9):
            for c in range(9):
                if self.sudoku_puzzle[r][c] == 0:
                    self.sudoku_empty_cells.append((r,c))

        self.sudoku_fill_index = 0
        self.sudoku_filling_timer = QTimer(self)
        self.sudoku_filling_timer.timeout.connect(self.fill_next_sudoku_cell)
        self.sudoku_filling_timer.start(1000)  # 1s
        self.sudoku_reset_timer = QTimer(self)
        self.sudoku_reset_timer.setSingleShot(True)
        self.sudoku_reset_timer.timeout.connect(self.reset_sudoku)

        # ------------ ICE (CAT ASCII + Floating Z’s) ------------
        self.ice_color = "#dddddd"  # off-white
        # A single, static cat ASCII block
        self.cat_ascii = [
            r"  |\      _,,,---,,_",
            r"  /,`.-'`'    -.  ;-;;,_",
            r" |,4-  ) )-,_. ,\ (  `'-'",
            r"'---''(_/--'  `-'\'_)"
        ]
        
        self.z_chars = list("ZZZz")  # each character is animated up/down
        self.z_offsets = [0] * len(self.z_chars)
        self.z_directions = [1, -1, 1, -1]  # for a simple alternating pattern

        # Timer for the Z animation
        self.z_timer = QTimer(self)
        self.z_timer.timeout.connect(self.animate_ice_z)
        self.z_timer.start(150)  # 0.15s - subtle “wobble”

        self.setWindowTitle("SHRUNK")
        self.setMinimumSize(800, 600)

    # ----------------------------------------------------------------
    #                         DATA GENERATION
    # ----------------------------------------------------------------
    def generate_first_name(self, length=8):
        pool = string.ascii_letters + string.digits + "!@#$%^&*()_+-=<>?/|\\{}[]~"
        return ''.join(random.choices(pool, k=length))

    def update_first_name(self):
        self.first_name = self.generate_first_name(8)
        self.update()

    def generate_vowels(self, length=20):
        return ''.join(random.choices("AEIOU", k=length))

    def generate_address(self):
        glyphs = string.ascii_letters + string.digits + "!@#$%^&*()_+-=<>?/|\\{}[]~"
        self.address_chars = [random.choice(glyphs) for _ in range(self.address_length)]
        self.address_offsets = [0]*self.address_length
        self.address_directions = [1 if i%2==0 else -1 for i in range(self.address_length)]

    def generate_graffiti(self):
        return random.choice(self.graffiti_phrases)

    def update_graffiti(self):
        self.telephone = self.generate_graffiti()
        self.update()

    # ----------------------------------------------------------------
    #                     LAST NAME (FADES)
    # ----------------------------------------------------------------
    def fade_last_name(self):
        if not self.last_name:
            self.last_name = self.generate_vowels(self.last_name_length)
        else:
            self.last_name = self.last_name[:-1]
        self.update()

    # ----------------------------------------------------------------
    #            ADDRESS ANIMATION (UP/DOWN)
    # ----------------------------------------------------------------
    def animate_address(self):
        for i in range(self.address_length):
            if self.address_directions[i] > 0:
                self.address_offsets[i] += 1
                if self.address_offsets[i] >= 3:
                    self.address_directions[i] = -1
            else:
                self.address_offsets[i] -= 1
                if self.address_offsets[i] <= -3:
                    self.address_directions[i] = 1
        self.update()

    # ----------------------------------------------------------------
    #            SOCIAL (SUDOKU) ANIMATION
    # ----------------------------------------------------------------
    def fill_next_sudoku_cell(self):
        if self.sudoku_fill_index < len(self.sudoku_empty_cells):
            r, c = self.sudoku_empty_cells[self.sudoku_fill_index]
            self.sudoku_puzzle[r][c] = self.sudoku_solution[r][c]
            self.sudoku_fill_index += 1
            self.update()
        else:
            self.sudoku_filling_timer.stop()
            self.sudoku_reset_timer.start(5000)  # 5s

    def reset_sudoku(self):
        self.reset_puzzle_to_initial()
        self.sudoku_fill_index = 0
        self.sudoku_filling_timer.start(1000)
        self.update()

    def reset_puzzle_to_initial(self):
        for (r, c) in self.sudoku_empty_cells:
            self.sudoku_puzzle[r][c] = 0

    def get_ascii_sudoku(self):
        lines = []
        for row_i, row in enumerate(self.sudoku_puzzle):
            if row_i % 3 == 0 and row_i != 0:
                lines.append("- - - + - - - + - - -")
            row_parts = []
            for col_i, val in enumerate(row):
                if col_i % 3 == 0 and col_i != 0:
                    row_parts.append("|")
                char = str(val) if val != 0 else "."
                row_parts.append(char)
            lines.append(" ".join(row_parts))
        return "\n".join(lines)

    # ----------------------------------------------------------------
    #                ICE: Animate Z’s above the static cat
    # ----------------------------------------------------------------
    def animate_ice_z(self):
        """
        Each character in "ZZZz" floats up or down by 1 pixel,
        reversing direction at ±2.
        """
        for i in range(len(self.z_chars)):
            if self.z_directions[i] > 0:
                self.z_offsets[i] += 1
                if self.z_offsets[i] >= 2:
                    self.z_directions[i] = -1
            else:
                self.z_offsets[i] -= 1
                if self.z_offsets[i] <= -2:
                    self.z_directions[i] = 1
        self.update()

    # ----------------------------------------------------------------
    #                      PAINT EVENT
    # ----------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(self.bg_color))

        font = QFont(self.font_family, self.font_size)
        painter.setFont(font)
        fm = painter.fontMetrics()

        line_height = fm.height() + 10
        x_margin = 30
        y_start = 60

        # Title
        painter.setPen(QColor(self.fg_color))
        painter.drawText(x_margin, y_start, "~~SHRUNK~~")

        # FIRST NAME
        y_pos = y_start + line_height
        painter.drawText(x_margin, y_pos, f"FIRST NAME: {self.first_name}")

        # LAST NAME
        y_pos += line_height
        painter.drawText(x_margin, y_pos, f"LAST NAME: {self.last_name}")

        # ADDRESS
        y_pos += line_height
        painter.drawText(x_margin, y_pos, "ADDRESS: ")

        painter.setPen(QColor(self.address_color))
        x_address = x_margin + fm.width("ADDRESS: ")
        baseline = y_pos
        for i, ch in enumerate(self.address_chars):
            offset_y = baseline + self.address_offsets[i]
            painter.drawText(x_address, offset_y, ch)
            x_address += fm.width(ch)

        # TELEPHONE
        painter.setPen(QColor(self.fg_color))
        y_pos += line_height
        painter.drawText(x_margin, y_pos, f"TELEPHONE: {self.telephone}")

        # SOCIAL (Sudoku)
        painter.drawText(x_margin, y_pos + line_height, "SOCIAL:")
        y_pos += line_height * 2

        sudoku_str = self.get_ascii_sudoku()
        sudoku_lines = sudoku_str.split("\n")
        for s_line in sudoku_lines:
            painter.drawText(x_margin, y_pos, s_line)
            y_pos += line_height

        y_pos -= line_height
        # ICE: Draw the label
        painter.drawText(x_margin, y_pos + line_height, "ICE:")

        # ICE: cat ASCII + the Z’s that move up/down individually
        painter.setPen(QColor(self.ice_color))

        # Additional blank line before the cat
        y_pos += line_height * 2  # This adds one more blank line

        # 1) Draw the static cat lines
        cat_line_height = fm.height()
        for cat_line in self.cat_ascii:
            painter.drawText(x_margin, y_pos, cat_line)
            y_pos += cat_line_height

        # 2) Draw each Z individually, near the cat’s top-left
        cat_top = y_pos - len(self.cat_ascii) * cat_line_height
        z_base_x = x_margin + 100
        z_base_y = cat_top + fm.height()

        for i, z_ch in enumerate(self.z_chars):
            z_y = z_base_y + i * cat_line_height + self.z_offsets[i]
            painter.drawText(z_base_x, z_y, z_ch)

        # MEDICAL HISTORY
        painter.setPen(QColor(self.fg_color))
        painter.drawText(x_margin, y_pos + line_height, "MEDICAL HISTORY: ---")


def main():
    app = QApplication(sys.argv)
    window = ShrunkTerminalWidget()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
