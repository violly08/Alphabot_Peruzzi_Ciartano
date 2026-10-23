import time
from alphabot import AlphaBot

# Parametri regolabili
SPEED = 50          # velocità motori (0-100)
MOVE_TIME = 0.5     # secondi per avanti/indietro
TURN_TIME = 0.3     # secondi per le curve

robot = AlphaBot(speed=SPEED)


def muovi(azione, durata):
    azione()
    time.sleep(durata)
    robot.stop()


def main():
    print("Comandi: w = avanti, s = indietro, a = sinistra, d = destra, q = esci")
    try:
        while True:
            cmd = input("> ").strip().lower()

            if cmd == "w":
                muovi(robot.forward, MOVE_TIME)
            elif cmd == "s":
                muovi(robot.backward, MOVE_TIME)
            elif cmd == "a":
                muovi(robot.left, TURN_TIME)
            elif cmd == "d":
                muovi(robot.right, TURN_TIME)
            elif cmd == "q":
                break
            else:
                print("Comando non valido")
    except KeyboardInterrupt:
        pass
    finally:
        robot.cleanup()
        print("Fine.")


if __name__ == "__main__":
    main()