from kivy.app import App
from plyer import gps
from kivy.lang import Builder
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

from kivy.clock import Clock
import time

from math import radians, degrees, sin, cos, asin, acos, sqrt

import numpy as np #do szybkiego segregowania listy predkosci wrzuconej do tablicy numpaya


from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([
        Permission.ACCESS_FINE_LOCATION
        # Permission.ACCESS_COARSE_LOCATION
        # Permission.INTERNET
        # Permission.CAMERA
        # Permission.WRITE_EXTERNAL_STORAGE,
        # Permission.READ_EXTERNAL_STORAGE,
        # Permission.INTERNET,
        # Permission.BODY_SENSORS,
        # Permission.BLUETOOTH
    ])
else:
    print("To nie android")

ekran = '''
ScreenManager:
    id: screen_manager
    Screen:
        name: 'gps'

        GridLayout:
            rows:7
            GridLayout:
                cols:2
                size_hint_y: .5
                Button:
                    id: przycisk1
                    text: "GPS"
                    size_hint_y: .5
                    font_size:'20sp'
                    background_color: 0.9, 0.6, 0.3, 1
                    background_normal: ""
                Button:
                    id: przycisk2
                    text: "SPEEDER"
                    size_hint_y: .5
                    font_size:'20sp'
                    background_color: 0.9, 0.6, 0.3, 1
                    background_normal: ""
                    on_release: screen_manager.current = "speeder"
            Label:
                id: szer
                text: 'Szerokość geograficzna'
                font_size:'24sp'
                #color: 0, 0.5, 0.8, 1
                background_color: (0, 0.5, 0.8, 0.9)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                background_normal: ""
                size_hint_x: 1

            Label:
                id: dlu
                text: 'Długość geograficzna'
                font_size:'24sp'
                #color: 1, 1, 1, 1
                background_color: (0, 0.5, 0.8, 1)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                size_hint_x: 1

            Label:
                id: wys
                text: 'Wysokość npm'
                font_size:'24sp'
                #color: 1, 1, 1, 1
                background_color: (0, 0.5, 0.8, 0.9)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                size_hint_x: 1

            Label:
                id: azymut
                text: 'Azymut'
                font_size:'24sp'
                #color: 1, 1, 1, 1
                background_color: (0, 0.5, 0.8, 1)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                size_hint_x: 1

            Label:
                id: predkosc
                text: 'Prędkość'
                font_size:'24sp'
                #color: 1, 1, 1, 1
                background_color: (0, 0.5, 0.8, 0.9)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                size_hint_x: 1


            Button:
                id: przycisk
                text: "Sprawdź"
                size_hint_y: .7
                font_size:'24sp'
                background_color: 0.9, 0.6, 0.3, 1
                background_normal: ""
                #on_press: app.pokaz()
                on_press: app.show_must_go_on()

    Screen:
        name: 'speeder'
        GridLayout:
            rows:7
            GridLayout:
                cols:2
                size_hint_y: .4
                Button:
                    id: przycisk_gps
                    text: "GPS"
                    size_hint_y: .5
                    font_size:'20sp'
                    background_color: 0.9, 0.6, 0.3, 1
                    background_normal: ""
                    on_release: screen_manager.current = "gps"
                Button:
                    id: przycisk_speeder
                    text: "SPEEDER"
                    size_hint_y: .5
                    font_size:'20sp'
                    background_color: 0.9, 0.6, 0.3, 1
                    background_normal: ""
                    on_release: screen_manager.current = "speeder"
            Label:
                id: time
                text: 'Czas'
                font_size:'24sp'
                #color: 0, 0.5, 0.8, 1
                background_color: (0, 0.5, 0.8, 0.9)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                background_normal: ""
                size_hint_x: 1
            Label:
                id: dystans
                text: 'Dystans'
                font_size:'24sp'
                #color: 0, 0.5, 0.8, 1
                background_color: (0, 0.5, 0.8, 1)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                background_normal: ""
                size_hint_x: 1
            Label:
                id: predkosc_sr
                text: 'Prędkość średnia'
                font_size:'24sp'
                #color: 0, 0.5, 0.8, 1
                background_color: (0, 0.5, 0.8, 0.9)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                background_normal: ""
                size_hint_x: 1
            Label:
                id: predkosc_max
                text: 'Prędkość maksymalna'
                font_size:'24sp'
                #color: 0, 0.5, 0.8, 1
                background_color: (0, 0.5, 0.8, 1)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
                background_normal: ""
                size_hint_x: 1

            GridLayout:
                cols:2
                size_hint_y: .55
                Button:
                    id: przycisk_reset
                    text: "RESET"
                    size_hint_y: .15
                    size_hint_x: 1
                    font_size:'24sp'
                    background_color: 0.9, 0.6, 0.3, 1
                    background_normal: ""
                    on_press: app.reset()

                Button:
                    id: stoper
                    text: "START"
                    size_hint_y: .15
                    size_hint_x: 1
                    font_size:'24sp'
                    background_color: 0.9, 0.6, 0.3, 1
                    background_normal: ""
                    on_press: app.stoper()
'''


