

import tkinter as tk
from tkinter import messagebox, simpledialog
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
# Google API imports
import os
import datetime
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

usuarios = {
    'persona1': {'password': '123456', 'rol': 'admin'},
    'persona2': {'password': '123456', 'rol': 'usuario'}
}

class AsesoriaApp:
    chatbot = None
    chatbot_ready = False
    def __init__(self, root):
        self.root = root
        self.root.title("Asesoría Legal Virtual")
        self.root.geometry("500x600")
        self.root.configure(bg="#102542")
        self.usuario = None
        self.rol = None
        self.logo_img = None
        self.google_email = None
        if not AsesoriaApp.chatbot_ready:
            AsesoriaApp.chatbot = ChatBot(
                'LegalBot',
                logic_adapters=[
                    'chatterbot.logic.BestMatch',
                    'chatterbot.logic.MathematicalEvaluation'
                ],
                read_only=True
            )
            trainer = ChatterBotCorpusTrainer(AsesoriaApp.chatbot)
            trainer.train('chatterbot.corpus.spanish')
            AsesoriaApp.chatbot_ready = True
        self.welcome_screen()

    def welcome_screen(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#102542")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        try:
            from PIL import Image, ImageTk
            logo = Image.open("logo.png")
            logo = logo.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(frame, image=self.logo_img, bg="#102542").pack(pady=10)
        except Exception:
            tk.Label(frame, text="Asesoría Legal Virtual", font=("Arial", 18, "bold"), bg="#102542", fg="white").pack(pady=10)
        tk.Label(frame, text="Bienvenido a la plataforma de asesoría legal virtual", font=("Arial", 12), bg="#102542", fg="white").pack(pady=5)
        tk.Button(frame, text="Iniciar con usuario local", command=self.login_screen, width=25, height=2, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(frame, text="Iniciar sesión con Google", command=self.login_google, width=25, height=2, bg="#4285F4", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    def login_google(self):
        SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        if not os.path.exists('credentials.json'):
            messagebox.showerror("Google API", "No se encontró el archivo credentials.json. Descárgalo desde Google Cloud Console y colócalo en la carpeta del proyecto.")
            return
        creds = None
        if os.path.exists('token_google.pickle'):
            with open('token_google.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    messagebox.showerror("Google API", f"Error de autenticación: {e}")
                    return
            with open('token_google.pickle', 'wb') as token:
                pickle.dump(creds, token)
        try:
            from googleapiclient.discovery import build
            oauth2_service = build('oauth2', 'v2', credentials=creds)
            user_info = oauth2_service.userinfo().get().execute()
            self.google_email = user_info.get('email')
            self.usuario = user_info.get('name', self.google_email)
            self.rol = 'usuario'
            messagebox.showinfo("Google", f"Sesión iniciada como {self.usuario}")
            self.menu_inicio()
        except Exception as e:
            messagebox.showerror("Google API", f"No se pudo obtener información del usuario: {e}")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear()
        if self.logo_img:
            tk.Label(self.root, image=self.logo_img).pack(pady=10)
        else:
            tk.Label(self.root, text="Asesoría Legal Virtual", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="Usuario:").pack()
        user_entry = tk.Entry(self.root)
        user_entry.pack()
        tk.Label(self.root, text="Contraseña:").pack()
        pwd_entry = tk.Entry(self.root, show="*")
        pwd_entry.pack()
        def try_login():
            user = user_entry.get()
            pwd = pwd_entry.get()
            if user in usuarios and usuarios[user]['password'] == pwd:
                self.usuario = user
                self.rol = usuarios[user]['rol']
                messagebox.showinfo("Login", f"Bienvenido, {user} ({self.rol})")
                self.menu_inicio()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        tk.Button(self.root, text="Entrar", command=try_login, bg="#2196F3", fg="white").pack(pady=10)

    def menu_inicio(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#102542")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        if self.logo_img:
            tk.Label(frame, image=self.logo_img, bg="#102542").pack(pady=10)
        tk.Label(frame, text=f"Bienvenido {self.usuario} ({self.rol})", font=("Arial", 18, "bold"), bg="#102542", fg="white").pack(pady=10)
        btn_style = {"width": 28, "height": 2, "font": ("Arial", 13, "bold")}
        tk.Button(frame, text="Ir al menú principal", command=self.menu_principal, bg="#4CAF50", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Cambiar contraseña", command=self.cambiar_contrasena, bg="#2196F3", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Ver información de cuenta", command=self.info_cuenta, bg="#607D8B", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Cerrar sesión", command=self.login_screen, bg="#f44336", fg="white", **btn_style).pack(pady=8)

    def menu_principal(self):
        self.clear()
        tk.Label(self.root, text=f"Menú principal - {self.usuario} ({self.rol})").pack(pady=5)
        frame = tk.Frame(self.root, bg="#102542")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text=f"Menú principal - {self.usuario} ({self.rol})", font=("Arial", 18, "bold"), bg="#102542", fg="white").pack(pady=10)
        btn_style = {"width": 28, "height": 2, "font": ("Arial", 13, "bold")}
        tk.Button(frame, text="Consultar tipo de asesoría", command=self.consultar_asesoria, bg="#1976D2", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Agendar cita", command=self.agendar_cita, bg="#388E3C", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Bot de charla", command=self.bot_charla, bg="#512DA8", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Foro", command=self.foro, bg="#0097A7", fg="white", **btn_style).pack(pady=8)
        if self.rol == 'admin':
            tk.Button(frame, text="Ver mensajes del foro", command=self.ver_foro, bg="#FFA000", fg="white", **btn_style).pack(pady=8)
        else:
            tk.Button(frame, text="Cargar documento", command=self.cargar_documento, bg="#C2185B", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Mensajería asesoría", command=self.mensajeria, bg="#455A64", fg="white", **btn_style).pack(pady=8)
        tk.Button(frame, text="Salir al login", command=self.login_screen, bg="#f44336", fg="white", **btn_style).pack(pady=8)

    def consultar_asesoria(self):
        tipos = {1: "Laboral", 2: "Civil", 3: "Penal", 4: "Comercial"}
        seleccion = simpledialog.askinteger("Tipo de asesoría", "1. Laboral\n2. Civil\n3. Penal\n4. Comercial\n\nSelecciona un número:")
        if seleccion in tipos:
            messagebox.showinfo("Asesoría", f"Has elegido asesoría en: {tipos[seleccion]}")
        else:
            messagebox.showwarning("Asesoría", "Opción no válida.")

    def agendar_cita(self):
        nombre = simpledialog.askstring("Cita", "Tu nombre completo:")
        fecha = simpledialog.askstring("Cita", "Fecha deseada (dd/mm/aaaa):")
        hora = simpledialog.askstring("Cita", "Hora de inicio (formato 24h, ej: 10:00 a 19:00):")
        tipo = simpledialog.askstring("Cita", "Tipo de asesoría (Laboral, Civil, etc.):")
        email = simpledialog.askstring("Cita", "Correo electrónico para confirmación:")
        if not (nombre and fecha and hora and tipo and email):
            messagebox.showwarning("Cita", "Todos los campos son obligatorios.")
            return
        # Validar hora
        try:
            hora_dt = datetime.datetime.strptime(hora, '%H:%M')
            if not (10 <= hora_dt.hour < 19 or (hora_dt.hour == 19 and hora_dt.minute == 0)):
                messagebox.showerror("Cita", "La hora debe estar entre 10:00 y 19:00.")
                return
        except Exception:
            messagebox.showerror("Cita", "Formato de hora incorrecto. Usa HH:MM en 24h.")
            return
        # Google API scopes
        SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/gmail.send']
        creds = None
        if not os.path.exists('credentials.json'):
            messagebox.showerror("Google API", "No se encontró el archivo credentials.json. Descárgalo desde Google Cloud Console y colócalo en la carpeta del proyecto.")
            return
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    messagebox.showerror("Google API", f"Error de autenticación: {e}")
                    return
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # Crear evento en Google Calendar
        try:
            service = build('calendar', 'v3', credentials=creds)
            # Convertir fecha y hora a formato RFC3339
            try:
                fecha_dt = datetime.datetime.strptime(fecha, '%d/%m/%Y')
                start_dt = fecha_dt.replace(hour=hora_dt.hour, minute=hora_dt.minute)
                end_dt = start_dt + datetime.timedelta(hours=1)
            except Exception:
                messagebox.showerror("Cita", "Formato de fecha u hora incorrecto.")
                return
    def check_internet(self):
        import socket
        try:
            # Intenta conectarse a Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except Exception:
            return False
            event = {
                'summary': f'Cita de asesoría: {nombre}',
                'description': f'Tipo: {tipo}\nNombre: {nombre}\nEmail: {email}',
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Santiago'},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Santiago'},
                'attendees': [{'email': email}],
            }
            event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
            link = event.get('htmlLink', '')
        except Exception as e:
            messagebox.showerror("Cita", f"Error al crear evento en Google Calendar: {e}")
            return
        # Enviar correo de confirmación
        try:
            gmail_service = build('gmail', 'v1', credentials=creds)
            subject = "Confirmación de cita de asesoría legal"
            body = f"Hola {nombre},\n\nTu cita de asesoría ({tipo}) ha sido agendada para el {fecha} a las {hora} horas.\n\nPuedes ver el evento aquí: {link}\n\nGracias por usar la plataforma."
            message = MIMEText(body)
            message['to'] = email
            message['from'] = 'me'
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            gmail_service.users().messages().send(userId='me', body={'raw': raw}).execute()
        except Exception as e:
            messagebox.showwarning("Cita", f"Evento creado, pero no se pudo enviar el correo: {e}")
            return
        # Registrar la cita en Google Sheets (guardar el ID localmente para no pedirlo cada vez)
        try:
            import gspread
            from google.auth.transport.requests import Request
            SHEET_ID = None
            SHEET_ID_PATH = 'sheet_id.txt'
            if os.path.exists(SHEET_ID_PATH):
                with open(SHEET_ID_PATH, 'r', encoding='utf-8') as f:
                    SHEET_ID = f.read().strip()
            if not SHEET_ID:
                SHEET_ID = simpledialog.askstring("Google Sheets", "Ingresa el ID de tu hoja de Google Sheets para registrar la cita:\n(El ID es la parte entre /d/ y /edit en la URL)")
                if SHEET_ID:
                    with open(SHEET_ID_PATH, 'w', encoding='utf-8') as f:
                        f.write(SHEET_ID)
            if not SHEET_ID:
                messagebox.showwarning("Google Sheets", "No se proporcionó el ID de la hoja. No se registró la cita online.")
            else:
                gc = gspread.authorize(creds)
                sh = gc.open_by_key(SHEET_ID)
                ws = sh.sheet1
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ws.append_row([nombre, email, fecha, hora, tipo, link, timestamp])
                messagebox.showinfo("Google Sheets", "Cita registrada en la hoja online.")
        except Exception as e:
            messagebox.showwarning("Google Sheets", f"No se pudo registrar la cita en Google Sheets: {e}")
        messagebox.showinfo("Cita", f"Cita agendada y confirmación enviada a {email}.")

    def bot_charla(self):
        self.clear()
        tk.Label(self.root, text="Bot de Charla (escribe y presiona enviar)").pack()
        chat = tk.Text(self.root, height=10, width=40)
        chat.pack()
        entry = tk.Entry(self.root, width=30)
        entry.pack(side='left', padx=5)
        def enviar():
            mensaje = entry.get()
            if mensaje:
                chat.insert('end', f"Tú: {mensaje}\n")
                m = mensaje.lower()
                # Respuestas legales personalizadas
                if 'hola' in m:
                    chat.insert('end', "Bot: ¡Hola! ¿En qué puedo ayudarte?\n")
                elif 'gracias' in m:
                    chat.insert('end', "Bot: ¡De nada! Si tienes otra pregunta, dime.\n")
                elif 'asesoría' in m:
                    chat.insert('end', "Bot: Ofrecemos asesoría laboral, civil, penal y comercial.\n")
                elif 'laboral' in m:
                    chat.insert('end', "Bot: El derecho laboral regula las relaciones entre empleadores y trabajadores. ¿Tienes dudas sobre despidos, contratos o prestaciones?\n")
                elif 'civil' in m:
                    chat.insert('end', "Bot: El derecho civil abarca temas como herencias, contratos civiles, arrendamientos y familia. ¿Sobre qué tema civil necesitas ayuda?\n")
                elif 'penal' in m:
                    chat.insert('end', "Bot: El derecho penal trata delitos y sanciones. Si tienes dudas sobre denuncias, procesos penales o defensa, dime más detalles.\n")
                elif 'comercial' in m or 'mercantil' in m:
                    chat.insert('end', "Bot: El derecho comercial regula actividades empresariales, sociedades, contratos mercantiles y más. ¿Qué consulta tienes sobre derecho comercial?\n")
                elif 'divorcio' in m:
                    chat.insert('end', "Bot: El divorcio es un proceso legal para disolver el matrimonio. ¿Quieres saber requisitos, trámites o derechos tras el divorcio?\n")
                elif 'herencia' in m:
                    chat.insert('end', "Bot: La herencia es la transmisión de bienes tras el fallecimiento de una persona. ¿Tienes dudas sobre testamentos o sucesión intestada?\n")
                elif 'contrato' in m:
                    chat.insert('end', "Bot: Los contratos pueden ser civiles, laborales o mercantiles. ¿Sobre qué tipo de contrato necesitas información?\n")
                elif 'despido' in m:
                    chat.insert('end', "Bot: Si fuiste despedido, tienes derecho a recibir una justificación y, en su caso, una indemnización. ¿Quieres saber cómo reclamar?\n")
                elif 'demanda' in m:
                    chat.insert('end', "Bot: Para presentar una demanda necesitas identificar el tipo de asunto (laboral, civil, penal, etc.) y reunir pruebas. ¿Sobre qué tipo de demanda necesitas ayuda?\n")
                elif m == 'salir':
                    self.menu_principal()
                    return
                else:
                    # Si no hay coincidencia, usar ChatterBot
                    try:
                        respuesta = str(AsesoriaApp.chatbot.get_response(mensaje))
                        chat.insert('end', f"Bot: {respuesta}\n")
                    except Exception:
                        chat.insert('end', "Bot: Lo siento, no entendí tu pregunta.\n")
                entry.delete(0, 'end')
        tk.Button(self.root, text="Enviar", command=enviar).pack(side='left')
        tk.Button(self.root, text="Volver", command=self.menu_principal).pack(side='left', padx=5)

    def foro(self):
        mensaje = simpledialog.askstring("Foro", "Escribe tu mensaje para el foro (o 'salir' para volver):")
        if mensaje and mensaje.lower() != 'salir' and mensaje.strip():
            with open('foro.txt', 'a', encoding='utf-8') as f:
                f.write(mensaje + '\n')
            messagebox.showinfo("Foro", "Mensaje publicado en el foro.")

    def ver_foro(self):
        try:
            with open('foro.txt', 'r', encoding='utf-8') as f:
                mensajes = f.readlines()
                if mensajes:
                    messagebox.showinfo("Foro", '\n'.join([f"{i+1}. {m.strip()}" for i, m in enumerate(mensajes)]))
                else:
                    messagebox.showinfo("Foro", "No hay mensajes en el foro.")
        except FileNotFoundError:
            messagebox.showinfo("Foro", "No hay mensajes en el foro.")

    def cargar_documento(self):
        nombre_doc = simpledialog.askstring("Documento", "Nombre del archivo (ejemplo.pdf):")
        descripcion = simpledialog.askstring("Documento", "Descripción o mensaje para el asesor:")
        if nombre_doc and descripcion:
            with open('documentos.txt', 'a', encoding='utf-8') as f:
                f.write(f"Usuario: {self.usuario} | Archivo: {nombre_doc} | Mensaje: {descripcion}\n")
            messagebox.showinfo("Documento", "Documento registrado (simulado). El asesor podrá verlo.")

    def mensajeria(self):
        if self.rol == 'usuario':
            archivo = 'mensajes_admin.txt'
            archivo_ver = 'mensajes_usuario.txt'
        else:
            archivo = 'mensajes_usuario.txt'
            archivo_ver = 'mensajes_admin.txt'
        win = tk.Toplevel(self.root)
        win.title("Mensajería")
        def enviar():
            mensaje = entry.get()
            if mensaje:
                with open(archivo, 'a', encoding='utf-8') as f:
                    f.write(f"De {self.usuario}: {mensaje}\n")
                messagebox.showinfo("Mensajería", "Mensaje enviado.")
                entry.delete(0, 'end')
        def ver():
            try:
                with open(archivo_ver, 'r', encoding='utf-8') as f:
                    mensajes = f.readlines()
                    if mensajes:
                        messagebox.showinfo("Mensajes recibidos", '\n'.join([m.strip() for m in mensajes]))
                    else:
                        messagebox.showinfo("Mensajes recibidos", "No hay mensajes nuevos.")
            except FileNotFoundError:
                messagebox.showinfo("Mensajes recibidos", "No hay mensajes nuevos.")
        entry = tk.Entry(win, width=40)
        entry.pack(pady=5)
        tk.Button(win, text="Enviar mensaje", command=enviar).pack(fill='x')
        tk.Button(win, text="Ver mensajes recibidos", command=ver).pack(fill='x')
        tk.Button(win, text="Cerrar", command=win.destroy).pack(fill='x', pady=5)

    def cambiar_contrasena(self):
        nueva = simpledialog.askstring("Contraseña", "Nueva contraseña:")
        if nueva:
            usuarios[self.usuario]['password'] = nueva
            messagebox.showinfo("Contraseña", "Contraseña actualizada correctamente.")

    def info_cuenta(self):
        messagebox.showinfo("Cuenta", f"Usuario: {self.usuario}\nRol: {self.rol}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AsesoriaApp(root)
    root.mainloop()
