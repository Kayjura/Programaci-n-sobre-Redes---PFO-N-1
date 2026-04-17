#!/usr/bin/env python3
# client.py
# Cliente que se conecta al servidor en localhost:5000 y envía múltiples mensajes.
# Finaliza cuando el usuario escribe "éxito".

import socket
import sys

HOST = '127.0.0.1'
PORT = 5000

def run_client(host=HOST, port=PORT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except ConnectionRefusedError:
        print(f"[ERROR] No se pudo conectar a {host}:{port}. ¿El servidor está corriendo?")
        return
    except Exception as e:
        print(f"[ERROR] Falló la conexión: {e}")
        return

    print(f"[CONECTADO] Conectado a {host}:{port}. Escribí mensajes. Escribe 'éxito' para terminar.")
    try:
        with sock:
            while True:
                try:
                    mensaje = input("> ")
                except EOFError:
                    break
                if not mensaje:
                    continue
                # Enviar mensaje al servidor
                try:
                    sock.sendall((mensaje + "\n").encode('utf-8'))
                except BrokenPipeError:
                    print("[ERROR] Conexión cerrada por el servidor.")
                    break
                # Recibir respuesta (puede llegar en varias partes; leer hasta newline o cierre)
                try:
                    respuesta = sock.recv(4096)
                    if not respuesta:
                        print("[INFO] Servidor cerró la conexión.")
                        break
                    print("Servidor:", respuesta.decode('utf-8').strip())
                except Exception as e:
                    print(f"[ERROR] Al recibir respuesta: {e}")
                    break

                if mensaje.strip().lower() == 'éxito':
                    print("[FIN] Mensaje de terminación enviado. Cerrando cliente.")
                    break
    except KeyboardInterrupt:
        print("\n[INTERRUPCIÓN] Cliente finalizado por usuario.")
    finally:
        try:
            sock.close()
        except:
            pass

if __name__ == '__main__':
    run_client()