class GPSApp(App):

    def on_start(self):
        gps.configure(on_location=self.on_gps_location)
        gps.start()

    def on_gps_location(self, **kwargs):
        self.szerokosc = kwargs['lat']
        self.dlugosc = kwargs['lon']
        self.wysokosc = kwargs['altitude']
        self.azymut = kwargs['bearing']
        self.predkosc = kwargs['speed']
        print(kwargs)

    def build(self):
        self.szerokosc = 0.0
        self.dlugosc = 0.0
        self.wysokosc = 0
        self.azymut = 0.0
        self.predkosc = 0.0

        self.licznik = 0

        self.licznik2 = 0
        self.sec = 0
        self.min = 0
        self.hours = 0
        self.time_lapsed = 0

        self.dyst = 0
        self.coords_1 = [52.2296756, 21.0122287] #przykladowa lokalizacja punktu A
        self.coords_2 = [52.406374, 16.9251681] #przykladowa lokalizacja punktu B
        self.lista_predkosci = []


        return Builder.load_string(ekran)

    def show_must_go_on(self):
        wskaznik_przycisk = self.root.ids.przycisk
        if self.licznik == 0:
            self.licznik = 1
            print("czytanie rozpoczete")
            wskaznik_przycisk.background_color = 'red'
            Clock.schedule_interval(self.pokaz, 1.0 / 10.0)  # co 1/10 sek pokaz wynik
        else:
            self.licznik = 0
            print("czytanie zakonczone")
            wskaznik_przycisk.background_color = (0.9, 0.6, 0.3, 1)
            Clock.unschedule(self.pokaz)

    def pokaz(self, *args):
        wskaznik_szer = self.root.ids.szer
        wskaznik_dlu = self.root.ids.dlu
        wskaznik_wys = self.root.ids.wys
        wskaznik_azy = self.root.ids.azymut
        wskaznik_pred = self.root.ids.predkosc
        tekst = "S: {lat}".format(lat=self.szerokosc)
        tekst2 = "D: {lon}".format(lon=self.dlugosc)
        tekst3 = "W npm: {wys}".format(wys=self.wysokosc)
        tekst4 = "Azymut: {wys}".format(wys=self.azymut)
        tekst5 = "Prędkość: {pred}".format(pred=self.predkosc * 3.6) # *3.6 zamiana m/sek na km/h
        wskaznik_szer.text = tekst
        wskaznik_dlu.text = tekst2
        wskaznik_wys.text = tekst3
        wskaznik_azy.text = tekst4
        wskaznik_pred.text = tekst5





