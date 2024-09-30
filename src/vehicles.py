import tkinter as tk
from tkinter import ttk
import utilities.connection as dbconn
from tkinter import messagebox

class VehiclesFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self)
        frame.pack(pady=20, padx=20)

        tk.Label(frame, text="Ingrese Matrícula para buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_matricula = tk.Entry(frame)
        self.entry_search_matricula.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Buscar", command=lambda: self.search_vehicle()).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(frame, text="Matrícula:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_matricula = tk.Entry(frame)
        self.entry_matricula.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Cliente:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_clientes = ttk.Combobox(frame)
        self.combo_clientes.grid(row=2, column=1, padx=5, pady=5)
        self.load_clientes()

        tk.Label(frame, text="ID Cliente:").grid(row=2, column=2, padx=5, pady=5)
        self.entry_client_id = tk.Entry(frame)
        self.entry_client_id.config(state='disabled')
        self.entry_client_id.grid(row=2, column=3, padx=5, pady=5)

        tk.Label(frame, text="Marca:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_marca = tk.Entry(frame)
        self.entry_marca.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Modelo:").grid(row=3, column=2, padx=5, pady=5)
        self.entry_modelo = tk.Entry(frame)
        self.entry_modelo.grid(row=3, column=3, padx=5, pady=5)

        tk.Label(frame, text="Color:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_color = tk.Entry(frame)
        self.entry_color.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Kilómetros:").grid(row=4, column=2, padx=5, pady=5)
        self.entry_km = tk.Entry(frame)
        self.entry_km.grid(row=4, column=3, padx=5, pady=5)

        self.buttonNuevoVehiculo = tk.Button(frame, text="Nuevo", command=lambda: self.handle_vehicle_action("Nuevo"))
        self.buttonGuardarVehiculo = tk.Button(frame, text="Guardar", command=lambda: self.handle_vehicle_action("Guardar"))
        self.buttonEditarVehiculo = tk.Button(frame, text="Editar", command=lambda: self.handle_vehicle_action("Editar"))
        self.buttonCancelarVehiculo = tk.Button(frame, text="Cancelar", command=lambda: self.handle_vehicle_action("Cancelar"))

        self.buttonNuevoVehiculo.grid(row=8, column=0, padx=5, pady=10)
        self.buttonGuardarVehiculo.grid(row=8, column=1, padx=5, pady=10)
        self.buttonEditarVehiculo.grid(row=8, column=2, padx=5, pady=10)
        self.buttonCancelarVehiculo.grid(row=8, column=3, padx=5, pady=10)

        self.buttonGuardarVehiculo.config(state="disabled")
        self.buttonEditarVehiculo.config(state="disabled")
        self.buttonCancelarVehiculo.config(state="disabled")

    def load_clientes(self):
        """Cargar la lista de clientes en el combobox"""
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT cliente_id, nombre FROM clientes WHERE usuario_id = %s"
            cursor.execute(query, (self.parent.user_info['ID'],))
            clientes = cursor.fetchall()

            if clientes:
                self.combo_clientes['values'] = [f"{cliente[1]}" for cliente in clientes]
                self.combo_clientes.bind("<<ComboboxSelected>>", self.update_client_id)

            cursor.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error al cargar clientes", f"\nError: {e}")

    def update_client_id(self, event):
        """Actualizar el ID del cliente cuando se selecciona un nombre en el combobox"""
        cliente_nombre = self.combo_clientes.get()
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT cliente_id FROM clientes WHERE nombre = %s"
            cursor.execute(query, (cliente_nombre,))
            cliente = cursor.fetchone()

            if cliente:
                self.entry_client_id.config(state='normal')
                self.entry_client_id.delete(0, tk.END)
                self.entry_client_id.insert(0, cliente[0])
                self.entry_client_id.config(state='disabled')

            cursor.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error al actualizar ID del cliente", f"\nError: {e}")

    def search_vehicle(self):
        license_plate = self.entry_search_matricula.get()
        
        try:
            if license_plate == "":
                messagebox.showerror("Error", "Ingrese una matrícula para buscar")
                return

            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            
            query = """
                SELECT matricula, cliente_id, marca, modelo, color, km
                FROM vehiculos
                WHERE matricula = %s
            """
            cursor.execute(query, (license_plate,))
            vehicle = cursor.fetchone()


            if vehicle:
                self.entry_matricula.config(state="normal")
                self.entry_matricula.delete(0, tk.END)
                self.entry_matricula.insert(0, vehicle[0])

                client_id = vehicle[1]
                self.entry_client_id.config(state='normal')
                self.entry_client_id.delete(0, tk.END)
                self.entry_client_id.insert(0, client_id) 

                cursor.execute("SELECT nombre FROM clientes WHERE cliente_id = %s", (client_id,))
                client = cursor.fetchone()
                if client:
                    self.combo_clientes.set(client[0])  
                else:
                    self.combo_clientes.set("")  

                self.entry_marca.delete(0, tk.END)
                self.entry_marca.insert(0, vehicle[2])
                self.entry_modelo.delete(0, tk.END)
                self.entry_modelo.insert(0, vehicle[3])
                self.entry_color.delete(0, tk.END)
                self.entry_color.insert(0, vehicle[4])
                self.entry_km.delete(0, tk.END)
                self.entry_km.insert(0, vehicle[5])

                self.entry_matricula.config(state="disabled")
                self.buttonEditarVehiculo.config(state="normal")
                self.buttonCancelarVehiculo.config(state="normal")
                self.buttonGuardarVehiculo.config(state="disabled")

            else:
                messagebox.showerror("Error", "Vehículo no encontrado")

            cursor.close()
            con.close()
            
        except Exception as e:
            messagebox.showerror("Error de búsqueda de vehículo", f"\nError: {e}")



    def handle_vehicle_action(self, action):
        """Manejar acciones de Nuevo, Guardar, Editar, y Cancelar"""
        if action == "Nuevo":
            self.clear_entries()
            self.entry_matricula.config(state="normal")
            self.buttonGuardarVehiculo.config(state="normal")
            self.buttonCancelarVehiculo.config(state="normal")
            self.buttonEditarVehiculo.config(state="disabled")

        elif action == "Guardar":
            license_plate = self.entry_matricula.get()
            brand = self.entry_marca.get()
            model = self.entry_modelo.get()
            color = self.entry_color.get()
            km = self.entry_km.get()
            client_name = self.combo_clientes.get()  

            try:
                if not all([license_plate, brand, model, color, km, client_name]):
                    messagebox.showerror("Error", "Por favor, complete todos los campos.")
                    return

                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()

                cursor.execute("SELECT cliente_id FROM clientes WHERE nombre = %s", (client_name,))
                client_id = cursor.fetchone()

                if not client_id:
                    messagebox.showerror("Error", "Cliente no encontrado.")
                    return

                query = """
                    INSERT INTO vehiculos (matricula, cliente_id, marca, modelo, color, km)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (license_plate, client_id[0], brand, model, color, km))
                connection.commit()

                messagebox.showinfo("Éxito", "Vehículo guardado correctamente.")
                self.clear_entries()  

                cursor.close()
                con.close()
                
            except Exception as e:
                messagebox.showerror("Error al guardar vehículo", f"Error: {e}")


        elif action == "Editar":
            license_plate = self.entry_matricula.get()
            brand = self.entry_marca.get()
            model = self.entry_modelo.get()
            color = self.entry_color.get()
            km = self.entry_km.get()
            client_name = self.combo_clientes.get()  
            try:
                if not all([license_plate, brand, model, color, km, client_name]):
                    messagebox.showerror("Error", "Por favor, complete todos los campos.")
                    return

                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()

                cursor.execute("SELECT cliente_id FROM clientes WHERE nombre = %s", (client_name,))
                client_id = cursor.fetchone()

                if client_id is None:  
                    messagebox.showerror("Error", "Cliente no encontrado.")
                    return

                client_id = client_id[0]  
                query = """
                    UPDATE vehiculos
                    SET matricula = %s, cliente_id = %s, marca = %s, modelo = %s, color = %s, km = %s
                    WHERE matricula = %s
                """
                cursor.execute(query, (license_plate, client_id, brand, model, color, km, license_plate))
                connection.commit()

                messagebox.showinfo("Éxito", "Vehículo editado correctamente.")
                self.clear_entries()  

                cursor.close()
                con.close()
                
            except Exception as e:
                messagebox.showerror("Error al editar vehículo", f"Error: {e}")



        elif action == "Cancelar":
            self.clear_entries()
            self.buttonGuardarVehiculo.config(state="disabled")
            self.buttonEditarVehiculo.config(state="disabled")
            self.buttonCancelarVehiculo.config(state="disabled")

    def clear_entries(self):
        """Limpiar todos los campos de entrada"""
        self.entry_matricula.delete(0, tk.END)
        self.entry_client_id.config(state="normal")
        self.entry_client_id.delete(0, tk.END)
        self.entry_client_id.config(state="disabled")
        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_color.delete(0, tk.END)
        self.entry_km.delete(0, tk.END)
