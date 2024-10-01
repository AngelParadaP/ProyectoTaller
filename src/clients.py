import tkinter as tk
import utilities.connection as dbconn
from tkinter import messagebox

class ClientsFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent 
        #PARA ACCEDER A LA INFO DE USUARIO USAR self.parent.user_info['AQUI VA EL CAMPO']
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self)
        frame.pack(pady=20, padx=20)

        # Ingreso del ID del cliente a buscar
        tk.Label(frame, text="Ingrese ID del cliente a buscar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search_client_id = tk.Entry(frame)
        self.entry_search_client_id.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Buscar", command=lambda: self.search_client()).grid(row=0, column=2, padx=5, pady=5)

        # Muestra del ID del usuario que registró o va a registrar
        tk.Label(frame, text="Usuario ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_user_id = tk.Entry(frame)
        self.entry_user_id.config(state='disabled')
        self.entry_user_id.grid(row=1, column=1, padx=5, pady=5)

        # Mostrar el username del usuario que registró o va a registrar
        tk.Label(frame, text="Usuario que registró:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = tk.Entry(frame)
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

        # Posicionamiento de los botones
        self.buttonNuevoCliente.grid(row=6, column=0, padx=5, pady=10)
        self.buttonGuardarCliente.grid(row=6, column=1, padx=5, pady=10)
        self.buttonEditarCliente.grid(row=6, column=2, padx=5, pady=10)
        self.buttonCancelarCliente.grid(row=6, column=3, padx=5, pady=10)

        # Desactivar botones de edición inicialmente
        self.buttonGuardarCliente.config(state="disabled")
        self.buttonEditarCliente.config(state="disabled")
        self.buttonCancelarCliente.config(state="disabled")
    
    def search_client(self):
        client_id = self.entry_search_client_id.get()
        try:
            if client_id == "":
                messagebox.showerror("Error", "Ingrese un ID para buscar")
                return
            
            if not client_id.isdigit():
                raise ValueError("El ID debe ser un número")

            
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT * FROM clientes INNER JOIN usuarios ON clientes.usuario_id = usuarios.usuario_id WHERE cliente_id = %s"
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
                
                self.entry_user_id.config(state="normal")
                self.entry_user_id.delete(0, tk.END)
                self.entry_user_id.insert(0, client[4])
                self.entry_user_id.config(state="disabled")
                
                self.entry_username.config(state="normal")
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, client[6])
                self.entry_username.config(state="disabled")
                
                if self.parent.user_info['PERFIL'].lower() == "admin":
                    self.buttonEditarCliente.config(state="normal")
                self.buttonCancelarCliente.config(state="normal")
                self.buttonGuardarCliente.config(state="disabled")
                self.entry_client_id.config(state="disabled")
                self.entry_client_name.config(state="normal")
                self.entry_client_phone.config(state="normal")

            else:
                messagebox.showerror("Error", "Cliente no encontrado")

            cursor.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Error de busqueda de cliente", f"Error: {e}")

    def handle_client_action(self, action):
        if action == "Nuevo":
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            query = "SELECT MAX(cliente_id) FROM clientes"
            cursor.execute(query)
            result = cursor.fetchone()
            next_id = result[0] + 1 if result[0] is not None else 1
            
            self.entry_user_id.config(state="normal")
            self.entry_user_id.delete(0, tk.END)
            self.entry_user_id.insert(0, self.parent.user_info['ID'])
            self.entry_user_id.config(state="disabled")
            
            self.entry_username.config(state="normal")
            self.entry_username.delete(0, tk.END)
            self.entry_username.insert(0, self.parent.user_info['USERNAME'])
            self.entry_username.config(state="disabled")
            
            self.entry_client_id.config(state="normal")
            self.entry_client_name.config(state="normal")
            self.entry_client_phone.config(state="normal")
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_id.insert(0, str(next_id))
            self.entry_client_name.delete(0, tk.END)
            self.entry_client_phone.delete(0, tk.END)
            self.entry_client_id.config(state="disabled")
            self.buttonGuardarCliente.config(state="normal")
            self.buttonCancelarCliente.config(state="normal")
            self.buttonEditarCliente.config(state="disabled")

        elif action == "Guardar":
                # No necesitas obtener client_id ya que es SERIAL
                user_id = self.parent.user_info['ID']
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
                    messagebox.showerror("Error de guardado de cliente", f"\nError: {e}")


        elif action == "Editar":
            client_id = self.entry_client_id.get()
            client_name = self.entry_client_name.get()
            client_phone = self.entry_client_phone.get()
                
            if not client_name or not client_phone:
                messagebox.showerror("Error", "Los campos de nombre y telefono deben ser llenados")
                return

            try:
                con = dbconn.connection()
                connection = con.open()
                cursor = connection.cursor()
                update_query = "UPDATE clientes SET nombre = %s, telefono = %s"
                params = [client_name, client_phone]
                update_query += " WHERE cliente_id = %s"
                params.append(client_id)

                cursor.execute(update_query, tuple(params))
                connection.commit()

                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                self.handle_client_action("Cancelar")
                
                cursor.close()
                con.close()

            except Exception as e:
                messagebox.showerror("Error de edicion de cliente", f"\nError: {e}")


        elif action == "Cancelar":
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_name.delete(0, tk.END)
            self.entry_client_phone.delete(0, tk.END)
            
            self.entry_user_id.config(state="normal")
            self.entry_user_id.delete(0, tk.END)
            self.entry_user_id.config(state="disabled")
            
            self.entry_username.config(state="normal")
            self.entry_username.delete(0, tk.END)
            self.entry_username.config(state="disabled")

            self.entry_client_id.config(state="normal")
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_id.config(state="disabled")
            
            self.buttonGuardarCliente.config(state="disabled")
            self.buttonEditarCliente.config(state="disabled")
            self.buttonCancelarCliente.config(state="disabled")