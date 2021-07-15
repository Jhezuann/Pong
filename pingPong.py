import pygame,sys
from pygame.locals import *
import random

#Marcador
pygame.font.init()

#ventana
ALTURA = 500
ANCHO = 800

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (80,200,120)
ROJO = (250,0,0)

raiz = pygame.display.set_mode((ANCHO, ALTURA))
raiz.fill(NEGRO)
icono = pygame.image.load("logo.png")
pygame.display.set_icon(icono)
pygame.display.set_caption("Ping Pong")


#bloquesDeJugadores
class Bloques():
	def __init__(self,x,y,ancho,altura,color):
		self.x = x
		self.y = y
		self.ancho = ancho
		self.altura = altura
		self.color = color
		self.rect = (x, y, ancho, altura)
		self.movimientoDeVelocidad = 6

	#dibujo de los bloques
	def dibujar(self, ventana):
		pygame.draw.rect(ventana, self.color, self.rect)


	#mteclas para que los bloques se muevan
	def movimiento(self, bloque, superior, inferior):
		teclas = pygame.key.get_pressed()
		if bloque == 2:
			if teclas[pygame.K_UP]:
				self.y -= self.movimientoDeVelocidad
				if self.y <= superior:
					self.y += self.movimientoDeVelocidad

			if teclas[pygame.K_DOWN]:
				self.y += self.movimientoDeVelocidad
				if self.y + self.altura >= inferior:
					self.y -= self.movimientoDeVelocidad
		if bloque == 1:
			if teclas[pygame.K_w]:
				self.y -= self.movimientoDeVelocidad
				if self.y <= superior:
					self.y += self.movimientoDeVelocidad

			if teclas[pygame.K_s]:
				self.y += self.movimientoDeVelocidad
				if self.y + self.altura >= inferior:
					self.y -= self.movimientoDeVelocidad

		self.update()

	def update(self):
		self.rect = (self.x, self.y, self.ancho, self.altura)

#bola del ping pong
class Bola():
	def __init__(self, x, y, radio, color):
		self.x = x
		self.initx = x
		self.y = y
		self.inity = y
		self.radio = radio
		self.color = color
		self.centro = (x, y)
		self.movx = 8 * random.choice([-1,1])
		self.movy = 8 * random.choice([-1,1])
		self.golpear1 = False
		self.golpear2 = False

	#dibujo de la bola
	def draw(self, ventana):
		pygame.draw.circle(ventana, self.color, self.centro, self.radio)

	#movimiento de la bola
	def move(self, superior, inferior, izq, der, bloque_1, bloque_2):
		self.x += self.movx
		self.y += self.movy

		if self.y - self.radio <= superior:
			self.movy *= -1

		if self.y + self.radio >= inferior:
			self.movy *= -1

		if self.x - self.radio <= izq:
			self.x = self.initx
			self.y = self.inity
			self.resetear()
			self.movx *= -1
			return 1

		if self.x + self.radio >= der:
			self.x = self.initx
			self.y = self.inity
			self.resetear()
			self.movx *= -1
			return 2

		if bloque_2.x + bloque_2.ancho >= self.x + self.radio >= bloque_2.x:
			if bloque_2.y + bloque_2.altura >= self.y + self.radio >= bloque_2.y:
				if not self.golpear2:
					self.movx *= -1
					self.golpear2 = True
					self.golpear1 = False

		if bloque_1.x <= self.x - self.radio <= bloque_1.x + bloque_1.ancho:
			if bloque_1.y + bloque_1.altura >= self.y + self.radio >= bloque_1.y:
				if not self.golpear1:
					self.movx *= -1
					self.golpear1 = True
					self.golpear2 = False


		self.update()

	def update(self):
		self.centro = (self.x, self.y)

	def resetear(self):
		self.golpear2 = False
		self.golpear1 = False


#funciones
def ganador(ventana, jugador):
	fuente = pygame.font.SysFont("Arial", 100, True)
	text = "Gano El Jugador " + str(jugador) + "!"
	escribir = fuente.render(text, 1, ROJO)
	ventana.blit(escribir, (ANCHO/2-escribir.get_width/2, ALTURA/2-escribir.get_height))
	pygame.display.update()

def dibujarVentanaDeMarcador(ventana, puntaje1, puntaje2):
	fuente = pygame.font.SysFont("Arial", 40, True)
	text = "Jugador 2: " + str(puntaje1) + "           Jugador 1: " + str(puntaje2)
	escribir = fuente.render(text, 1, BLANCO)
	ventana.blit(escribir, (ANCHO/2-escribir.get_width()/2, 20))

bordeArriba = pygame.draw.rect(raiz, (255,255,255), (50,50,50,60))

def ventana(ventana, bloque_1, bloque_2,linea_1,linea_2,linea_3, bola, puntaje1, puntaje2):
	ventana.fill(VERDE)
	bloque_1.dibujar(ventana)
	bloque_2.dibujar(ventana)
	linea_1.dibujar(ventana)
	linea_2.dibujar(ventana)
	linea_3.dibujar(ventana)
	bola.draw(ventana)
	dibujarVentanaDeMarcador(ventana, puntaje1, puntaje2)

def main():
	puntaje1 = 0
	puntaje2 = 0
	reloj = pygame.time.Clock()

	#objetos
	bloque_1 = Bloques(ANCHO/30, ALTURA/2-65, ANCHO/40, 140, BLANCO)
	bloque_2 = Bloques(ANCHO-(ANCHO/30+ANCHO/40), ALTURA/2-65, ANCHO/40, 140, BLANCO)
	linea_1 = Bloques(ANCHO-402, ALTURA-2-500, ANCHO/400, 500, BLANCO)
	linea_2 = Bloques(ANCHO/1000, ALTURA-2-2, ANCHO-0, 500, BLANCO)
	linea_3 = Bloques(ANCHO-800, ALTURA/2-746, ANCHO/1, 500, BLANCO)
	bola = Bola(int(round(ANCHO/2)), int(round(ALTURA/2)), int(round(ANCHO/80)), BLANCO)

	bandera = True
	while bandera:
		pygame.time.delay(10)
		reloj.tick(220) #FPS
		for evento in pygame.event.get():
			if evento.type == QUIT:
				bandera = False
				pygame.quit()

		bloque_1.movimiento(1, 0, ALTURA)
		bloque_2.movimiento(2, 0, ALTURA)
		punto = bola.move(0, ALTURA, 0, ANCHO, bloque_1, bloque_2)

		if punto == 1:
			puntaje1 += 1
		elif punto == 2:
			puntaje2 += 1 

		bola.update()


		ventana(raiz, bloque_1,bloque_2,linea_1,linea_2,linea_3,bola,puntaje1,puntaje2)

		if puntaje1 == 10:
			ganador(win, 1)
			pygame.time.delay(5000)
			bandera = False
			pygame.quit()
		elif puntaje2 == 10:
			ganador(win, 2)
			pygame.time.delay(5000)
			bandera = False
			pygame.quit()


		pygame.display.update()


if __name__ == '__main__':
	main()