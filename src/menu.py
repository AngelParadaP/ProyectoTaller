import tkinter as tk
from tkinter import messagebox
from .users import UsersFrame
from .clients import ClientsFrame
from .vehicles import VehiclesFrame
from .repairs import RepairsFrame
from .pieces import PiecesFrame

class Menu:
    def __init__(self, user_info):
        self.user_info = user_info
        self.current_frame = None

    def open_main_menu(self):
        self.menu_window = tk.Tk()
        self.menu_window.title("Menú Principal")
        self.menu_window.minsize(500, 300)

        # Contenedor principal
        self.container = tk.Frame(self.menu_window)
        self.container.pack(fill="both", expand=True)

        # Frame para el menú
        self.menu_frame = tk.Frame(self.container)
        self.menu_frame.pack(side="top", fill="x")

        # Etiqueta de bienvenida
        self.welcome_label = tk.Label(self.container, text=f'Hola {self.user_info["NOMBRE"]}', font=("Arial", 16))
        self.welcome_label.pack(pady=20)

        # Crear botones para el menú
        self.create_menu_buttons()

        self.menu_window.mainloop()

    def create_menu_buttons(self):
        # Diccionario de acciones según el perfil del usuario
        profile_actions = {
            "admin": ["Usuarios", "Clientes", "Vehiculos", "Reparaciones", "Partes", "Cerrar Sesion"],
            "secretaria": ["Clientes", "Vehiculos", "Cerrar Sesion"],
            "mecanico": ["Vehiculos", "Reparaciones", "Cerrar Sesion"]
        }

        actions = profile_actions.get(self.user_info["PERFIL"].lower())
        if actions:
            for action in actions:
                button = tk.Button(self.menu_frame, text=action, command=lambda a=action: self.handle_menu_action(a))
                button.pack(side="left", padx=5, pady=5)  # Espaciado entre botones
        else:
            messagebox.showerror("Error", "Perfil de usuario no reconocido")
            self.menu_window.destroy()

    def handle_menu_action(self, action):
        if self.current_frame:
            self.current_frame.destroy()  # Eliminar el frame actual
            self.welcome_label.pack_forget()


        if action == "Cerrar Sesion":
            self.menu_window.destroy()
            from .login import Login
            Login()
            return

        # Inicializa el frame correspondiente
        frame_class = {
            "Usuarios": UsersFrame,
            "Clientes": ClientsFrame,
            "Vehiculos": VehiclesFrame,
            "Reparaciones": RepairsFrame,
            "Partes": PiecesFrame
        }.get(action)

        if frame_class:
            self.current_frame = frame_class(self, self.container)
            self.current_frame.pack(fill="both", expand=True)  # Mostrar el nuevo frame
