import tkinter as tk
from tkinter import messagebox
import utilities.connection as dbconn

class PiecesFrame(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.parent = parent
        
        # Etiquetas y campos de entrada
        tk.Label(self, text="Buscar por ID:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_search = tk.Entry(self)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)
        
        self.button_search = tk.Button(self, text="Buscar", command=self.search_piece)
        self.button_search.grid(row=0, column=2, padx=10, pady=10)
        
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self, state="disabled")  # Campo de ID, solo de lectura
        self.entry_id.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Descripción:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_description = tk.Entry(self)
        self.entry_description.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Stock:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_stock = tk.Entry(self)
        self.entry_stock.grid(row=3, column=1, padx=10, pady=10)
        self.entry_stock.bind("<KeyRelease>", self.validate_stock_entry)
        
        # Botones
        self.button_new = tk.Button(self, text="Nuevo", command=self.new_piece)
        self.button_new.grid(row=4, column=0, padx=10, pady=10)
        
        self.button_save = tk.Button(self, text="Guardar", command=self.save_piece)
        self.button_save.grid(row=4, column=1, padx=10, pady=10)
        self.button_save.config(state="disabled")  # Solo habilitado al hacer "Nuevo"
        
        self.button_edit = tk.Button(self, text="Editar", command=self.edit_piece)
        self.button_edit.grid(row=5, column=0, padx=10, pady=10)
        self.button_edit.config(state="disabled")
        
        self.button_cancel = tk.Button(self, text="Cancelar", command=self.clear_entries)
        self.button_cancel.grid(row=5, column=1, padx=10, pady=10)
        
        self.button_remove = tk.Button(self, text="Eliminar", command=self.remove_piece)
        self.button_remove.grid(row=6, column=0, padx=10, pady=10)
        self.button_remove.config(state="disabled")
        
    def validate_stock_entry(self, event):
        stock_value = self.entry_stock.get()
        if not stock_value.isdigit():
            messagebox.showerror("Error", "El stock debe ser un número entero positivo.")
            self.entry_stock.delete(0, tk.END)
    
    def new_piece(self):
        self.clear_entries()
        
        try:
            # Obtener el siguiente ID disponible
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM partes")
            next_id = cursor.fetchone()[0]
            cursor.close()
            con.close()
            
            self.entry_id.config(state="normal")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, next_id)
            self.entry_id.config(state="disabled")
            
            self.entry_description.config(state="normal")
            self.entry_stock.config(state="normal")
            self.button_save.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar nuevo ID: {e}")
    
    def save_piece(self):
        """Guardar la nueva pieza en la base de datos, validando los datos."""
        description = self.entry_description.get().strip()
        stock = self.entry_stock.get().strip()
        
        # Validar que los campos no estén vacíos y que el stock no sea negativo
        if not description or not stock:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        if int(stock) < 0:
            messagebox.showerror("Error", "El stock no puede ser negativo.")
            return
        
        try:
            # Validar que no exista una pieza con la misma descripción
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM partes WHERE descripcion = %s", (description,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Ya existe una pieza con esta descripción.")
                cursor.close()
                con.close()
                return
            
            # Insertar nueva pieza
            cursor.execute("INSERT INTO partes (descripcion, stock) VALUES (%s, %s)", (description, stock))
            connection.commit()
            cursor.close()
            con.close()
            
            messagebox.showinfo("Éxito", "Pieza guardada correctamente.")
            self.clear_entries()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la pieza: {e}")
    
    def edit_piece(self):
        description = self.entry_description.get().strip()
        stock = self.entry_stock.get().strip()
        piece_id = self.entry_id.get()
        
        if not description or not stock:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        if int(stock) < 0:
            messagebox.showerror("Error", "El stock no puede ser negativo.")
            return
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            
            cursor.execute(
                "UPDATE partes SET descripcion = %s, stock = %s WHERE id = %s",
                (description, stock, piece_id)
            )
            connection.commit()
            cursor.close()
            con.close()
            
            messagebox.showinfo("Éxito", "Pieza editada correctamente.")
            self.clear_entries()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al editar la pieza: {e}")
    
    def remove_piece(self):
        piece_id = self.entry_id.get()
        
        if not piece_id:
            messagebox.showerror("Error", "Seleccione una pieza para eliminar.")
            return
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            
            cursor.execute("DELETE FROM partes WHERE id = %s", (piece_id,))
            connection.commit()
            cursor.close()
            con.close()
            
            messagebox.showinfo("Éxito", "Pieza eliminada correctamente.")
            self.clear_entries()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la pieza: {e}")
    
    def search_piece(self):
        piece_id = self.entry_search.get().strip()
        
        if not piece_id.isdigit():
            messagebox.showerror("Error", "El ID de la pieza debe ser un número.")
            return
        
        try:
            con = dbconn.connection()
            connection = con.open()
            cursor = connection.cursor()
            
            cursor.execute("SELECT id, descripcion, stock FROM partes WHERE id = %s", (piece_id,))
            piece = cursor.fetchone()
            
            if piece:
                self.entry_id.config(state="normal")
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, piece[0])
                self.entry_id.config(state="disabled")
                
                self.entry_description.delete(0, tk.END)
                self.entry_description.insert(0, piece[1])
                
                self.entry_stock.delete(0, tk.END)
                self.entry_stock.insert(0, piece[2])
                
                self.button_edit.config(state="normal")
                self.button_remove.config(state="normal")
                self.button_save.config(state="disabled")
            else:
                messagebox.showerror("Error", "Pieza no encontrada.")
            
            cursor.close()
            con.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar la pieza: {e}")
    
    def clear_entries(self):
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state="disabled")
        
        self.entry_description.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        
        self.button_save.config(state="disabled")
        self.button_edit.config(state="disabled")
        self.button_remove.config(state="disabled")
