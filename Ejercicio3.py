
# -*- coding: utf-8 -*-
"""
VentanaContacto en Python con Tkinter.
- Nombres, Apellidos (Entry)
- Fecha de nacimiento (DatePicker propio)
- Dirección, Teléfono, Correo (Entry)
- Botón "Agregar" → valida, guarda en ListaContactos y muestra en Listbox (lista inferior)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from typing import Optional, List
import calendar


class Contacto:
    
    def __init__(self, nombres: str, apellidos: str, fechaNacimiento: date,
                 direccion: str, telefono: str, correo: str):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fechaNacimiento = fechaNacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

    def toString(self) -> str:
        # Formato similar al JavaFX: a-b-c-d-e-f
        return f"{self.nombres} - {self.apellidos} - {self.fechaNacimiento.strftime('%Y-%m-%d')} - {self.direccion} - {self.telefono} - {self.correo}"


class ListaContactos:
 
    def __init__(self):
        self.lista: List[Contacto] = []

    def agregarContacto(self, contacto: Contacto):
        self.lista.append(contacto)

    def obtenerTodos(self) -> List[Contacto]:
        return list(self.lista)


class DatePicker(tk.Frame):
    """
    DatePicker simple hecho en Tkinter:
    - Botón que muestra una ventana con un calendario.
    - Navega meses y selecciona día.
    - Entry muestra la fecha en formato YYYY-MM-DD.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.selectedDate: Optional[date] = None

        self.entryVar = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entryVar)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.btn = tk.Button(self, text="📅", command=self._openCalendar)
        self.btn.grid(row=0, column=1, padx=4)
        self.columnconfigure(0, weight=1)

    def _openCalendar(self):
        top = tk.Toplevel(self)
        top.title("Seleccionar fecha")
        top.resizable(False, False)

        now = self.selectedDate or date.today()
        self._calYear = now.year
        self._calMonth = now.month

        header = tk.Frame(top, padx=6, pady=6)
        header.pack(fill="x")
        self.lblTitle = tk.Label(header, text="", font=("Segoe UI", 10, "bold"))
        self.lblTitle.pack(side="left", padx=6)
        tk.Button(header, text="◀", command=lambda: self._shiftMonth(-1, top)).pack(side="right")
        tk.Button(header, text="▶", command=lambda: self._shiftMonth(+1, top)).pack(side="right")

        body = tk.Frame(top, padx=6, pady=6)
        body.pack(fill="both")
        weekdays = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
        for j, wd in enumerate(weekdays):
            tk.Label(body, text=wd, font=("Segoe UI", 9, "bold")).grid(row=0, column=j, padx=3, pady=3)

        self._body = body
        self._renderMonth(top)

    def _shiftMonth(self, delta: int, top: tk.Toplevel):
        m = self._calMonth + delta
        y = self._calYear
        if m < 1:
            m = 12; y -= 1
        elif m > 12:
            m = 1; y += 1
        self._calMonth = m
        self._calYear = y
        self._renderMonth(top)

    def _renderMonth(self, top: tk.Toplevel):
        monthName = calendar.month_name[self._calMonth]
        self.lblTitle.config(text=f"{monthName} {self._calYear}")

        # Limpia filas de días, conserva encabezado (row 0)
        for w in self._body.grid_slaves():
            info = w.grid_info()
            if info["row"] != 0:
                w.destroy()

        cal = calendar.Calendar(firstweekday=0)
        row = 1
        for week in cal.monthdayscalendar(self._calYear, self._calMonth):
            col = 0
            for day in week:
                if day == 0:
                    tk.Label(self._body, text="").grid(row=row, column=col, padx=3, pady=3)
                else:
                    d = date(self._calYear, self._calMonth, day)
                    tk.Button(self._body, text=str(day), width=3,
                              command=lambda dd=d, t=top: self._selectDate(dd, t)).grid(row=row, column=col, padx=2, pady=2)
                col += 1
            row += 1

    def _selectDate(self, d: date, top: tk.Toplevel):
        self.selectedDate = d
        self.entryVar.set(d.strftime("%Y-%m-%d"))
        top.destroy()

    def getValue(self) -> Optional[date]:
        txt = (self.entryVar.get() or "").strip()
        if not txt:
            return None
        try:
            return datetime.strptime(txt, "%Y-%m-%d").date()
        except Exception:
            return None

    def setValue(self, d: Optional[date]):
        self.selectedDate = d
        self.entryVar.set("" if d is None else d.strftime("%Y-%m-%d"))



