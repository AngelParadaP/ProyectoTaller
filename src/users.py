import tkinter as tk
from tkinter import ttk, messagebox
import utilities.connection as dbconn
from utilities.hasspass import *

class UsersFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent 
        #PARA ACCEDER A LA INFO DE USUARIO USAR self.parent.user_info['AQUI VA EL CAMPO']
        self.setup_ui()

    def setup_ui(self):
        # Crear el frame de la interfaz de usuarios
        frame = tk.Frame(self)
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

        # Configuraciones iniciales
        self.buttonNuevoUsuario.config(state="normal")
        self.buttonSalvarUsuario.config(state="disabled")
        self.buttonCancelarUsuario.config(state="disabled")
        self.buttonEditarUsuario.config(state="disabled")
        self.entry_user_id.config(state="disabled")
        self.entry_name.config(state="disabled")
        self.entry_password_user.config(state="disabled")
        self.entry_username_user.config(state="disabled")
        self.profile_combobox.config(state="disabled")

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