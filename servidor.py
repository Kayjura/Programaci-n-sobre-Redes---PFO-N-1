#!/usr/bin/env python3
# server.py
# Servidor multihilo que escucha en localhost:5000, guarda mensajes en SQLite y responde al cliente.

import socket
import threading
import sqlite3
import datetime
import sys
import traceback

HOST = '127.0.0.1'  # Configuración del socket TCP/IP: localhost
PORT = 5000         # Puerto a escuchar

DB_FILE = 'mensajes.db'  # Archivo de la base de datos SQLite

# Inicializar la base de datos: crea la tabla si no existe.
def init_db(db_file=DB_FILE):
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn
    except Exception as e:
        print(f"[ERROR DB] No se pudo inicializar la base de datos: {e}")
        raise

# Guarda un mensaje en la DB. Esta función es segura para usar desde múltiples hilos
# si se maneja la conexión/lock apropiadamente. Usamos la misma conexión con bloqueo de hilo simple.
db_lock = threading.Lock()
def guardar_mensaje(conn, contenido, ip_cliente):
    # Usar timestamp timezone-aware en UTC (evita DeprecationWarning de utcnow)
    fecha = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with db_lock:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)',
                (contenido, fecha, ip_cliente)
            )
            conn.commit()
            return fecha
    except Exception as e:
        print(f"[ERROR DB] No se pudo guardar el mensaje: {e}")
        raise

# Maneja una conexión cliente en un hilo separado.
def manejar_cliente(conn_sock, addr, db_conn):
    ip_cliente = addr[0]
    print(f"[CONEXIÓN] Cliente conectado desde {ip_cliente}:{addr[1]}")
    try:
        with conn_sock:
            # Recibimos hasta que el cliente cierre la conexión
            while True:
                data = conn_sock.recv(4096)
                if not data:
                    break  # cliente desconectó
                try:
                    mensaje = data.decode('utf-8').strip()
                except UnicodeDecodeError:
                    mensaje = ''
                if mensaje == '':
                    # Ignorar mensajes vacíos
                    continue
                # Guardar en DB
                try:
                    timestamp = guardar_mensaje(db_conn, mensaje, ip_cliente)
                except Exception:
                    # Informar error al cliente si fallo la DB
                    err_msg = "ERROR: no se pudo guardar el mensaje en la base de datos.\n"
                    conn_sock.sendall(err_msg.encode('utf-8'))
                    continue
                # Enviar confirmación con timestamp
                respuesta = f"Mensaje recibido: {timestamp}\n"
                conn_sock.sendall(respuesta.encode('utf-8'))
                print(f"[RECIBIDO] {ip_cliente}: {mensaje} -> {timestamp}")
    except Exception as e:
        print(f"[ERROR] Excepción en manejar_cliente: {e}")
        traceback.print_exc()
    finally:
        print(f"[CERRADO] Conexión con {ip_cliente} finalizada.")

# Inicializa el socket y comienza a aceptar conexiones (hilos por cliente).
def iniciar_servidor(host=HOST, port=PORT):
    # Inicializar DB primero
    try:
        db_conn = init_db()
    except Exception:
        print("[FATAL] No se puede continuar sin DB. Saliendo.")
        sys.exit(1)

    # Crear socket TCP
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar el puerto inmediatamente después de reiniciar el servidor
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_sock.bind((host, port))
        server_sock.listen(5)
        print(f"[INICIO] Servidor escuchando en {host}:{port}")
    except OSError as e:
        print(f"[ERROR] No se pudo bindear el socket en {host}:{port}: {e}")
        server_sock.close()
        sys.exit(1)

    try:
        while True:
            try:
                client_sock, addr = server_sock.accept()
            except KeyboardInterrupt:
                print("\n[STOP] Interrupción por teclado. Cerrando servidor.")
                break
            except Exception as e:
                print(f"[ERROR] Al aceptar conexión: {e}")
                continue

            # Lanzar un hilo para manejar la conexión del cliente
            t = threading.Thread(target=manejar_cliente, args=(client_sock, addr, db_conn), daemon=True)
            t.start()
    finally:
        server_sock.close()
        try:
            db_conn.close()
        except:
            pass
        print("[FIN] Servidor detenido.")

if __name__ == '__main__':
    iniciar_servidor()
