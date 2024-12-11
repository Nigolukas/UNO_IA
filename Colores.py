import pygame
import random as rd
global UNO
UNO = False
colores=["NEGRO", "AZUL", "VERDE", "ROJA", "AMARILLA"]
baraja=[] #La baraja de cartas sin cojer
monton=[] #El montón en la mesa
pygame.init()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def crearBaraja():
   baraja=[]
   for v in range(0,9):
      for color in colores[1:]:
         for _ in range(2 if v>0 else 1):
            baraja.append({"color":color,"valor":str(v), "robar":0})

   for _ in range(4): # cartas especiales
      baraja.append({"color":"NEGRO", "valor":"+4", "robar":4})
      baraja.append({"color":"NEGRO", "valor":"COMODIN", "robar":0})

   for _ in range(3): # cartas de +2
      for color in colores[1:]:
         baraja.append({"color":color, "valor":"+2", "robar":2})
         baraja.append({"color":color, "valor":"CAMBIO", "robar":0})
         baraja.append({"color":color, "valor":"SALTO", "robar":0})
   rd.shuffle(baraja)
   return baraja

baraja=crearBaraja()
jugadores=[
   {"nombre":"","mano":[], "tipo":"HUMANO", "puntuacion":0},
   {"nombre":"robot1","mano":[], "tipo": "IA", "puntuacion":0},
   {"nombre":"robot2","mano":[], "tipo": "IA", "puntuacion":0},
   {"nombre":"robot3","mano":[], "tipo": "IA", "puntuacion":0}
]
jugadores[0]["nombre"]="Humano"
#reparticion de Adam Smith 
for _ in range(7):
   for jugador in jugadores:
      jugador["mano"].append(baraja[0])
      baraja=baraja[1:]


for jugador in jugadores:
   print("")
   print(jugador["nombre"])
   print ("MANO")
   for carta in jugador["mano"]:
      print(((carta["color"]+" ") if carta["color"]!="NEGRO" else "") +carta["valor"])


monton.append(baraja[0])
baraja=baraja[1:]
if(monton[0]["color"]=="NEGRO"):
   monton[0]["color"]=rd.choice(colores[1:])

def pintarCarta(carta): #no necesaria
   return ((carta["color"]+" ") if carta["color"]!="NEGRO" else "") +carta["valor"] + ("("+str(carta["robar"])+")" if carta["robar"]>0 else "")

def cumpleLasReglas(cartaEscogida,cartaEnMesa):
   if cartaEscogida["color"]=="NEGRO":
      return True
   else:
      return cartaEnMesa["color"]==cartaEscogida["color"] or cartaEnMesa["valor"]==cartaEscogida["valor"]

def mostrarMano(jugador, numeradas=False,cartaMesa=None): #no necesaria
   i=1
   col=0
   cadenaSalida=""
   for carta in jugador["mano"]:
      
      textoCarta=((str(i)+" " if numeradas else ""))
      if cartaMesa!=None and cumpleLasReglas(carta,cartaMesa):
         textoCarta+=bcolors.BOLD+ pintarCarta(carta)+bcolors.ENDC
      else:
         textoCarta+=pintarCarta(carta)
      cadenaSalida+=("\t" if col>0 else "\r\n")+textoCarta.ljust(20," ")
      if(col==3):
         col=0
      else:
         col+=1
      i+=1
   print(cadenaSalida)

def dibujar_recuadro_color(color, x, y):
    pygame.draw.rect(ventana, color, (x, y, 50, 50))
