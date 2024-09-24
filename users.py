import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import connection as dbconn
from hasspass import *

class UsersInterface:
    def open_users_interface(self, username):
        users_window = tk.Tk()
        users_window.title("Gestión de Usuarios")
        users_window.minsize(400, 300)

        # Mostrar el nombre del usuario autenticado en la parte superior
        tk.Label(users_window, text=f"Usuario: {username}", font=("Arial", 12)).pack(pady=10)

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

        self.disable_user_fields()

        users_window.mainloop()

    def disable_user_fields(self):
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
                self.populate_user_fields(user)
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

            cursor.close()
            con.close()

        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\nError: {e}")

    def populate_user_fields(self, user):
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