class VentanaContacto(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Detalles del contacto")
        self.geometry("600x330")
        self.resizable(False, False)

        self.listaContactos = ListaContactos()

        # Frame principal (simula GridPane con borde estilo CSS)
        grid = tk.Frame(self, bd=2, relief="solid")
        grid.pack(fill="both", expand=True, padx=10, pady=10)

        # Etiquetas
        tk.Label(grid, text="Nombres:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        tk.Label(grid, text="Apellidos:").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        tk.Label(grid, text="Fecha nacimiento:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        tk.Label(grid, text="Dirección").grid(row=3, column=0, sticky="w", padx=6, pady=6)
        tk.Label(grid, text="Correo").grid(row=4, column=0, sticky="w", padx=6, pady=6)
        tk.Label(grid, text="Teléfono").grid(row=5, column=0, sticky="w", padx=6, pady=6)

        # Campos
        self.campoNombres = tk.Entry(grid)
        self.campoApellidos = tk.Entry(grid)
        self.campoFechaNacimiento = DatePicker(grid)
        self.campoDireccion = tk.Entry(grid)
        self.campoCorreo = tk.Entry(grid)
        self.campoTelefono = tk.Entry(grid)

        self.campoNombres.grid(row=0, column=1, sticky="ew", padx=6, pady=6)
        self.campoApellidos.grid(row=1, column=1, sticky="ew", padx=6, pady=6)
        self.campoFechaNacimiento.grid(row=2, column=1, sticky="ew", padx=6, pady=6)
        self.campoDireccion.grid(row=3, column=1, sticky="ew", padx=6, pady=6)
        self.campoCorreo.grid(row=4, column=1, sticky="ew", padx=6, pady=6)
        self.campoTelefono.grid(row=5, column=1, sticky="ew", padx=6, pady=6)

        # Botón Agregar
        agregar = tk.Button(grid, text="Agregar", bg="#ff6a13", fg="white", command=self.mostrarDatos)
        agregar.grid(row=6, column=1, sticky="e", padx=6, pady=8)

        grid.columnconfigure(1, weight=1)

        # ListView inferior (Listbox + Scrollbar)
        bottom = tk.Frame(self, padx=10, pady=6)
        bottom.pack(fill="both", expand=True)
        tk.Label(bottom, text="Contactos agregados:").pack(anchor="w")

        listFrame = tk.Frame(bottom)
        listFrame.pack(fill="both", expand=True)
        self.listaVisual = tk.Listbox(listFrame, height=6)
        scrollY = tk.Scrollbar(listFrame, orient="vertical", command=self.listaVisual.yview)
        self.listaVisual.configure(yscrollcommand=scrollY.set)

        self.listaVisual.pack(side="left", fill="both", expand=True)
        scrollY.pack(side="right", fill="y")

    def mostrarDatos(self):
     
        a = self.campoNombres.get().strip()
        b = self.campoApellidos.get().strip()
        c = self.campoFechaNacimiento.getValue()
        d = self.campoDireccion.get().strip()
        e = self.campoTelefono.get().strip()
        f = self.campoCorreo.get().strip()

        # Validaciones
        if a == "" or b == "" or d == "" or e == "" or f == "":
            messagebox.showinfo("Mensaje", "Error en ingreso de datos\nNo se permiten campos vacíos", parent=self)
            return
        if c is None:
            messagebox.showinfo("Mensaje", "Error en ingreso de datos\nSeleccione una fecha válida (YYYY-MM-DD).", parent=self)
            return

        # Crear y guardar
        contacto = Contacto(a, b, c, d, e, f)
        self.listaContactos.agregarContacto(contacto)

        # Añadir a lista visual
        self.listaVisual.insert(tk.END, contacto.toString())

        # Limpiar campos
        self.campoNombres.delete(0, tk.END)
        self.campoApellidos.delete(0, tk.END)
        self.campoFechaNacimiento.setValue(None)
        self.campoDireccion.delete(0, tk.END)
        self.campoTelefono.delete(0, tk.END)
        self.campoCorreo.delete(0, tk.END)



class Principal:
    @staticmethod
    def main():
        app = VentanaContacto()
        app.mainloop()


if __name__ == "__main__":
    Principal.main()