#---------------------------stoper SPEEDER
    def stoper(self):
        wskaznik_stoper = self.root.ids.stoper
        if self.licznik2 == 0:
            self.licznik2 = 1
            print("stoper wlaczony")
            wskaznik_stoper.background_color = 'red'
            wskaznik_stoper.text = 'STOP'
            self.poczatek()
        else:
            self.licznik2 = 0
            print("stoper wylaczony")
            wskaznik_stoper.background_color = (0.9, 0.6, 0.3, 1)
            wskaznik_stoper.text = 'START'
            self.koniec()

    def pokaz_czas(self):
        self.sec = self.time_lapsed
        self.mins = self.sec // 60
        self.hours = self.mins // 60
        wskaznik_czas = self.root.ids.time
        wskaznik_czas.text = 'Time: {0}:{1}:{2}'.format(int(self.hours),int(self.mins),int(self.sec))


    def poczatek(self):
        self.lista_predkosci.clear() #czysci liste predkosci
        self.start_time = time.time()
        self.punkt_A_lat = self.szerokosc #wspolrzedne punktu startu
        self.punkt_A_lon = self.dlugosc
        Clock.schedule_interval(self.uplyw, 1.0 / 10.0)

    def uplyw(self,x):
        self.end_time = time.time()
        self.time_lapsed = self.end_time - self.start_time
        self.pokaz_czas()
        self.lista_predkosci.append(self.predkosc * 3.6)  # dopisuj predkosc w km do listy

    def koniec(self):
        Clock.unschedule(self.uplyw)
        self.punkt_B_lat = self.szerokosc  # wspolrzedne punktu konca
        self.punkt_B_lon = self.dlugosc
        self.dystans()
        self.predkosc_MAX()

    def reset(self):
        Clock.unschedule(self.uplyw)
        self.lista_predkosci.clear()  # czysci liste predkosci
        wskaznik_stoper = self.root.ids.stoper
        wskaznik_stoper.background_color = (0.9, 0.6, 0.3, 1)
        wskaznik_stoper.text = 'START'
        wskaznik_czas = self.root.ids.time
        wskaznik_czas.text = 'Time: 0:0:0'
        wskaznik_dyst = self.root.ids.dystans
        wskaznik_dyst.text = "Dystans"
        wskaznik_pred = self.root.ids.predkosc_sr
        wskaznik_pred.text = "Prędkość średnia"
        wskaznik_pred_max = self.root.ids.predkosc_max
        wskaznik_pred_max.text = "Prędkość maksymalna"
        print("stoper wylaczony")
        self.licznik2 = 0

    #----------------------dystans
    def dystans(self):
        #tylko do testow:
        #self.punkt_A_lon = self.coords_1[1]
        #self.punkt_A_lat = self.coords_1[0]
        #self.punkt_B_lon = self.coords_2[1]
        #self.punkt_B_lat = self. coords_2[0]

        #formula Great Circle, ziemia jako kula
        self.punkt_A_lon, self.punkt_A_lat, self.punkt_B_lon, self.punkt_B_lat = map(radians, [self.punkt_A_lon,self.punkt_A_lat,self.punkt_B_lon,self.punkt_B_lat])
        self.dyst = 6371 * (acos(sin(self.punkt_A_lat) * sin(self.punkt_B_lat) + cos(self.punkt_A_lat) * cos(self.punkt_B_lat) * cos(self.punkt_A_lon - self.punkt_B_lon)))
        print(self.dyst)
        tekst = "Dystans: {dyst} km".format(dyst=round(self.dyst,3)) #zaokraglam do 3 miejsca po przecinku 1km,100m, 1m
        wskaznik_dyst = self.root.ids.dystans
        wskaznik_dyst.text = str(tekst)
        
        self.predkosc_SR()

    #---------------------Predkosc srednia
    def predkosc_SR(self):
        czas_w_godz = self.sec / 3600
        predkosc = self.dyst / czas_w_godz
        wskaznik_pred = self.root.ids.predkosc_sr
        tekst2 = "Prędkość średnia: {sr} km/h".format(sr=round(predkosc,1))
        wskaznik_pred.text = str(tekst2)

    #-------------------Predkosc maksymalna
    def predkosc_MAX(self):
        #self.lista_predkosci = [3,8,2,10,4,5] #do testow - dziala
        tablica_predkosci = np.array(self.lista_predkosci) #wrzucam liste do tablicy numpaya
        tablica_predkosci_sorted = np.sort(tablica_predkosci) #sortuj
        pred_max = tablica_predkosci_sorted[-1] #ostatni element posortowanych predkosci czyli maks
        wskaznik_pred_max = self.root.ids.predkosc_max
        tekst_n = "Prędkość maksymalna: {max} km/h".format(max=round(pred_max,1))
        wskaznik_pred_max.text = str(tekst_n)




GPSApp().run()
