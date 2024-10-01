import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import utilities.connection as dbconn

class RepairsFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        self.container = container
        self.client_ids = []  # Lista para almacenar los IDs de clientes
        self.piece_ids = []   # Lista para almacenar los IDs de piezas
        self.create_widgets()
        self.clear_entries()
        self.load_clients()  # Carga inicial de clientes
        self.load_pieces()   # Carga inicial de piezas

    def create_widgets(self):
        tk.Label(self, text="Buscar por Folio:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_folio = tk.Entry(self)
        self.entry_search_folio.grid(row=0, column=1, padx=5, pady=5)
        self.button_search = tk.Button(self, text="Buscar", command=self.search_by_folio)
        self.button_search.grid(row=0, column=2, padx=5, pady=5)
        
        tk.Label(self, text="Folio:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_folio = tk.Entry(self, state="disabled") 
        self.entry_folio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Cliente:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_clientes = ttk.Combobox(self, state="readonly")
        self.combo_clientes.bind("<<ComboboxSelected>>", self.load_client_vehicles)
        self.combo_clientes.grid(row=2, column=1, padx=5, pady=5)
        self.entry_client_id = tk.Entry(self, state="disabled")
        self.entry_client_id.grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self, text="Vehículo (Matrícula):").grid(row=3, column=0, padx=5, pady=5)
        self.combo_vehicles = ttk.Combobox(self, state="readonly")
        self.combo_vehicles.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Pieza:").grid(row=4, column=0, padx=5, pady=5)
        self.combo_piezas = ttk.Combobox(self, state="readonly")
        self.combo_piezas.bind("<<ComboboxSelected>>", self.load_piece_id)  
        self.combo_piezas.grid(row=4, column=1, padx=5, pady=5)
        self.entry_pieza_id = tk.Entry(self, state="disabled")
        self.entry_pieza_id.grid(row=4, column=2, padx=5, pady=5)

        tk.Label(self, text="Cantidad:").grid(row=4, column=3, padx=5, pady=5)
        self.entry_cantidad = tk.Entry(self)
        self.entry_cantidad.grid(row=4, column=4, padx=5, pady=5)

        tk.Label(self, text="Falla:").grid(row=5, column=0, padx=5, pady=5)
        self.entry_falla = tk.Entry(self)
        self.entry_falla.grid(row=5, column=1, padx=5, pady=5, columnspan=2, sticky="we")

        tk.Label(self, text="Fecha de entrada:").grid(row=6, column=0, padx=5, pady=5)
        self.entry_fecha_entrada = DateEntry(self)
        self.entry_fecha_entrada.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="Fecha de salida:").grid(row=6, column=2, padx=5, pady=5)
        self.entry_fecha_salida = DateEntry(self)
        self.entry_fecha_salida.grid(row=6, column=3, padx=5, pady=5)

        self.buttonNuevo = tk.Button(self, text="Nuevo", command=self.load_next_folio)
        self.buttonNuevo.grid(row=7, column=0, padx=5, pady=10)

        self.buttonGuardar = tk.Button(self, text="Guardar", command=self.create_new_record)
        self.buttonGuardar.grid(row=7, column=1, padx=5, pady=10)

        self.buttonEditar = tk.Button(self, text="Editar", command=self.edit_record)
        self.buttonEditar.grid(row=7, column=2, padx=5, pady=10)

        self.buttonCancelar = tk.Button(self, text="Cancelar", command=self.clear_entries)
        self.buttonCancelar.grid(row=7, column=3, padx=5, pady=10)

    def load_clients(self):
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = """
                SELECT DISTINCT c.cliente_id, c.nombre
                FROM clientes c
                JOIN vehiculos v ON c.cliente_id = v.cliente_id
            """
            cursor.execute(query)
            clientes = cursor.fetchall()
            if clientes:
                self.combo_clientes['values'] = [cliente[1] for cliente in clientes]
                self.client_ids = [cliente[0] for cliente in clientes]  # Almacenar IDs de clientes
            else:
                self.combo_clientes['values'] = ["No hay clientes con vehículos registrados"]

            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")

    def load_client_vehicles(self, event):
        try:
            selected_index = self.combo_clientes.current() 
            cliente_id = self.client_ids[selected_index]  
            self.entry_client_id.config(state="normal")
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_id.insert(0, cliente_id)
            self.entry_client_id.config(state="disabled")

            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT matricula FROM vehiculos WHERE cliente_id = %s"
            cursor.execute(query, (cliente_id,))
            vehiculos = cursor.fetchall()
            if vehiculos:
                self.combo_vehicles['values'] = [vehiculo[0] for vehiculo in vehiculos]
            else:
                self.combo_vehicles['values'] = ["No hay vehículos para este cliente"]
            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar vehículos: {str(e)}")

    def load_piece_id(self, event):
        try:
            selected_index = self.combo_piezas.current() 
            pieza_id = self.piece_ids[selected_index]  
            self.entry_pieza_id.config(state="normal")
            self.entry_pieza_id.delete(0, tk.END)
            self.entry_pieza_id.insert(0, pieza_id)
            self.entry_pieza_id.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el ID de la pieza: {str(e)}")

    def load_pieces(self):
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT id, descripcion FROM partes WHERE stock > 0"
            cursor.execute(query)
            piezas = cursor.fetchall()
            if piezas:
                self.combo_piezas['values'] = [pieza[1] for pieza in piezas]
                self.piece_ids = [pieza[0] for pieza in piezas] 
            else:
                self.combo_piezas['values'] = ["No hay piezas disponibles"]

            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar piezas: {str(e)}")    

    def load_next_folio(self):
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT MAX(folio) FROM reparaciones" 
            cursor.execute(query)
            next_folio = cursor.fetchone()[0] or 0  
            self.entry_folio.configure(state="normal")  
            self.entry_folio.delete(0, tk.END)
            self.entry_folio.insert(0, next_folio + 1)  
            self.entry_folio.configure(state="disabled")  
            cursor.close()
            connection.close()
            self.buttonNuevo.config(state="disable")
            self.buttonGuardar.config(state="normal")
            self.buttonEditar.config(state="disable")
            self.buttonCancelar.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar folios: {str(e)}")
            
    def search_by_folio(self):
        folio = self.entry_search_folio.get().strip()  
        if not folio:
            messagebox.showwarning("Advertencia", "Por favor ingresa un folio.")
            return
        
        try:
            if not folio.isdigit():
                raise ValueError("El folio debe ser un número")
            
            
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            
            query = """
                SELECT folio, cliente_id, vehiculo_matricula, pieza_id, cantidad, falla, fecha_entrada, fecha_salida
                FROM reparaciones
                WHERE folio = %s
            """
            cursor.execute(query, (folio,))
            record = cursor.fetchone()

            if record:
                
                self.entry_folio.configure(state="normal")
                self.entry_folio.delete(0, tk.END)
                self.entry_folio.insert(0, record[0])
                self.entry_folio.configure(state="disabled")

                cliente_id = record[1]
                pieza_id = record[3]

                cursor.execute("SELECT nombre FROM clientes WHERE cliente_id = %s", (cliente_id,))
                cliente_record = cursor.fetchone()
                cliente_nombre = cliente_record[0] if cliente_record else "Desconocido"
                
                self.entry_client_id.configure(state="normal")
                self.entry_client_id.delete(0, tk.END)
                self.entry_client_id.insert(0, record[1])
                self.entry_client_id.configure(state="disabled")

                cursor.execute("SELECT descripcion FROM partes WHERE id = %s", (pieza_id,))
                pieza_record = cursor.fetchone()
                pieza_descripcion = pieza_record[0] if pieza_record else "Desconocida"
                
                self.entry_pieza_id.config(state="normal")
                self.entry_pieza_id.delete(0, tk.END)

                self.entry_pieza_id.insert(0,record[3])
                self.entry_pieza_id.config(state="disable")

                self.combo_clientes.set(cliente_nombre)
                self.combo_piezas.set(pieza_descripcion)

                self.combo_vehicles.set(record[2])
                self.entry_cantidad.delete(0, tk.END)
                self.entry_cantidad.insert(0, record[4])
                self.entry_falla.delete(0, tk.END)
                self.entry_falla.insert(0, record[5])
                self.entry_fecha_entrada.set_date(record[6])
                self.entry_fecha_salida.set_date(record[7])
                self.buttonNuevo.config(state="disabled")
                self.buttonGuardar.config(state="disable")
                self.buttonEditar.config(state="normal")
                self.buttonCancelar.config(state="normal")
                self.combo_clientes.config(state="disable")
                self.combo_vehicles.config(state="disable")
                self.combo_piezas.config(state="disable")
                self.entry_fecha_entrada.config(state="disable")
                self.entry_falla.config(state="disabled")
                
                if self.parent.user_info['PERFIL'].lower() == 'mecanico':
                    self.buttonEditar.config(state="disabled")
            else:
                messagebox.showinfo("Información", "No se encontró el registro con el folio proporcionado.")

            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar el registro: {str(e)}")

            
    def create_new_record(self):
        try:
            folio_id = self.entry_folio.get()
            self.entry_client_id.config(state="normal")
            cliente_id = self.entry_client_id.get()  
            self.entry_client_id.config(state="disable")

            vehiculo_matricula = self.combo_vehicles.get()
            self.entry_pieza_id.config(state="normal")

            pieza_id = self.entry_pieza_id.get()  
            self.entry_pieza_id.config(state="disable")

            cantidad = self.entry_cantidad.get()
            falla = self.entry_falla.get()
            
            fecha_entrada = self.entry_fecha_entrada.get_date().strftime('%Y-%m-%d')
            fecha_salida = self.entry_fecha_salida.get_date().strftime('%Y-%m-%d')

            if not (folio_id and cliente_id and vehiculo_matricula and pieza_id and cantidad and falla and fecha_entrada and fecha_salida):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            try:
                cantidad = int(cantidad)
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser un número positivo.")
            except ValueError:
                messagebox.showwarning("Advertencia", "La cantidad debe ser un número válido.")
                return

            if fecha_salida <= fecha_entrada:
                messagebox.showwarning("Advertencia", "La fecha de salida debe ser mayor que la fecha de entrada.")
                return

            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            cursor.execute("SELECT stock FROM partes WHERE id = %s", (pieza_id,))
            stock_record = cursor.fetchone()

            if stock_record:
                stock = stock_record[0]
                if stock < cantidad:
                    messagebox.showwarning("Advertencia", f"No hay suficiente stock. Stock disponible: {stock}.")
                    return
            else:
                messagebox.showwarning("Advertencia", "No se encontró la pieza.")
                return

            query = """
                INSERT INTO reparaciones (folio, cliente_id, vehiculo_matricula, pieza_id, cantidad, falla, fecha_entrada, fecha_salida)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (folio_id, cliente_id, vehiculo_matricula, pieza_id, cantidad, falla, fecha_entrada, fecha_salida))
            
            new_stock = stock - cantidad
            cursor.execute("UPDATE partes SET stock = %s WHERE id = %s", (new_stock, pieza_id))
            
            connection.commit()

            messagebox.showinfo("Éxito", "Registro creado exitosamente.")

            self.clear_entries()

            cursor.close()
            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el registro: {str(e)}")
            
    def edit_record(self):
        try:
            folio_id = self.entry_folio.get()
            self.entry_client_id.config(state="normal")
            cliente_id = self.entry_client_id.get()  
            self.entry_client_id.config(state="disable")

            vehiculo_matricula = self.combo_vehicles.get()
            self.entry_pieza_id.config(state="normal")

            pieza_id = self.entry_pieza_id.get()  
            self.entry_pieza_id.config(state="disable")

            nueva_cantidad = self.entry_cantidad.get()
            falla = self.entry_falla.get()

            fecha_entrada = self.entry_fecha_entrada.get_date().strftime('%Y-%m-%d')
            fecha_salida = self.entry_fecha_salida.get_date().strftime('%Y-%m-%d')

            if not (folio_id and cliente_id and vehiculo_matricula and pieza_id and nueva_cantidad and falla and fecha_entrada and fecha_salida):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            try:
                nueva_cantidad = int(nueva_cantidad)
                if nueva_cantidad <= 0:
                    raise ValueError("La cantidad debe ser un número positivo.")
            except ValueError:
                messagebox.showwarning("Advertencia", "La cantidad debe ser un número válido.")
                return

            if fecha_salida <= fecha_entrada:
                messagebox.showwarning("Advertencia", "La fecha de salida debe ser mayor que la fecha de entrada.")
                return

            # Consultar el registro actual para obtener la cantidad anterior
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            cursor.execute("SELECT cantidad, pieza_id FROM reparaciones WHERE folio = %s", (folio_id,))
            registro_actual = cursor.fetchone()

            if registro_actual:
                cantidad_anterior = registro_actual[0]
                pieza_id_actual = registro_actual[1]

                # Calcular la diferencia de piezas
                diferencia = nueva_cantidad - cantidad_anterior
                
                # Consultar el stock disponible para la pieza
                cursor.execute("SELECT stock FROM partes WHERE id = %s", (pieza_id,))
                stock_record = cursor.fetchone()

                if stock_record:
                    stock = stock_record[0]
                    
                    # Validar stock solo si se aumenta la cantidad
                    if diferencia > 0 and stock < diferencia:
                        messagebox.showwarning("Advertencia", f"No hay suficiente stock. Stock disponible: {stock}.")
                        return
                    
                    nuevo_stock = stock - diferencia  # Restar si se aumenta, sumar si se disminuye
                    cursor.execute("UPDATE partes SET stock = %s WHERE id = %s", (nuevo_stock, pieza_id))
                else:
                    messagebox.showwarning("Advertencia", "No se encontró la pieza.")
                    return

                query = """
                    UPDATE reparaciones
                    SET cliente_id = %s, vehiculo_matricula = %s, pieza_id = %s, cantidad = %s, falla = %s, fecha_entrada = %s, fecha_salida = %s
                    WHERE folio = %s
                """
                cursor.execute(query, (cliente_id, vehiculo_matricula, pieza_id, nueva_cantidad, falla, fecha_entrada, fecha_salida, folio_id))
                connection.commit()
                
                messagebox.showinfo("Éxito", "Registro editado exitosamente.")

                self.clear_entries()
                

                cursor.close()
                connection.close()
            else:
                messagebox.showwarning("Advertencia", "No se encontró el registro a editar.")
                cursor.close()
                connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al editar el registro: {str(e)}")




    def clear_entries(self):
        self.combo_clientes.config(state="normal")
        self.combo_vehicles.config(state="normal")
        self.combo_piezas.config(state="normal")
        self.entry_fecha_entrada.config(state="normal")
        self.entry_falla.config(state="normal")
        self.buttonNuevo.config(state="normal")
        self.buttonGuardar.config(state="disable")
        self.buttonEditar.config(state="disable")
        self.buttonCancelar.config(state="disable")
        self.entry_folio.config(state="normal")
        self.entry_folio.delete(0, tk.END)
        self.entry_folio.config(state="disable")
        self.entry_search_folio.delete(0, tk.END)
        self.combo_clientes.set('')
        self.entry_client_id.config(state='normal')
        self.entry_client_id.delete(0, tk.END)
        self.entry_client_id.config(state='disabled')
        self.combo_vehicles.set('')
        self.combo_piezas.set('')
        self.entry_pieza_id.config(state='normal')
        self.entry_pieza_id.delete(0, tk.END)
        self.entry_pieza_id.config(state='disabled')
        self.entry_cantidad.delete(0, tk.END)
        self.entry_falla.delete(0, tk.END)
        
        today = datetime.today().date()
        self.entry_fecha_entrada.set_date(today)
        self.entry_fecha_salida.set_date(today)