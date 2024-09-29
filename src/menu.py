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
        self.current_frame = None  # Para almacenar el frame actual

    def open_main_menu(self):
        self.menu_window = tk.Tk()
        self.menu_window.title("Menú Principal")
        self.menu_window.minsize(500, 300)
        
        # Frame contenedor donde se mostrarán los frames
        self.container = tk.Frame(self.menu_window)
        self.container.pack(fill="both", expand=True)
        
        self.welcome_label = tk.Label(self.container, text=f'Hola {self.user_info["NOMBRE"]}', font=("Arial", 16))
        self.welcome_label.pack(pady=20)  # Añadir algo de margen


        def handle_menu_action(action):
            if self.current_frame:
                self.current_frame.destroy()  # Eliminar el frame actual
                
            self.welcome_label.forget()
            
            if action == "Usuarios":
                self.current_frame = UsersFrame(self, self.container)
            elif action == "Clientes":
                self.current_frame = ClientsFrame(self, self.container)
            elif action == "Vehiculos":
                self.current_frame = VehiclesFrame(self, self.container)
            elif action == "Reparaciones":
                self.current_frame = RepairsFrame(self, self.container)
            elif action == "Partes":
                self.current_frame = PiecesFrame(self, self.container)
            elif action == "Cerrar Sesion":
                self.current_frame = None
                self.menu_window.destroy()
                from .login import Login
                Login()

            if self.current_frame:
                self.current_frame.pack(fill="both", expand=True)  # Mostrar el nuevo frame

        self.menu = tk.Menu(self.menu_window)
        self.menu_window.config(menu=self.menu)

        # Configurar el menú según el perfil del usuario
        if self.user_info["PERFIL"].lower() == "admin":
            self.menu.add_cascade(label="Usuarios", command=lambda: handle_menu_action("Usuarios"))
            self.menu.add_cascade(label="Clientes", command=lambda: handle_menu_action("Clientes"))
            self.menu.add_cascade(label="Vehiculos", command=lambda: handle_menu_action("Vehiculos"))
            self.menu.add_cascade(label="Reparaciones", command=lambda: handle_menu_action("Reparaciones"))
            self.menu.add_cascade(label="Partes", command=lambda: handle_menu_action("Partes"))
            self.menu.add_cascade(label="Cerrar Sesion", command=lambda: handle_menu_action("Cerrar Sesion"))
        elif self.user_info["PERFIL"].lower() == "secretaria":
            self.menu.add_cascade(label="Clientes", command=lambda: handle_menu_action("Clientes"))
            self.menu.add_cascade(label="Vehiculos", command=lambda: handle_menu_action("Vehiculos"))
            self.menu.add_cascade(label="Cerrar Sesion", command=lambda: handle_menu_action("Cerrar Sesion"))
        elif self.user_info["PERFIL"].lower() == "mecanico":
            self.menu.add_cascade(label="Vehiculos", command=lambda: handle_menu_action("Vehiculos"))
            self.menu.add_cascade(label="Reparaciones", command=lambda: handle_menu_action("Reparaciones"))
            self.menu.add_cascade(label="Cerrar Sesion", command=lambda: handle_menu_action("Cerrar Sesion"))
        else:
            messagebox.showerror("Error", "Perfil de usuario no reconocido")
            self.menu_window.destroy()

        self.menu_window.mainloop()
