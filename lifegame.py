# -*- coding: utf-8 -*-
import pyxel
from enum import Enum
import copy
import random
import math


# アプリケーションウィンドウの幅
APP_WIDTH = 256
# アプリケーションウィンドウの高さ
APP_HEIGHT = 256

# セルキャンバスの幅
CANVAS_WIDTH = 48
# セルキャンバスの高さ
CANVAS_HEIGHT = 48

# セルの幅
CELL_WIDTH = APP_WIDTH / CANVAS_WIDTH
# セルの高さ
CELL_HEIGHT = APP_HEIGHT / CANVAS_HEIGHT


class AppState(Enum):
    Playing = 0
    Pausing = 1


class CellState(Enum):
    Off = 0
    On = 1


class App:
    def __init__(self):
        # 初期化
        pyxel.init(APP_WIDTH, APP_HEIGHT, fps=30)
        pyxel.mouse(True)

        self.state = AppState.Pausing

        self.focusCells = []

        # セルの初期化
        self.cells = []
        self.initCells()

        # 実行
        pyxel.run(self.update, self.draw)

    def initCells(self):
        self.cells = []
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                self.cells.append(CellState.Off)
                self.focusCells.append(False)

    def update(self):
        # 更新

        self.updateState()

        # セルを更新
        self.updateCells()

        if self.state == AppState.Playing:
            self.moveCells()
        elif self.state == AppState.Pausing:
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.moveCells()
            if pyxel.btnp(pyxel.KEY_R):
                for i in range(len(self.cells)):
                    self.cells[i] = self.getRandomCellState()
            if pyxel.btnp(pyxel.KEY_C):
                self.initCells()

    def getRandomCellState(self):
        if bool(random.getrandbits(1)):
            return CellState.On
        else:
            return CellState.Off

    def updateState(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            if self.state == AppState.Pausing:
                self.state = AppState.Playing
            else:
                self.state = AppState.Pausing

    def updateCells(self):
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                left_top_x = x * CELL_WIDTH
                left_top_y = y * CELL_HEIGHT
                right_bottom_x = left_top_x + CELL_WIDTH
                right_bottom_y = left_top_y + CELL_HEIGHT
                focus = (pyxel.mouse_x > left_top_x) and (pyxel.mouse_x < right_bottom_x) and (
                    pyxel.mouse_y > left_top_y) and (pyxel.mouse_y < right_bottom_y)
                self.setCellFocus(x, y, focus)

                if focus:
                    if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                        self.setCell(x, y, CellState.On)
                    if pyxel.btn(pyxel.MOUSE_RIGHT_BUTTON):
                        self.setCell(x, y, CellState.Off)

    def moveCells(self):
        tmp = copy.copy(self.cells)
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                index = self.getCellIndex(x, y)
                state = self.getCell(x, y)
                count = self.aroundLiveCellCount(x, y)

                # 次世代を生成
                if state == CellState.Off and count == 3:
                    tmp[index] = CellState.On
                elif state == CellState.On and (count == 2 or count == 3):
                    tmp[index] = CellState.On
                else:
                    tmp[index] = CellState.Off
        self.cells = tmp

    def aroundLiveCellCount(self, x, y):
        # 周りの生きたセルの数を算出
        count = 0
        count += self.getCellAsInt(x - 1, y - 1)
        count += self.getCellAsInt(x - 1, y)
        count += self.getCellAsInt(x - 1, y + 1)
        count += self.getCellAsInt(x, y - 1)
        count += self.getCellAsInt(x, y + 1)
        count += self.getCellAsInt(x + 1, y - 1)
        count += self.getCellAsInt(x + 1, y)
        count += self.getCellAsInt(x + 1, y + 1)
        return count

    def draw(self):
        # 描画
        # 画面を消去
        pyxel.cls(7)

        self.drawCells()
        self.drawState()

    def drawState(self):
        if self.state == AppState.Pausing:
            pyxel.text(10, 10, 'Pausing', 12)
        else:
            pyxel.text(10, 10, 'Playing', 12)

        # for y in range(CANVAS_HEIGHT):
        #     for x in range(CANVAS_WIDTH):
        #         pyxel.text(x * CELL_WIDTH, y * CELL_HEIGHT,
        #                    str(self.aroundLiveCellCount(x, y)), 8)

    def drawCells(self):
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                draw_x = x * CELL_WIDTH
                draw_y = y * CELL_HEIGHT
                pyxel.rect(draw_x, draw_y, CELL_WIDTH / 1.001,
                           CELL_HEIGHT / 1.001, self.getCellColor(x, y))

    def getCellIndex(self, x, y):
        return y * CANVAS_WIDTH + x

    def getCell(self, x, y):
        if x < 0 or y < 0 or x >= CANVAS_WIDTH or y >= CANVAS_HEIGHT:
            return CellState.Off
        return self.cells[y * CANVAS_WIDTH + x]

    def getCellAsInt(self, x, y):
        if self.getCell(x, y) == CellState.On:
            return 1
        else:
            return 0

    def getCellColor(self, x, y):
        cell = self.getCell(x, y)
        if cell == CellState.Off:
            if self.getCellFocus(x, y):
                return 5
            else:
                return 0
        else:
            if self.getCellFocus(x, y):
                return 3
            else:
                return 11

    def setCell(self, x, y, state):
        self.cells[y * CANVAS_WIDTH + x] = state

    def getCellFocus(self, x, y):
        return self.focusCells[y * CANVAS_WIDTH + x]

    def setCellFocus(self, x, y, focus):
        self.focusCells[y * CANVAS_WIDTH + x] = focus


App()
