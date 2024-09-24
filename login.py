import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import connection as dbconn
from hasspass import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.minsize(300, 200)

        frame = tk.Frame(self.root)
        frame.pack(pady=20, padx=20)

        tk.Label(frame, text="Username:").grid(row=0, column=0, pady=5)
        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        tk.Button(self.root, text="Acceder", command=self.login).pack(pady=10)

        # Variable para almacenar el perfil del usuario
        self.user_profile = None

    def login(self):
        username = self.entry_username.get()
        input_password = self.entry_password.get()

        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT usuario_id, username, password, perfil FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user:
                stored_user_id = user[0]  # Almacenar el usuario_id del usuario
                stored_username = user[1]  # Almacenar el username
                stored_hashed_password = user[2]
                stored_hashed_password = stored_hashed_password.encode('utf-8')

                if check_password(input_password, stored_hashed_password):
                    self.user_id = stored_user_id  # Almacenar el usuario_id
                    self.username = stored_username   # Almacenar el username
                    self.user_profile = user[3]       # Almacenar el perfil del usuario
                    self.root.destroy()
                    self.open_main_menu()
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

            cursor.close()
            con.close()

        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")




    def open_main_menu(self):
        menu_window = tk.Tk()
        menu_window.title("Menú Principal")
        menu_window.minsize(400, 300)

        frame = tk.Frame(menu_window)
        frame.pack(pady=20, padx=20)

        # Función para manejar los botones del menú
        def handle_menu_action(action):
            menu_window.destroy()
            if action == "Usuarios":
                self.open_users_interface()
            elif action == "Clientes":
                self.open_clients_interface()
            elif action == "Carros":
                self.open_carros_interface()
            elif action == "Partes":
                self.open_partes_interface()
            elif action == "Reparaciones":
                self.open_reparaciones_interface()
            elif action == "Vehiculos":
                self.open_vehiculos_interface()
            elif action == "Salir":
                menu_window.quit()

        # Crear botones según el perfil del usuario
        if self.user_profile.lower() == "admin":
            tk.Button(frame, text="Usuarios", width=20, command=lambda: handle_menu_action("Usuarios")).pack(pady=5)
            tk.Button(frame, text="Clientes", width=20, command=lambda: handle_menu_action("Clientes")).pack(pady=5)
            tk.Button(frame, text="Carros", width=20, command=lambda: handle_menu_action("Carros")).pack(pady=5)
            tk.Button(frame, text="Partes", width=20, command=lambda: handle_menu_action("Partes")).pack(pady=5)
            tk.Button(frame, text="Reparaciones", width=20, command=lambda: handle_menu_action("Reparaciones")).pack(pady=5)  # Botón adicional para Admin
            tk.Button(frame, text="Salir", width=20, command=lambda: handle_menu_action("Salir")).pack(pady=20)
        elif self.user_profile.lower() == "secretaria":
            tk.Button(frame, text="Clientes", width=20, command=lambda: handle_menu_action("Clientes")).pack(pady=5)
            tk.Button(frame, text="Carros", width=20, command=lambda: handle_menu_action("Carros")).pack(pady=5)
            tk.Button(frame, text="Salir", width=20, command=lambda: handle_menu_action("Salir")).pack(pady=20)
        elif self.user_profile.lower() == "mecanico":
            tk.Button(frame, text="Vehiculos", width=20, command=lambda: handle_menu_action("Vehiculos")).pack(pady=5)
            tk.Button(frame, text="Reparación", width=20, command=lambda: handle_menu_action("Reparaciones")).pack(pady=5)
            tk.Button(frame, text="Salir", width=20, command=lambda: handle_menu_action("Salir")).pack(pady=20)
        else:
            messagebox.showerror("Error", "Perfil de usuario no reconocido")
            menu_window.destroy()

        menu_window.mainloop()

    def open_users_interface(self):
        users_window = tk.Tk()
        users_window.title("Gestión de Usuarios")
        users_window.minsize(400, 300)

        frame = tk.Frame(users_window)
        frame.pack(pady=20, padx=20)
        tk.Label(frame, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_id = tk.Entry(frame)
        self.entry_search_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Buscar", command=self.search_user).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame, text="Usuario ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_user_id = tk.Entry(frame)
        self.entry_user_id.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_username_user = tk.Entry(frame)
        self.entry_username_user.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.entry_password_user = tk.Entry(frame, show="*")
        self.entry_password_user.grid(row=4, column=1, padx=5, pady=5)
        tk.Label(frame, text="Perfil:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.profile_combobox = ttk.Combobox(frame, values=["Admin", "Secretaria", "Mecanico"])
        self.profile_combobox.grid(row=5, column=1, padx=5, pady=5)

        # Botones para acciones
        self.buttonNuevoUsuario = tk.Button(frame, text="Nuevo", command=lambda: self.handle_user_action("Nuevo"))
        self.buttonSalvarUsuario = tk.Button(frame, text="Salvar", command=lambda: self.handle_user_action("Salvar"))
        self.buttonEditarUsuario = tk.Button(frame, text="Editar", command=lambda: self.handle_user_action("Editar"))
        self.buttonCancelarUsuario = tk.Button(frame, text="Cancelar", command=lambda: self.handle_user_action("Cancelar"))
        self.buttonNuevoUsuario.grid(row=6, column=0, padx=5, pady=10)
        self.buttonSalvarUsuario.grid(row=6, column=1, padx=5, pady=10)
        self.buttonEditarUsuario.grid(row=6, column=2, padx=5, pady=10)
        self.buttonCancelarUsuario.grid(row=6, column=3, padx=5, pady=10)
        self.buttonNuevoUsuario.config(state="normal")
        self.buttonSalvarUsuario.config(state="disabled")
        self.buttonCancelarUsuario.config(state="disabled")
        self.buttonEditarUsuario.config(state="disabled")
        self.entry_user_id.config(state="disabled")
        self.entry_name.config(state="disabled")
        self.entry_password_user.config(state="disabled")
        self.entry_username_user.config(state="disabled")
        self.profile_combobox.config(state="disabled")

        users_window.mainloop()

    def search_user(self):
        user_id = self.entry_search_id.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT * FROM usuarios WHERE usuario_id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user:
                self.buttonNuevoUsuario.config(state="disabled")
                self.buttonSalvarUsuario.config(state="disabled")
                self.buttonCancelarUsuario.config(state="normal")
                self.buttonEditarUsuario.config(state="normal")
                self.entry_user_id.config(state="normal")
                self.entry_name.config(state="normal")
                self.entry_password_user.config(state="normal")
                self.entry_username_user.config(state="normal")
                self.profile_combobox.config(state="normal")
                self.entry_user_id.delete(0, tk.END)
                self.entry_user_id.insert(0, user[0])
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, user[1])
                self.entry_username_user.delete(0, tk.END)
                self.entry_username_user.insert(0, user[2])
                self.entry_password_user.delete(0, tk.END)
                self.profile_combobox.set(user[4])
                self.entry_user_id.config(state="disabled")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

            cursor.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")

    def handle_user_action(self, action):
        if action == "Nuevo":
                self.buttonNuevoUsuario.config(state="disabled")
                self.buttonSalvarUsuario.config(state="normal")
                self.buttonCancelarUsuario.config(state="normal")
                self.buttonEditarUsuario.config(state="disabled")
                self.entry_user_id.config(state="disabled")
                self.entry_name.config(state="normal")
                self.entry_password_user.config(state="normal")
                self.entry_username_user.config(state="normal")
                self.profile_combobox.config(state="normal")
                self.entry_name.delete(0, tk.END)
                self.entry_username_user.delete(0, tk.END)
                self.entry_password_user.delete(0, tk.END)
                self.profile_combobox.set("")

                # Obtener el siguiente ID disponible desde la base de datos
                try:
                    con = dbconn.connection()
                    connection = con.open()
                    cursor = connection.cursor()
                    query = "SELECT MAX(usuario_id) FROM usuarios"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    next_id = result[0] + 1 if result[0] is not None else 1
                    self.entry_user_id.config(state=tk.NORMAL)
                    self.entry_user_id.delete(0, tk.END)
                    self.entry_user_id.insert(0, str(next_id))
                    self.entry_user_id.config(state="disabled")

                    cursor.close()
                    con.close()

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo obtener el siguiente ID disponible. Error: {e}")
        
        elif action == "Salvar":
            user_id = self.entry_user_id.get()
            name = self.entry_name.get()
            username = self.entry_username_user.get()
            password = self.entry_password_user.get()
            profile = self.profile_combobox.get()

            if not name or not username or not password or not profile:
                messagebox.showerror("Error", "Todos los campos deben ser llenados")
                return

            hashed_password = hash_password(password)

            try:
                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()
                query = """
                        INSERT INTO usuarios (nombre, username, password, perfil)
                        VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query, (name, username, hashed_password, profile))
                connection.commit()

                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                self.handle_user_action("Cancelar")
                cursor.close()
                con.close()

            except Exception as e:
                messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")
                
        elif action == "Editar":
            user_id = self.entry_user_id.get()
            name = self.entry_name.get()
            username = self.entry_username_user.get()
            password = self.entry_password_user.get()
            profile = self.profile_combobox.get()

            if not name or not username or not profile:
                messagebox.showerror("Error", "Los campos de nombre, usuario y perfil deben ser llenados")
                return

            try:
                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()

                if user_id:  
                    update_query = "UPDATE usuarios SET nombre = %s, username = %s, perfil = %s"
                    params = [name, username, profile]
                    # Solo actualizar la contraseña si se ingresó una nueva
                    if password:
                        hashed_password = hash_password(password)
                        update_query += ", password = %s"
                        params.append(hashed_password)
                    update_query += " WHERE usuario_id = %s"
                    params.append(user_id)

                    cursor.execute(update_query, tuple(params))
                    connection.commit()

                    messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                    self.handle_user_action("Cancelar")
                else:
                    messagebox.showerror("Error", "No se encontró el ID del usuario para editar.")
                
                cursor.close()
                con.close()

            except Exception as e:
                messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")

        elif action == "Cancelar":
            self.entry_user_id.config(state=tk.NORMAL)
            self.entry_name.config(state=tk.NORMAL)
            self.entry_username_user.config(state=tk.NORMAL)
            self.entry_password_user.config(state=tk.NORMAL)
            self.profile_combobox.config(state=tk.NORMAL)
            self.entry_user_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.entry_username_user.delete(0, tk.END)
            self.entry_password_user.delete(0, tk.END)
            self.profile_combobox.set("")
            self.entry_user_id.config(state="disabled")
            self.entry_name.config(state="disabled")
            self.entry_username_user.config(state="disabled")
            self.entry_password_user.config(state="disabled")
            self.profile_combobox.config(state="disabled")
            self.buttonNuevoUsuario.config(state="normal")
            self.buttonSalvarUsuario.config(state="disabled")
            self.buttonCancelarUsuario.config(state="disabled")
            self.buttonEditarUsuario.config(state="disabled")

    def open_clients_interface(self):
        clients_window = tk.Tk()
        clients_window.title("Gestión de Clientes")
        clients_window.minsize(500, 400)

        frame = tk.Frame(clients_window)
        frame.pack(pady=20, padx=20)

        # Ingreso del ID del cliente a buscar
        tk.Label(frame, text="Ingrese ID del cliente a buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_client_id = tk.Entry(frame)
        self.entry_search_client_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Buscar", command=self.search_client).grid(row=0, column=2, padx=5, pady=5)

        # Prellenado con información de usuario logueado
    # Mostrar el ID del usuario logueado (usuario_id)
        tk.Label(frame, text="Usuario ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_user_id = tk.Entry(frame)
        self.entry_user_id.insert(0, self.user_id)  # Mostrar el usuario_id
        self.entry_user_id.config(state='disabled')
        self.entry_user_id.grid(row=1, column=1, padx=5, pady=5)

        # Mostrar el username del usuario logueado
        tk.Label(frame, text="Username:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = tk.Entry(frame)
        self.entry_username.insert(0, self.username)  # Mostrar el username
        self.entry_username.config(state='disabled')
        self.entry_username.grid(row=2, column=1, padx=5, pady=5)

        # Campos de información del cliente
        tk.Label(frame, text="ID del Cliente:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_client_id = tk.Entry(frame)
        self.entry_client_id.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nombre del Cliente:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.entry_client_name = tk.Entry(frame)
        self.entry_client_name.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Teléfono:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.entry_client_phone = tk.Entry(frame)
        self.entry_client_phone.grid(row=5, column=1, padx=5, pady=5)

        # Botones de acción
        self.buttonNuevoCliente = tk.Button(frame, text="Nuevo", command=lambda: self.handle_client_action("Nuevo"))
        self.buttonGuardarCliente = tk.Button(frame, text="Guardar", command=lambda: self.handle_client_action("Guardar"))
        self.buttonEditarCliente = tk.Button(frame, text="Editar", command=lambda: self.handle_client_action("Editar"))
        self.buttonCancelarCliente = tk.Button(frame, text="Cancelar", command=lambda: self.handle_client_action("Cancelar"))
        
        self.buttonNuevoCliente.grid(row=6, column=0, padx=5, pady=10)
        self.buttonGuardarCliente.grid(row=6, column=1, padx=5, pady=10)
        self.buttonEditarCliente.grid(row=6, column=2, padx=5, pady=10)
        self.buttonCancelarCliente.grid(row=6, column=3, padx=5, pady=10)

        # Desactivar botones de edición inicialmente
        self.buttonGuardarCliente.config(state="disabled")
        self.buttonEditarCliente.config(state="disabled")
        self.buttonCancelarCliente.config(state="disabled")
        clients_window.mainloop()
        
    def search_client(self):
        client_id = self.entry_search_client_id.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT * FROM clientes WHERE cliente_id = %s"
            cursor.execute(query, (client_id,))
            client = cursor.fetchone()

            if client:
                self.entry_client_id.config(state="normal")
                self.entry_client_id.delete(0, tk.END)
                self.entry_client_id.insert(0, client[0])
                self.entry_client_name.delete(0, tk.END)
                self.entry_client_name.insert(0, client[2])
                self.entry_client_phone.delete(0, tk.END)
                self.entry_client_phone.insert(0, client[3])
                self.buttonEditarCliente.config(state="normal")
            else:
                messagebox.showerror("Error", "Cliente no encontrado")

            cursor.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")

    def handle_client_action(self, action):
        if action == "Nuevo":
            self.entry_client_id.config(state="normal")
            self.entry_client_name.config(state="normal")
            self.entry_client_phone.config(state="normal")
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_name.delete(0, tk.END)
            self.entry_client_phone.delete(0, tk.END)
            self.buttonGuardarCliente.config(state="normal")
            self.buttonCancelarCliente.config(state="normal")
            self.buttonEditarCliente.config(state="disabled")

        elif action == "Guardar":
                # No necesitas obtener client_id ya que es SERIAL
                user_id = self.user_id
                client_name = self.entry_client_name.get()
                client_phone = self.entry_client_phone.get()

                if not client_name or not client_phone:
                    messagebox.showerror("Error", "Todos los campos deben ser llenados")
                    return

                try:
                    con = dbconn.connection()
                    connection = con.open()
                    cursor = connection.cursor()
                    query = """
                            INSERT INTO clientes (usuario_id, nombre, telefono)
                            VALUES (%s, %s, %s)
                        """
                    cursor.execute(query, (user_id, client_name, client_phone))
                    connection.commit()

                    messagebox.showinfo("Éxito", "Cliente guardado correctamente")
                    self.handle_client_action("Cancelar")
                    cursor.close()
                    con.close()

                except Exception as e:
                    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")


        elif action == "Cancelar":
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_name.delete(0, tk.END)
            self.entry_client_phone.delete(0, tk.END)
            self.buttonGuardarCliente.config(state="disabled")
            self.buttonEditarCliente.config(state="disabled")
            self.buttonCancelarCliente.config(state="disabled")

    def open_carros_interface(self):
        messagebox.showinfo("Carros", "Interfaz de Carros aún no implementada.")

    def open_partes_interface(self):
        messagebox.showinfo("Partes", "Interfaz de Partes aún no implementada.")

    def open_reparaciones_interface(self):
        messagebox.showinfo("Reparaciones", "Interfaz de Reparaciones aún no implementada.")

    def open_vehiculos_interface(self):
        messagebox.showinfo("Vehiculos", "Interfaz de Vehiculos aún no implementada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
