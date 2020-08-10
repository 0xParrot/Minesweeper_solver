#!/usr/bin/env python3
import json
from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import time

def flagBombs(falseCells):
    for cell in falseCells:
        elementId = "%d_%d" % (cell[0] + 1 , cell[1] + 1 )
        element = driver.find_element_by_id(elementId)
        if(element.get_attribute("class") != "square bombflagged" ):
            driver.execute_script("document.getElementById('%s').setAttribute('class','square bombflagged');" % (elementId))
            cells[cell[0]][cell[1]] = "BOMB"
def checkBomb(rowidx,cellidx,posses):
    falseCells = []
    bombCells = []
    cellVal = cells[rowidx][cellidx]
    for poss in posses:
        posscell = cells[poss[0]][poss[1]]
        if(str(posscell) == 'False'):
            falseCells.append([poss[0],poss[1]])
        elif(posscell == "BOMB"):
            falseCells.append([poss[0],poss[1]])
    if( (len(falseCells)+len(bombCells)) == cellVal and len(bombCells) != cellVal   ):
        flagBombs(falseCells)
def bombStart():
    for rowidx,row in enumerate(cells):
        for cellidx,cell in enumerate(row):
            if(cell != False):
                cellposses = possiblities[rowidx][cellidx]
                checkBomb(rowidx,cellidx,cellposses)
def updateCellNumbers(elems,number):
    for cell in elems:
        cell = cell.get_attribute("id").split("_")
        rowidx = int(cell[0])-1
        cellidx = int(cell[1])-1
        cells[rowidx][cellidx] = number
def updateCells(driver):
    for cellNumber in range(0,7):
        try:
            elems = driver.find_elements_by_class_name("open%d" % cellNumber)
        except:
            elems = None
        if(elems):
            updateCellNumbers(elems,cellNumber)
def defuse(posses):
    for cell in posses:
        print(cell)
        elementId = "%d_%d" % (cell[0] + 1 , cell[1] + 1 )
        driver.find_element_by_id(elementId).click()
def checkNotBomb(rowidx,cellidx,posses):
    falseCells = []
    bombCells = []
    cellVal = cells[rowidx][cellidx]
    for poss in posses:
        posscell = cells[poss[0]][poss[1]]
        if(str(posscell) == 'False'):
            falseCells.append([poss[0],poss[1]])
        elif(str(posscell) == 'BOMB'):
            bombCells.append([poss[0],poss[1]])
    if(len(bombCells) == cellVal and len(falseCells) > 0):
        defuse(falseCells)
def updateNonBomb():
    for rowidx,row in enumerate(cells):
        for cellidx,cell in enumerate(row):
            if(str(cell).isnumeric()):
                cellposses = possiblities[rowidx][cellidx]
                checkNotBomb(rowidx,cellidx,cellposses)
def checkSolved():
    for row in cells:
        for cell in row:
            if(cell == False):
                return False            
    return True
cells = [[False for i in range(16)] for i in range(16)]
possiblities = json.load(open("possiblities.json"))
driver = Chrome()
actionChains = ActionChains(driver) 
driver.get("http://minesweeperonline.com/#intermediate-200")
driver.find_element_by_id("8_9").click()
while(1):
    updateCells(driver)
    if(checkSolved()):
        print("YOY")
        exit()
    bombStart()
    updateNonBomb()