import requests
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import webbrowser


def get_json(url):
    data = requests.get(url)

    data = data.json()

    return data

def json_to_string(data):
    results = []
    urls = []
    for f in range(len(data['features'])):


        properties = data['features'][f]['properties']

        place = str(properties['place'])
        mag = str(properties['mag'])
        tsunami = properties['tsunami']

        if tsunami == 1:
            tsunami_chance = "yes"
        else:
            tsunami_chance = "No"

        urls.append(properties['url'])

        results.append([f'{place:<}', mag, tsunami_chance])

    return results, urls


def get_past_day():
    data = get_json('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_day.geojson')

    text, urls = json_to_string(data)

    return text, urls


def get_past_week():
    data = get_json('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson')

    text, urls = json_to_string(data)

    return text, urls

def get_past_month():
    data = get_json('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson')

    text, urls = json_to_string(data)

    return text, urls





if __name__ == '__main__':

    toprow = [f'{"place":50}', 'mag.', 'tsunami chance']

    # sg.theme('LightBlue')

    font = ('Ariel', 15)

    datalist = [
        'Significant: past day',
        'Significant: past 7 days',
        'Significant: past month'
    ]

    option_column = [
        [sg.Text('Please select what data you want to see')],
        [sg.DropDown(datalist, key='-DATALIST-')],
        [sg.Button('Ok', key = '-GETDATA-')]
    ]

    results_column = [
        [sg.Text('Results:')],
        [sg.Table(values = [], headings=toprow, key = '-DATA-OUTPUT-',
                  justification='lcc', enable_events=True,
                  display_row_numbers=False,
                  selected_row_colors='white on black')],
        [sg.Button('Go to details', key='-OPEN-BROWSER-')],
        [sg.Canvas(key='-PLOT-')]
    ]

    layout = [
        [
        sg.Column(option_column),
        sg.VSeparator(),
        sg.Column(results_column)
        ]
    ]

    window = sg.Window("Earthquake data", layout, font = font, resizable=True,
                       finalize=True)


    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'EXIT':
            break

        elif event == '-GETDATA-':
            if values['-DATALIST-'] == 'Significant: past day':
                text, urls = get_past_day()
            elif values['-DATALIST-'] == 'Significant: past 7 days':
                text, urls = get_past_week()
            elif values['-DATALIST-'] == 'Significant: past month':
                text, urls = get_past_month()

            window['-DATA-OUTPUT-'].update(text)

        elif event == '-DATA-OUTPUT-':
            try:
                url = urls[values['-DATA-OUTPUT-'][0]]
            except:
                continue

        elif event == '-OPEN-BROWSER-':
            try:
                webbrowser.open(url)
            except:
                sg.popup('Must click event first', font = font)


    window.close()

