# _*_ coding: utf-8 _*_

import pygame
import math
import os

ORIENTATION_COSTUME_ROTATE = 0
ORIENTATION_COSTUME_FLIP_H   = 1
ORIENTATION_COSTUME_FLIP_V   = 2
ORIENTATION_COSTUME_FIXED  = 3

def angolo(A, B):
    ''' Funzione che calcola il coefficiente angolare della 
        retta che passa per i due punti in input e ne deriva 
        l'angolo di incidenza con l'asse delle ascisse.

        A è il punto in cui sta l'osservatore 
        B è il punto verso cui bisogna guardare.
    '''
    dy = 0.0 + B[1] - A[1]
    dx = B[0]-A[0]
    if dx == 0:
        angolo = 90
        if dy < 0: angolo = angolo + 180     
    else:
        angolo = math.degrees(math.atan(dy / dx))
        if angolo <= 0 and dx < 0: angolo = 180 + angolo
        if angolo >= 0 and dy < 0: angolo = angolo - 180
    return (angolo + 360) % 360


class Attore(pygame.sprite.DirtySprite):
    ''' Uno sprite i cui comportamenti base possono essere 
        programmati dall'esterno
    '''
    
    def __init__(self, *group):
        super(Attore, self) .__init__(*group)
        self.angle = 0
        self.speed = 0
        self.rotation = 0
        self.speed_x = 0
        self.speed_y = 0
        self.center_x = 0
        self.center_y = 0
        self.frame = []
        self.frame_attivo = 0
        self.orientation_mode = 0      
        self.last_orientation = 0


    def costume_da_file(self, image_path):
        image = pygame.image.load(os.path.normpath(image_path)).convert_alpha()
        self.costume(image)
 

   
    def costume(self, image):
        self.frame.append(image)
        if len(self.frame) == 1:
            self.usa_costume(0)            
            self.spostati_a(self.rect.centerx, self.rect.centery)


    def usa_costume(self, indice):
        if len(self.frame) >= indice:
            # prima immagine inserita
            self.base = self.frame[indice]
            self.image = self.base
            self.rect = self.image.get_rect()
            self.frame_attivo = indice


    def costume_successivo(self):
        self.usa_costume((self.frame_attivo + 1) % len(self.frame))  
          

    def spostati_a(self, x, y):
        self.center_x = x
        self.center_y = y
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y


    def posizione(self):
        return (self.center_x, self.center_y)


    def direzione(self, angolo):
        self.angle = angolo % 360


    def ruota(self, degree_per_frame):
        self.rotation = math.radians(degree_per_frame % 360)


    def velocita(self, pixel_per_frame):
        self.speed = pixel_per_frame
        self.update_speed()


    def mostra(self):
        self.visible = True


    def nascondi(self):
        self.visible = False


    def cambia_visibilita(self):
        self.visible = not self.visible


    def guarda_verso(self, point):
        print (isinstance(point, Attore))
        if isinstance(point, Attore):
            point = point.posizione()
        self.angle = angolo(self.posizione(), point)
        self.update_speed()


    def modifica_angolo(self, angolo):
        self.set_angolo(self.angle + 360 + angolo)


    def set_angolo(self, angolo):
        self.angle = angolo % 360
        self.update_speed()


    def update_speed(self):
        if self.speed != 0:
            rad = math.radians(self.angle)
            self.speed_x = math.ceil(self.speed * math.cos(rad))
            self.speed_y = math.ceil(self.speed * math.sin(rad))
        else:
            self.speed_x, self.speed_y = 0, 0
        #print "(", self.speed_x, ", ", self.speed_y, ")[", pixel_per_frame, "]"


    def move(self):
        if self.rotation != 0:
            self.angle += self.rotation
        self.update_speed()
        # calcoliamo la nuova posizione in coordinate cartesiane        
        self.center_x = self.center_x + self.speed_x
        self.center_y = self.center_y + self.speed_y
        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y
        
        
    def orienta_costume(self):
        if self.angle != self.last_orientation:
            self.last_orientation = self.angle + self.rotation
            if self.orientation_mode == ORIENTATION_COSTUME_FLIP_H :
                if not (self.angle > -90 and self.angle < 90):
                   self.image = pygame.transform.flip(self.base, True, False)
            elif self.orientation_mode == ORIENTATION_COSTUME_FIXED:
               self.image = self.base
            else:  
               self.image = pygame.transform.rotate(self.base, -self.last_orientation)
            self.rect = self.image.get_rect()

  
    def update(self):
        self.orienta_costume()
        self.move()
        self.dirty = 1


class Timer (object):
    ''' Un oggetto di tipo timer si usa per posticipare l'uso
        di un metodo di una particolare classe ad un istante
        nel futuro.
    '''


    def __init__ (self, *args):
        super(Timer, self) .__init__(*args)
        self.task = []
    	self.last_event_time = pygame.time.get_ticks()
    

    def add(self, msec, chi, cosa, *come):
        ''' Invoca la funzione tra msec millisecondi 
            a partire dalla chiamata a questa funzione.
        '''
        msec = msec + pygame.time.get_ticks()
        self._insert(msec, chi, cosa, come)


    def add_after(self, msec, chi, cosa, *come):
        ''' Invoca la funzione tra msec millisecondi 
            a partire dalla chiamata posticipata più
            lontana nel futuro.
        '''
        msec = msec + self.last_event_time
        self._insert(msec, chi, cosa, come)


    def add_chain(self, msec, chi, cosa, *come):
        ''' Invoca la funzione tra msec millisecondi 
            a partire dall'istante di invocazione 
            dell'ultimo compito inserito (che non
            è detto che sia quello più lontano nel
            tempo).
        '''
        msec += self.last_added_time
        self._insert(msec, chi, cosa, come)


    def _insert(self, istante, chi, cosa, come):
        ''' Questa funzione si occupa di inserire 
            davvero i compiti in lista d'attesa.
            É una funzione privata e non deve 
            essere chiamata direttamente.
        '''
        self.task.append({
            "quando": istante, 
            "chi":    chi, 
            "cosa":   cosa, 
            "come":   come
        })
        self.last_event_time = max(istante, self.last_event_time)
        self.last_added_time = istante

 
    def esegui(self):
        ora = pygame.time.get_ticks()
        futuri = []
        for compito in self.task:
            if compito ["quando"] <= ora:
                getattr(compito ["chi"], compito ["cosa"])(*compito["come"])
                print ora, compito["quando"], compito ["cosa"]
            else:
                futuri.append(compito)
        self.task = futuri
