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

    def login(self):
        username = self.entry_username.get()
        input_password = self.entry_password.get()

        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()

            query = "SELECT password FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user[0]
                stored_hashed_password = stored_hashed_password.encode('utf-8')

                if check_password(input_password, stored_hashed_password):
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

        tk.Button(frame, text="Usuarios", command=lambda: handle_menu_action("Usuarios")).pack(pady=5)
        tk.Button(frame, text="Clientes", command=lambda: handle_menu_action("Clientes")).pack(pady=5)
        tk.Button(frame, text="Carros", command=lambda: handle_menu_action("Carros")).pack(pady=5)
        tk.Button(frame, text="Partes", command=lambda: handle_menu_action("Partes")).pack(pady=5)
        tk.Button(frame, text="Salir", command=menu_window.quit).pack(pady=20)

        menu_window.mainloop()

    def open_users_interface(self):
        users_window = tk.Tk()
        users_window.title("Gestión de Usuarios")
        users_window.minsize(400, 300)

        frame = tk.Frame(users_window)
        frame.pack(pady=20, padx=20)

        # Etiqueta y campo de entrada para buscar usuario por ID
        tk.Label(frame, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_id = tk.Entry(frame)
        self.entry_search_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Buscar", command=self.search_user).grid(row=0, column=2, padx=5, pady=5)

        # Etiquetas y campos de entrada para mostrar y editar datos del usuario
        tk.Label(frame, text="Usuario ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_user_id = tk.Entry(frame)
        self.entry_user_id.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Username:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = tk.Entry(frame)
        self.entry_username.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Perfil:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.profile_combobox = ttk.Combobox(frame, values=["Admin", "User", "Guest"])
        self.profile_combobox.grid(row=5, column=1, padx=5, pady=5)

        # Botones para acciones
        self.buttonNuevoUsuario=tk.Button(frame, text="Nuevo", command=lambda: self.handle_user_action("Nuevo"))
        self.buttonSalvarUsuario=tk.Button(frame, text="Salvar", command=lambda: self.handle_user_action("Salvar"))
        self.buttonEditarUsuario=tk.Button(frame, text="Editar", command=lambda: self.handle_user_action("Editar"))
        self.buttonCancelarUsuario=tk.Button(frame, text="Cancelar", command=lambda: self.handle_user_action("Cancelar"))
        self.buttonNuevoUsuario.grid(row=6, column=0, padx=5, pady=10)
        self.buttonSalvarUsuario.grid(row=6, column=1, padx=5, pady=10)
        self.buttonEditarUsuario.grid(row=6, column=2, padx=5, pady=10)
        self.buttonCancelarUsuario.grid(row=6, column=3, padx=5, pady=10)
        self.buttonNuevoUsuario.config(state="normal")
        self.buttonSalvarUsuario.config(state="disabled")
        self.buttonCancelarUsuario.config(state="disabled")
        self.buttonEditarUsuario.config(state="disable")
        self.entry_user_id.config(state="disabled")
        self.entry_name.config(state="disabled")
        self.entry_password.config(state="disabled")
        self.entry_username.config(state="disabled")
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
                self.entry_password.config(state="normal")
                self.entry_username.config(state="normal")
                self.profile_combobox.config(state="normal")
                self.entry_user_id.delete(0, tk.END)
                self.entry_user_id.insert(0, user[0])
                self.entry_name.delete(0, tk.END)
                self.entry_name.insert(0, user[1])
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, user[2])
                self.entry_password.delete(0, tk.END)
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
            try:
                """
                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()
                
                cursor.execute("select last_value from usuarios_usuario_id_seq;")
                next_id = cursor.fetchone()[0]
                """
                
                self.buttonNuevoUsuario.config(state="disable")
                self.buttonSalvarUsuario.config(state="normal")
                self.buttonCancelarUsuario.config(state="normal")
                self.buttonEditarUsuario.config(state="disable")
                self.entry_user_id.config(state="normal")
                self.entry_name.config(state="normal")
                self.entry_password.config(state="normal")
                self.entry_username.config(state="normal")
                self.profile_combobox.config(state="normal")
                self.entry_user_id.delete(0, tk.END) #aqui se insertaria el next_id obtenido de la query
                self.entry_name.delete(0, tk.END)
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.profile_combobox.set("")
                self.entry_name.config(state=tk.NORMAL)
                self.entry_username.config(state=tk.NORMAL)
                self.entry_password.config(state=tk.NORMAL)
                self.profile_combobox.config(state=tk.NORMAL)
                self.entry_user_id.config(state="disabled")

                """
                cursor.close()
                con.close()
                """

            except Exception as e:
                messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")
            
        elif action == "Salvar":            
            user_id = self.entry_user_id.get()
            name = self.entry_name.get()
            username = self.entry_username.get()
            password = self.entry_password.get()
            profile = self.profile_combobox.get()

            if not name or not username or not password or not profile:
                messagebox.showerror("Error", "Todos los campos deben ser llenados")
                return
            
            password = hash_password(password)
            
            try:
                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()

                if user_id:  # Si hay un ID, se asume que se está editando un usuario existente
                    query = """
                        UPDATE usuarios
                        SET nombre = %s, username = %s, password = %s, perfil = %s
                        WHERE usuario_id = %s
                    """
                    cursor.execute(query, (name, username, password, profile, user_id))
                    connection.commit()
                    messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                    self.handle_user_action("Cancelar")

                else:  # Si no hay ID, se está creando un nuevo usuario
                    query = """
                        INSERT INTO usuarios (nombre, username, password, perfil)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (name, username, password, profile))
                    connection.commit()
                    
                    messagebox.showinfo("Éxito", "Usuario creado correctamente")
                    self.handle_user_action("Cancelar")
                cursor.close()
                con.close()

            except Exception as e:
                messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")
        elif action == "Editar":
            self.entry_user_id.config(state="disabled")
            self.buttonNuevoUsuario.config(state="disable")
            self.buttonSalvarUsuario.config(state="normal")
            self.buttonCancelarUsuario.config(state="normal")
            self.buttonEditarUsuario.config(state="disable")
            messagebox.showinfo("Acción", "Puedes editar los campos ahora")
        elif action == "Cancelar":
            self.entry_user_id.config(state=tk.NORMAL)
            self.entry_name.config(state=tk.NORMAL)
            self.entry_username.config(state=tk.NORMAL)
            self.entry_password.config(state=tk.NORMAL)
            self.profile_combobox.config(state=tk.NORMAL)
            self.entry_user_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.profile_combobox.set("")
            self.entry_user_id.config(state=tk.DISABLED)
            self.entry_name.config(state=tk.DISABLED)
            self.entry_username.config(state=tk.DISABLED)
            self.entry_password.config(state=tk.DISABLED)
            self.profile_combobox.config(state=tk.DISABLED)
            self.buttonNuevoUsuario.config(state="normal")
            self.buttonSalvarUsuario.config(state="disabled")
            self.buttonCancelarUsuario.config(state="disabled")
            self.buttonEditarUsuario.config(state="disable")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
