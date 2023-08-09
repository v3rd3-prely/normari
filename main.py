import PySimpleGUI as sg
import xlsxwriter
import os
import time
from datetime import datetime

textFont = ('Any', 16)
timeFont = ('Any', 32)

# Create directory for file and returns path to file

def createValidFilePath(path, name):
    path += '/'
    extension = '.xlsx'

    if not os.path.exists(path):
        os.makedirs(path)
    while os.path.exists(path+name+extension):
        # print('File already exists.')
        val = 1
        if name.endswith(')'):
            # print('copy')
            name = name.split('(')
            val = int(name[1].split(')')[0])
            val += 1
            name = name[0]
            # print(name)
            # print(val)
        name += '('+str(val)+')'
    return path+name+extension

# Writing Excel file

def writeExcelFile(path, filename, data):
    fullpath = createValidFilePath(path, filename)
    workbook = xlsxwriter.Workbook(fullpath)
    worksheet = workbook.add_worksheet()
    if data[0][0] == 'continous':
        for index in range(0, len(data[1])):
            if len(data[1][index]) > 1 :
                worksheet.merge_range(index*2, 0, index*2+1, 0, '')
                worksheet.merge_range(index*2, 1, index*2+1, 1, '')
                worksheet.write(index*2+1, 2, data[1][index][1])
                worksheet.write(index*2, 2, data[1][index][1])
            for column in range(2, len(data[1][index])):
                worksheet.write(index*2+1, column+1, data[1][index][column])
                worksheet.write(index*2, column+1, data[1][index][column]-data[1][index][column-1])
    elif data[0][0] == 'parallel':
        for index in range(0, data[0][1]):
            worksheet.merge_range(index*2, 0, index*2+1, 0, '')
            worksheet.merge_range(index*2, 1, index*2+1, 1, '')

        for index in range(0, len(data[1])):
            if len(data[1][index]) > 1 :
                # worksheet.merge_range(index*2, 0, index*2+1, 0, '')
                # worksheet.merge_range(index*2, 1, index*2+1, 1, '')
                worksheet.write(1, index+2, data[1][index][1])
                worksheet.write(0, index+2, data[1][index][1])
            for row in range(2, len(data[1][index])):
                worksheet.write(row*2-1, index+2, data[1][index][row])
                worksheet.write(row*2-2, index+2, data[1][index][row]-data[1][index][row-1])
    workbook.close()

def formatTime(value):
    precision = 1000
    diff = int(value/60*precision)
    return diff/precision

