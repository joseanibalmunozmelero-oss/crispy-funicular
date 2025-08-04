# asesoria.py

def mostrar_menu():
    print("\n--- Asesoría Legal Virtual ---")
    print("1. Consultar tipo de asesoría")
    print("2. Agendar cita")
    print("3. Bot de charla")
    print("4. Foro")
    print("5. Cargar documento")
    print("6. Mensajería asesoría")
    print("7. Salir")

def mostrar_menu_admin():
    print("\n--- Panel de Administrador ---")
    print("1. Consultar tipo de asesoría")
    print("2. Agendar cita")
    print("3. Bot de charla")
    print("4. Foro")
    print("5. Ver mensajes del foro")
    print("6. Mensajería asesoría")
    print("7. Salir")

def consultar_asesoria():
    tipos = {
        1: "Laboral",
        2: "Civil",
        3: "Penal",
        4: "Comercial"
    }
    print("\nTipos de asesorías disponibles:")
    for numero, nombre in sorted(tipos.items()):
        print(f"{numero}. {nombre}")
    seleccion = int(input("Selecciona un número: "))
    print(f"\nHas elegido asesoría en: {tipos.get(seleccion, 'Opción no válida')}")

def bot_charla():
    print("\n--- Bot de Charla ---")
    print("Escribe 'salir' para volver al menú.")
    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() == 'salir':
            break
        if 'hola' in mensaje.lower():
            print("Bot: ¡Hola! ¿En qué puedo ayudarte?")
        elif 'gracias' in mensaje.lower():
            print("Bot: ¡De nada! Si tienes otra pregunta, dime.")
        elif 'asesoría' in mensaje.lower():
            print("Bot: Ofrecemos asesoría laboral, civil, penal y comercial.")
        else:
            print("Bot: Lo siento, soy un bot sencillo. ¿Puedes reformular tu pregunta?")

def foro():
    print("\n--- Foro de Mensajes ---")
    mensaje = input("Escribe tu mensaje para el foro (o 'salir' para volver): ")
    if mensaje.lower() != 'salir' and mensaje.strip():
        with open('foro.txt', 'a', encoding='utf-8') as f:
            f.write(mensaje + '\n')
        print("Mensaje publicado en el foro.")

def ver_foro():
    print("\n--- Mensajes del Foro ---")
    try:
        with open('foro.txt', 'r', encoding='utf-8') as f:
            mensajes = f.readlines()
            if mensajes:
                for i, m in enumerate(mensajes, 1):
                    print(f"{i}. {m.strip()}")
            else:
                print("No hay mensajes en el foro.")
    except FileNotFoundError:
        print("No hay mensajes en el foro.")

def cargar_documento(usuario):
    print("\n--- Cargar Documento ---")
    nombre_doc = input("Nombre del archivo (ejemplo.pdf): ")
    descripcion = input("Descripción o mensaje para el asesor: ")
    with open('documentos.txt', 'a', encoding='utf-8') as f:
        f.write(f"Usuario: {usuario} | Archivo: {nombre_doc} | Mensaje: {descripcion}\n")
    print("Documento registrado (simulado). El asesor podrá verlo.")

def mensajeria(usuario, rol):
    print("\n--- Mensajería Asesoría ---")
    archivo = 'mensajes_admin.txt' if rol == 'usuario' else 'mensajes_usuario.txt'
    archivo_ver = 'mensajes_usuario.txt' if rol == 'usuario' else 'mensajes_admin.txt'
    while True:
        print("1. Enviar mensaje")
        print("2. Ver mensajes recibidos")
        print("3. Volver al menú principal")
        op = input("Elige una opción: ")
        if op == '1':
            mensaje = input("Escribe tu mensaje: ")
            with open(archivo, 'a', encoding='utf-8') as f:
                f.write(f"De {usuario}: {mensaje}\n")
            print("Mensaje enviado.")
        elif op == '2':
            print("\n--- Mensajes recibidos ---")
            try:
                with open(archivo_ver, 'r', encoding='utf-8') as f:
                    mensajes = f.readlines()
                    if mensajes:
                        for m in mensajes:
                            print(m.strip())
                    else:
                        print("No hay mensajes nuevos.")
            except FileNotFoundError:
                print("No hay mensajes nuevos.")
        elif op == '3':
            break
        else:
            print("Opción no válida.")

def agendar_cita():
    nombre = input("Tu nombre completo: ")
    fecha = input("Fecha deseada (dd/mm/aaaa): ")
    tipo = input("Tipo de asesoría (Laboral, Civil, etc.): ")
    print(f"\nCita agendada para {nombre} el día {fecha} para asesoría {tipo}.")

def main():
    usuarios = {
        'persona1': {'password': '123456', 'rol': 'admin'},
        'persona2': {'password': '123456', 'rol': 'usuario'}
    }
    while True:
        print("Bienvenido al sistema de Asesoría Legal Virtual")
        user = input("Usuario: ")
        pwd = input("Contraseña: ")
        if user in usuarios and usuarios[user]['password'] == pwd:
            rol = usuarios[user]['rol']
            print(f"\nLogin exitoso. Rol: {rol}")
            while True:
                print("\n--- Menú de Inicio de Sesión ---")
                print("1. Ir al menú principal")
                print("2. Cambiar contraseña")
                print("3. Ver información de cuenta")
                print("4. Cerrar sesión")
                opcion_inicio = input("Elige una opción: ")
                if opcion_inicio == '1':
                    while True:
                        if rol == 'admin':
                            mostrar_menu_admin()
                            opcion = input("Elige una opción: ")
                            if opcion == '1':
                                consultar_asesoria()
                            elif opcion == '2':
                                agendar_cita()
                            elif opcion == '3':
                                bot_charla()
                            elif opcion == '4':
                                foro()
                            elif opcion == '5':
                                ver_foro()
                            elif opcion == '6':
                                mensajeria(user, rol)
                            elif opcion == '7':
                                print("Gracias por utilizar el sistema. ¡Hasta pronto!")
                                break
                            else:
                                print("Opción no válida. Intenta nuevamente.")
                        else:
                            mostrar_menu()
                            opcion = input("Elige una opción: ")
                            if opcion == '1':
                                consultar_asesoria()
                            elif opcion == '2':
                                agendar_cita()
                            elif opcion == '3':
                                bot_charla()
                            elif opcion == '4':
                                foro()
                            elif opcion == '5':
                                cargar_documento(user)
                            elif opcion == '6':
                                mensajeria(user, rol)
                            elif opcion == '7':
                                print("Gracias por utilizar el sistema. ¡Hasta pronto!")
                                break
                            else:
                                print("Opción no válida. Intenta nuevamente.")
                    break
                elif opcion_inicio == '2':
                    nueva_pwd = input("Nueva contraseña: ")
                    usuarios[user]['password'] = nueva_pwd
                    print("Contraseña actualizada correctamente.")
                elif opcion_inicio == '3':
                    print(f"\nUsuario: {user}\nRol: {rol}")
                elif opcion_inicio == '4':
                    print("Sesión cerrada. ¡Hasta pronto!")
                    break
                else:
                    print("Opción no válida. Intenta nuevamente.")
            # Al cerrar sesión, volver al login
        else:
            print("Usuario o contraseña incorrectos.")

if __name__ == "__main__":
    main()


