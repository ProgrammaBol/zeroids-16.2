# _*_ coding: utf-8 _*_

import pygame


class Timer (object):
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
                #print ora, compito["quando"], compito ["cosa"]
            else:
                futuri.append(compito)
        self.task = futuri


        