def escogerColor():
    colorEscogido = ""
    repetir = True
    font = pygame.font.Font(None, 36)
    
    while repetir:
        dibujar_recuadro_color(color_amarillo, 200, 100)
        dibujar_recuadro_color(color_verde, 300, 100)
        dibujar_recuadro_color(color_rojo, 400, 100)
        dibujar_recuadro_color(color_azul, 500, 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_4:
                    # Si se presiona una tecla numérica del 1 al 4, elige el color correspondiente
                    colorEscogido = colores[event.key - pygame.K_1 + 1]
                    repetir = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si el clic del mouse está dentro de un recuadro de color
                x, y = event.pos
                if 200 <= x <= 250 and 100 <= y <= 150:
                    colorEscogido = "AMARILLA"
                    repetir = False
                    print("Cambio de color a Amarillo")
                elif 300 <= x <= 350 and 100 <= y <= 150:
                    colorEscogido = "VERDE"
                    repetir = False
                    print("Cambio de color a Verde")
                elif 400 <= x <= 450 and 100 <= y <= 150:
                    colorEscogido = "ROJA"
                    repetir = False
                    print("Cambio de color a Rojo")
                elif 500 <= x <= 550 and 100 <= y <= 150:
                    colorEscogido = "AZUL"
                    repetir = False
                    print("Cambio de color a Azul")
    return colorEscogido


def robar(jugador,numero,baraja):
   for _ in range(numero):
      if len(baraja)>0:
         jugador["mano"].append(baraja[0])
         baraja=baraja[1:]
   return baraja

def controlaRobos(jugador,cartaMesa,baraja):
   if cartaMesa["valor"]=="+4":
      print(bcolors.FAIL +"\t---ROBA 4 Cartas---" + bcolors.ENDC)
      #Tengo que robar 4 cartas
      baraja=robar(jugador,4,baraja)
      cartaMesa["robar"]=0
   elif cartaMesa["valor"]=="+2" and cartaMesa["robar"]>0:
      tengo=False
      for carta in jugador["mano"]:
         tengo=tengo or carta["valor"]=="+2"
      if not tengo:
         print(bcolors.FAIL +"\t---ROBA "+str(cartaMesa["robar"])+" Cartas---" + bcolors.ENDC)
         baraja=robar(jugador, cartaMesa["robar"],baraja)
         cartaMesa["robar"]=0
   return baraja


def escogerCarta(jugador, cartaEnMesa, baraja):
    global UNO
    repetir = True
    seleccionada = None

    while repetir:
        robot1 = jugadores[1]
        robot2 = jugadores[2]
        robot3 = jugadores[3]
        humano = jugadores[0]
        dibujar_carta(color_negro, str(len(robot1["mano"])),20,250,None)
        dibujar_carta(color_negro, str(len(robot2["mano"])),600,10,None)
        dibujar_carta(color_negro, str(len(robot3["mano"])),1150,250,None)
        x_in = ventana.get_width() // 2 - 50*(len(jugador["mano"]))
        carta_en_mesa = monton[-1]
        convertir_a_dibujo_carta(carta_en_mesa,ventana.get_width() // 2 - ancho_carta // 2, ventana.get_height() // 2 - alto_carta // 2)
        #cartasValidas=0
        #for i,carta in enumerate(jugador["mano"]):
            #if cumpleLasReglas(carta,cartaEnMesa):
           #     cartasValidas+=1
          #  elif carta["color"]!="NEGRO":
         #      cartasValidas+=1
        #if cartasValidas==0:
            #if len(baraja)>0:
                
        for carta in jugador["mano"]:
            convertir_a_dibujo_carta(carta,x_in,550)
            x_in=x_in+100
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si el clic del mouse está dentro de un recuadro de color
                x, y = event.pos
                if 700<= x <= 700+ancho_carta and  285 <= y <= 285+alto_carta:
                    baraja = robar(jugador, 1, baraja)
                    anterior = len(jugador["mano"])
                if   len(humano["mano"]) == 2 and 300<= x <= 300 + ancho_carta and  300 <= y <= 300+alto_carta:
                    dibujar_carta(color_verde, "UNO",300,300,None)
                    UNO = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Presionar "R" para robar una carta
                    if len(baraja) > 0:
                        baraja = robar(jugador, 1, baraja)
                    else:
                        print("NO HAY CARTAS PARA ROBAR")

                elif event.key == pygame.K_c:
                    # Presionar "C" para realizar una acción específica
                    return -3, baraja

                elif event.key == pygame.K_s:
                    # Presionar "S" para salir del juego
                    return -1, baraja

                elif pygame.K_1 <= event.key <= pygame.K_9:
                    # Presionar una tecla numérica para seleccionar una carta
                    number = event.key - pygame.K_0
                    if 1 <= number <= len(jugador["mano"]):
                        cartaEscogida = jugador["mano"][number - 1]
                        if cumpleLasReglas(cartaEscogida, cartaEnMesa):
                            jugador["mano"] = (
                                jugador["mano"][: number - 1] + jugador["mano"][number:]
                            )
                            if cartaEscogida["color"] == "NEGRO":
                                cartaEscogida["color"] = escogerColor()
                            repetir = False
                        else:
                            print(bcolors.FAIL + "CARTA NO VALE" + bcolors.ENDC)

        
        pygame.display.flip()

    return cartaEscogida, baraja

def puntuar(carta): # no necesaria
   #{"color":"NEGRO", "valor":"+4", "robar":4}
   if carta["valor"]=="+4":
      return 100
   if carta["valor"]=="+2":
      return 20
   if carta["valor"]=="COMODIN":
      return 20
   if carta["valor"]=="SALTO":
      return 50
   if carta["valor"]=="CAMBIO":
      return 50
   return int(carta["valor"])


def jugarCarta(jugador, cartaEnMesa, baraja): #esto lo hace la IA
   #Pintamos la mano
   repetir=True
   selecioniada=None
   while repetir:
      #mostrarMano(jugador, True) #Lo quitaríamos despues para evitar que los usuario lo vean
      #print("\r\n\r\nCarta en la mesa: ", pintarCarta(monton[-1]))
      print("Tiene "+str(len(jugador["mano"]))+" cartas")
      
      cartasValidas=[]
      cartasColor={}
      for i,carta in enumerate(jugador["mano"]):
         if cumpleLasReglas(carta,cartaEnMesa):
            cartasValidas.append(i)
         if carta["color"]!="NEGRO":
            if carta["color"] in cartasColor:
               cartasColor[carta["color"]]+=1
            else:
               cartasColor[carta["color"]]=1

      # cartas son válidas
      idCartaSeleccionada=-1
      if len(cartasValidas)==0:
         if len(baraja)>0:
            print(bcolors.WARNING+"\tRobo carta"+bcolors.ENDC)
            baraja=robar(jugador,1,baraja)
         else:
            print("NO HAY CARTAS PARA ROBAR")
            #TODO: Definir que pasa cuando ya no hay carta
            return None,baraja
      else:
         #Cogemos la más ventajosa
         for idCarta in cartasValidas:
            if idCartaSeleccionada<0:
               idCartaSeleccionada=idCarta
            else:
               if not jugador["mano"][idCarta]["valor"].isnumeric():
                  idCartaSeleccionada=idCarta
      
         if jugador["mano"][idCartaSeleccionada]["color"]=="NEGRO":
            color=""
            colorNumero=0
            for c in cartasColor:
               if cartasColor[c]>colorNumero:
                  colorNumero=cartasColor[c]
                  color=c
            jugador["mano"][idCartaSeleccionada]["color"]=c
         repetir=False
   cartaEscogida=jugador["mano"][idCartaSeleccionada]
   jugador["mano"]=jugador["mano"][0:int(idCartaSeleccionada)]+jugador["mano"][int(idCartaSeleccionada)+1:]
   return cartaEscogida,baraja




# Definir colores RGB
color_fondo = (247,199,217)
color_rojo = (231, 76, 60)
color_verde = (46, 204, 113)
color_azul = (52, 152, 219)
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_sombra = (144, 114, 145)
color_amarillo = (231, 208, 4)

# Definir tamaño de las cartas
ancho_carta = 100
alto_carta = 150

# Cargar imagen para las cartas
img_cambio_sentido = pygame.image.load("cambio_sentido.png")
img_cambio_sentido = pygame.transform.scale(img_cambio_sentido, (80, 120))  # Ajustar tamaño
img_bloqueo = pygame.image.load("bloqueo.png")
img_bloqueo = pygame.transform.scale(img_bloqueo, (80, 120))  # Ajustar tamaño
img_mas_cuatro= pygame.image.load("cambio_color.png")
img_camio_color= pygame.transform.scale(img_mas_cuatro, (60, 90))  # Ajustar tamaño
img_blanco= pygame.image.load("blanco.png")
img_blanco= pygame.transform.scale(img_blanco, (60, 90))  # Ajustar tamaño
# Crear ventana
ventana = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Ejemplo de Cartas')

# Función para dibujar una carta
def dibujar_carta(color, valor, x, y, especial=None):
    # Dibujar sombra de la carta (rectángulo ligeramente desplazado)
    pygame.draw.rect(ventana, color_sombra, (x + 5, y + 5, ancho_carta, alto_carta), border_radius=10)

    # Dibujar el cuerpo de la carta (rectángulo con esquinas redondeadas)
    pygame.draw.rect(ventana, color, (x, y, ancho_carta, alto_carta), border_radius=10)

    # Dibujar el borde de la carta
    pygame.draw.rect(ventana, color_negro, (x, y, ancho_carta, alto_carta), width=3, border_radius=10)

    # Dibujar la imagen correspondiente a las cartas especiales
    font = pygame.font.Font(None, 36)
    if especial == "cambio_sentido":
        ventana.blit(img_blanco, (x + 19, y + 29))
        ventana.blit(img_cambio_sentido, (x + 10, y + 10))  # Ajustar posición
        
    elif especial=="+2":
        ventana.blit(img_blanco, (x + 19, y + 29))
        texto = font.render(especial, True, color)
        texto_rect = texto.get_rect(center=(x + ancho_carta // 2, y + alto_carta // 2))
        ventana.blit(texto, texto_rect)
    elif especial=="bloqueo":
        ventana.blit(img_blanco, (x + 19, y + 29))
        ventana.blit(img_bloqueo, (x + 10, y + 10))  # Ajustar posición
    elif especial == "+4":
        # Dibujar el texto "+4" en el centro de la carta con fondo negro
        pygame.draw.rect(ventana, color_negro, (x , y, ancho_carta, alto_carta), border_radius=10)  # Fondo negro
        ventana.blit(img_camio_color, (x + 18, y + 29))
        texto = font.render("+4", True, color_blanco)
        texto_rect = texto.get_rect(center=(x + ancho_carta // 2, y + alto_carta // 2))
        ventana.blit(texto, texto_rect)
    elif especial == "cambio color":
        # Dibujar el texto "+4" en el centro de la carta con fondo negro
        pygame.draw.rect(ventana, color_negro, (x , y, ancho_carta, alto_carta), border_radius=10)  # Fondo negro
        ventana.blit(img_camio_color, (x + 19, y + 29))

    else:
        # Dibujar el número en el centro de la carta (texto)
        ventana.blit(img_blanco, (x + 19, y + 29))
        texto = font.render(valor, True, color)
        texto_rect = texto.get_rect(center=(x + ancho_carta // 2, y + alto_carta // 2))
        ventana.blit(texto, texto_rect)

def convertir_a_dibujo_carta(carta,x,y):

    color = color_blanco  # Color predeterminado para la carta (o color por defecto)
    valor = ""  # Valor predeterminado para la carta (o valor por defecto)
    especial = None  # Tipo especial de carta predeterminado (o sin tipo especial)

    # Aquí debes analizar la información de la carta para establecer el color, valor y tipo especial (si corresponde)
    # Utiliza la información de la carta para determinar qué color, valor y tipo especial tiene
    if carta["color"] == "AMARILLA":
        color = color_amarillo
    if carta["color"] == "ROJA":
        color = color_rojo
    if carta["color"] == "VERDE":
        color = color_verde
    if carta["color"] == "AZUL":
        color = color_azul
    if carta["color"] == "NEGRO":
        color = color_negro
        # Manejar las cartas especiales (cambio de color, +4, etc.)
        if carta["valor"] == "+4":
            especial = "+4"
        elif carta["valor"] == "COMODIN":
            especial = "cambio color"
        # Ajusta los valores 'color', 'valor' y 'especial' según corresponda para las cartas negras

    else:
        # Manejar las cartas de colores
        if carta["valor"].isnumeric():
            valor = carta["valor"]
        elif carta["valor"] == "+2":
            especial = "+2"
        elif carta["valor"] == "SALTO":
            especial = "bloqueo"
        elif carta["valor"] == "CAMBIO":
            especial = "cambio_sentido"
        # Ajusta los valores 'color', 'valor' y 'especial' según corresponda para las cartas de colores

    # Llama a la función 'dibujar_carta' con los valores calculados
    dibujar_carta(color, valor, x, y, especial)


# Bucle principal del juego
continuar= True
idJugador=0
direccionJuego=+1
numeroJugadores=len(jugadores)
while continuar:
    jugador = jugadores[idJugador]
    humano = jugadores[0]
    anterior = len(jugador["mano"])
    robot1 = jugadores[1]
    anterior1 = len(robot1["mano"])
    robot2 = jugadores[2]
    anterior2 = len(robot2["mano"])
    robot3 = jugadores[3]
    anterior3 = len(robot3["mano"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuar = False

    ventana.fill(color_fondo)  # Limpiar la pantalla

    # Dibujar cartas de ejemplo en posiciones específicas
    fuente = pygame.font.Font(None, 36)
    color_texto = (0, 0, 0)
    carta_en_mesa = monton[-1]
    convertir_a_dibujo_carta(
        carta_en_mesa, ventana.get_width() // 2 - ancho_carta // 2, ventana.get_height() // 2 - alto_carta // 2
    )
    
    if jugador["tipo"] == "IA":
        dibujar_carta(color_negro, str(len(robot1["mano"])), 20, 250, None)
        dibujar_carta(color_negro, str(len(robot2["mano"])), 600, 10, None)
        dibujar_carta(color_negro, str(len(robot3["mano"])), 1150, 250, None)
        superficie_texto = fuente.render(
            str(jugador["nombre"]) + " tiene " + str(anterior) + " cartas, esta pensando...", True, color_texto
        )
        posicion_texto = ((ventana.get_width() // 2) - 200, 500)
        ventana.blit(superficie_texto, posicion_texto)
        pygame.display.flip()
        x_in = ventana.get_width() // 2 - 50 * (len(jugador["mano"]))
        pygame.time.delay(2000)
    else:
        if len(humano["mano"]) == 2:
            superficie_texto = fuente.render("Avisa que vas a tener UNO!", True, color_texto)
            posicion_texto = ((ventana.get_width() // 2) - 200, 500)
            ventana.blit(superficie_texto, posicion_texto)
        elif len(humano["mano"]) == 1 and UNO == False:
            superficie_texto = fuente.render("No avisaste, que sad", True, color_texto)
            posicion_texto = ((ventana.get_width() // 2) - 200, 500)
            ventana.blit(superficie_texto, posicion_texto)
            baraja = robar(humano, 1, baraja)
        elif len(humano["mano"]) == 1 and UNO == True:
            superficie_texto = fuente.render("Ya vas a ganar!", True, color_texto)
            posicion_texto = ((ventana.get_width() // 2) - 200, 500)
            ventana.blit(superficie_texto, posicion_texto)
        x_in = ventana.get_width() // 2 - 50 * (len(jugador["mano"]))
        for carta in humano["mano"]:
            convertir_a_dibujo_carta(carta, x_in, 550)
            x_in = x_in + 100

    dibujar_carta(color_negro, str(anterior1), 20, 250, None)
    dibujar_carta(color_negro, str(anterior2), 600, 10, None)
    dibujar_carta(color_negro, str(anterior3), 1150, 250, None)
    dibujar_carta(color_negro, "R", 700, 285, None)
    dibujar_carta(color_rojo, "UNO", 300, 300, None)
    pygame.display.flip()  # Actualizar pantalla
    print("\r\nTurno de " + jugador["nombre"] + " - " + str(jugador["puntuacion"]) + " puntos")
    baraja = controlaRobos(jugador, monton[-1], baraja)
    if monton[-1]["valor"] == "SALTO":
        idJugador += direccionJuego
        idJugador = (numeroJugadores + idJugador) if idJugador < 0 else idJugador % numeroJugadores

    if jugador["tipo"] == "IA":
        cartaEscogida, baraja = jugarCarta(jugador, monton[-1], baraja)
        print(bcolors.BOLD + "\tTira " + pintarCarta(cartaEscogida) + bcolors.ENDC)
    else:
        cartaEscogida, baraja = escogerCarta(jugador, monton[-1], baraja)
    if cartaEscogida == -1:
        continuar = False
    else:
        if cartaEscogida is not None:
            jugador["puntuacion"] += puntuar(cartaEscogida)
            cartaEscogida["robar"] += monton[-1]["robar"]
            monton.append(cartaEscogida)
        print("Tine puntuación " + str(jugador["puntuacion"]))
        if len(jugador["mano"]) == 0:
            continuar = False
            print(
                jugador["nombre"]
                + "  GANA LA PARTIDA"
                + (
                    (" Con puntuación de " + str(jugador["puntuacion"]))
                    if jugador["puntuacion"]
                    else " SE ha quedado sin cartas"
                )
            )
            
        if monton[-1]["valor"] == "CAMBIO":
            direccionJuego *= -1
        idJugador += direccionJuego
        idJugador = (numeroJugadores + idJugador) if idJugador < 0 else idJugador % numeroJugadores

superficie_texto = fuente.render(str(jugador["nombre"]) + " gano!", True, color_texto)
posicion_texto = ((ventana.get_width() // 2) - 200, 500)
ventana.blit(superficie_texto, posicion_texto)
pygame.time.delay(10000)
pygame.quit()  


   