def runTumer():
    timerLayout = [[
        sg.Column([
            [sg.Text('Please select type of operation:', key='-operation-type-')],
            [
                sg.Button('Continuu', key='-set-continous-', button_color=('black', 'grey')),
                sg.Button('Paralel', key='-set-parallel-', button_color=('black', 'grey'))
            ],
            [sg.Text('Enter number of operations (for parallel only):', key='-text-')],
            [sg.InputText('1',disabled=False, key='-operation-name-'), sg.Button('Ok', key='-set-operation-name-')],
            [
                sg.Button('Set', key='-set-timer-', button_color=('white', 'blue')),
                sg.Button('Reset', key='-reset-timer-', button_color=('white', 'red')),
                sg.Button('Pause', key='-pause-timer-', button_color=('white', 'blue')),
                sg.Button('Undo', key='-undo-timer-', button_color=('white', 'blue')),
            ],
            [
                sg.Text('0:', key='-current-operation-number-', size=(4, 1), font=timeFont),
                sg.Text('', key='-current-time-', size=(8, 0), font=timeFont),
                sg.Text('', key='-total-time-', size=(8, 0), font=timeFont)
            ],
            [sg.Button('Done')],
        ]),
    ]]

    timeWindow = sg.Window('Normare', timerLayout, finalize=True, font=textFont, grab_anywhere=False)
    timeWindow.bind('<Return>', '-enter-')

    isRunning = hasStarted = False
    deltaTotal = deltaStep = currentOperation = 0
    arr = []
    data = []
    operationType = ''
    numberOperations = 1
    while True:
        eventTime, valuesTime = timeWindow.read(timeout=10)
        if eventTime == sg.WIN_CLOSED or eventTime == 'Done':
            timeWindow.close()
            break
        elif eventTime in ('-enter-', '-set-timer-'):
            if hasStarted:
                arr.append(formatTime(deltaTotal))
            else:
                # arr.append(valuesTime['-operation-name-'])
                arr.append('')
                hasStarted = isRunning = True
                deltaTotal = 0
            deltaStep = 0
            end = time.perf_counter()
            timeWindow['-current-operation-number-'].update(str(currentOperation)+':')
            currentOperation += 1
        elif eventTime == '-undo-timer-':
            arr = []
            isRunning = hasStarted = False
            deltaStep = deltaTotal = currentOperation = 0
            timeWindow['-current-operation-number-'].update(str(currentOperation)+':')
        elif eventTime == '-pause-timer-':
            isRunning = not isRunning
        elif eventTime == '-reset-timer-':
            if len(arr) > 1:
                data.append(arr)
            arr = []
            isRunning = hasStarted = False
            deltaStep = deltaTotal = currentOperation = 0
            timeWindow['-current-operation-number-'].update(str(currentOperation)+':')
        elif eventTime == '-set-continous-':
            if len(data) == 0:
                timeWindow['-set-continous-'].update(button_color=('white', 'green'))
                timeWindow['-set-parallel-' ].update(button_color=('black', 'grey'))
                operationType = 'continous'
            else:
                print("Can't change type now")
        elif eventTime == '-set-parallel-':
            if len(data) == 0:
                timeWindow['-set-parallel-' ].update(button_color=('white', 'green'))
                timeWindow['-set-continous-'].update(button_color=('black', 'grey'))
                operationType = 'parallel'
            else:
                print("Can't change type now")
        elif eventTime == '-set-operation-name-':
            # if operationType == 'parallel':
            try:
# try converting to integer
                # int(data)
                numberOperations = int(valuesTime['-operation-name-'])
            except ValueError:
                print('Not a number')
                numberOperations = 1
            # print(numberOperations)
        tmp = time.perf_counter()
        if isRunning:
            deltaTotal += tmp-end
            deltaStep += tmp-end
        timeWindow['-total-time-'].update(formatTime(deltaTotal))
        timeWindow['-current-time-'].update(formatTime(deltaStep))
        end = tmp
    # print(data)
    return [[operationType, numberOperations], data]

# Main


# Load defaults
defaultDirPath = ''
if os.path.exists('./defaults.txt'):
    defaultDirFile = open('defaults.txt', 'r')
    defaultDirPath = defaultDirFile.read()
    defaultDirFile.close()

filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

# Create the Windows
sg.theme('SystemDefault')
fileSelectorLayout = [[
                sg.Column([
                    [sg.Text('Select location: ')],
                    [sg.InputText(defaultDirPath, key='-folder-', enable_events=True), sg.FolderBrowse()],
                    [sg.Text('Enter File Name: ', key='-title-')],
                    [sg.InputText(filename, enable_events=False, disabled=False, key='-filename-'), sg.Button('Ok', key='-open-timer-')],
                ]),
]]
fileWindow = sg.Window('Creare Fisier Norme', fileSelectorLayout, finalize=True, font=textFont, grab_anywhere=False)
timeWindow = 0

while True:
    event, values = fileWindow.read()
    if event == sg.WIN_CLOSED :
        fileWindow.close()
        break
    elif event == '-filename-':
        filename = values['-filename-']
        # print(filename)
    elif event == '-folder-':
        defaultDirPath = values['-folder-']
    elif event == '-open-timer-':
        filename = values['-filename-']
        data = runTumer()
        print(data)
        if len(data[1]) > 0:
            writeExcelFile(defaultDirPath, filename, data)
        filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        fileWindow['-filename-'].update(filename)

# Update default folder path

defaultDirFile = open('defaults.txt', 'w')
defaultDirFile.write(defaultDirPath)
defaultDirFile.close()