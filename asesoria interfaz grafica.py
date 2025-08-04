import tkinter as tk
from tkinter import messagebox, simpledialog

usuarios = {
    'persona1': {'password': '123456', 'rol': 'admin'},
    'persona2': {'password': '123456', 'rol': 'usuario'}
}

class AsesoriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Asesoría Legal Virtual")
        self.usuario = None
        self.rol = None
        self.logo_img = None
        self.welcome_screen()

    def welcome_screen(self):
        self.clear()
        try:
            from PIL import Image, ImageTk
            logo = Image.open("logo.png")
            logo = logo.resize((120, 120))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self.root, image=self.logo_img).pack(pady=10)
        except Exception:
            tk.Label(self.root, text="Asesoría Legal Virtual", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(self.root, text="Bienvenido a la plataforma de asesoría legal virtual", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Iniciar", command=self.login_screen, width=20, height=2, bg="#4CAF50", fg="white").pack(pady=20)

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
        if self.logo_img:
            tk.Label(self.root, image=self.logo_img).pack(pady=10)
        tk.Label(self.root, text=f"Bienvenido {self.usuario} ({self.rol})", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Button(self.root, text="Ir al menú principal", command=self.menu_principal, bg="#4CAF50", fg="white").pack(fill='x')
        tk.Button(self.root, text="Cambiar contraseña", command=self.cambiar_contrasena).pack(fill='x')
        tk.Button(self.root, text="Ver información de cuenta", command=self.info_cuenta).pack(fill='x')
        tk.Button(self.root, text="Cerrar sesión", command=self.login_screen, bg="#f44336", fg="white").pack(fill='x')

    def menu_principal(self):
        self.clear()
        tk.Label(self.root, text=f"Menú principal - {self.usuario} ({self.rol})").pack(pady=5)
        tk.Button(self.root, text="Consultar tipo de asesoría", command=self.consultar_asesoria).pack(fill='x')
        tk.Button(self.root, text="Agendar cita", command=self.agendar_cita).pack(fill='x')
        tk.Button(self.root, text="Bot de charla", command=self.bot_charla).pack(fill='x')
        tk.Button(self.root, text="Foro", command=self.foro).pack(fill='x')
        if self.rol == 'admin':
            tk.Button(self.root, text="Ver mensajes del foro", command=self.ver_foro).pack(fill='x')
        else:
            tk.Button(self.root, text="Cargar documento", command=self.cargar_documento).pack(fill='x')
        tk.Button(self.root, text="Mensajería asesoría", command=self.mensajeria).pack(fill='x')
        tk.Button(self.root, text="Salir al login", command=self.login_screen).pack(fill='x', pady=10)

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
        tipo = simpledialog.askstring("Cita", "Tipo de asesoría (Laboral, Civil, etc.):")
        if nombre and fecha and tipo:
            messagebox.showinfo("Cita", f"Cita agendada para {nombre} el día {fecha} para asesoría {tipo}.")

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
                if 'hola' in mensaje.lower():
                    chat.insert('end', "Bot: ¡Hola! ¿En qué puedo ayudarte?\n")
                elif 'gracias' in mensaje.lower():
                    chat.insert('end', "Bot: ¡De nada! Si tienes otra pregunta, dime.\n")
                elif 'asesoría' in mensaje.lower():
                    chat.insert('end', "Bot: Ofrecemos asesoría laboral, civil, penal y comercial.\n")
                elif mensaje.lower() == 'salir':
                    self.menu_principal()
                    return
                else:
                    chat.insert('end', "Bot: Lo siento, soy un bot sencillo. ¿Puedes reformular tu pregunta?\n")
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
