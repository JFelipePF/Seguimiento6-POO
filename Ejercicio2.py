
# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
from typing import Optional



class Huesped:

    def __init__(self, nombres: str, apellidos: str, documentoIdentidad: int):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documentoIdentidad = documentoIdentidad
        self.fechaIngreso: Optional[date] = None
        self.fechaSalida: Optional[date] = None

    def setFechaIngreso(self, fecha: date):
        self.fechaIngreso = fecha

    def setFechaSalida(self, fecha: date):
        self.fechaSalida = fecha

    def getFechaIngreso(self) -> Optional[date]:
        return self.fechaIngreso

    def obtenerDiasAlojamiento(self) -> int:
        """
        Equivalente a (fechaSalida.getTime() - fechaIngreso.getTime())/86400000 en Java.
        """
        if self.fechaIngreso is None or self.fechaSalida is None:
            return 0
        return (self.fechaSalida - self.fechaIngreso).days


class Habitacion:

    def __init__(self, numeroHabitacion: int, disponible: bool, precioDia: float):
        self.numeroHabitacion = numeroHabitacion
        self.disponible = disponible
        self.precioDia = precioDia
        self.huesped: Optional[Huesped] = None

    # --- GETTERS (como en Java) ---
    def getNumeroHabitacion(self) -> int:
        return self.numeroHabitacion

    def getDisponible(self) -> bool:
        return self.disponible

    def getPrecioDia(self) -> float:
        return self.precioDia

    def getHuesped(self) -> Optional[Huesped]:
        return self.huesped

    # --- SETTERS ---
    def setHuesped(self, huesped: Optional[Huesped]):
        self.huesped = huesped

    def setDisponible(self, disponible: bool):
        self.disponible = disponible


class Hotel:


    def __init__(self):
        self.listaHabitaciones: list[Habitacion] = []
        # Crear 10 habitaciones con disponibilidad True y sus precios
        for n in range(1, 11):
            precio = 120_000 if n <= 5 else 160_000
            self.listaHabitaciones.append(Habitacion(n, True, precio))

    def buscarFechaIngresoHabitacion(self, numero: int) -> str:
      
        for hab in self.listaHabitaciones:
            if hab.getNumeroHabitacion() == numero:
                hue = hab.getHuesped()
                if hue and hue.getFechaIngreso():
                    fecha = hue.getFechaIngreso()
                    return fecha.strftime("%Y/%m/%d")
        return ""

    def buscarHabitacionOcupada(self, numero: int) -> bool:
       
        for hab in self.listaHabitaciones:
            if hab.getNumeroHabitacion() == numero and not hab.getDisponible():
                return True
        return False

    def getHabitacion(self, numero: int) -> Habitacion:
        if numero < 1 or numero > 10:
            raise ValueError("El número de habitación debe estar entre 1 y 10.")
        return self.listaHabitaciones[numero - 1]



class VentanaHabitaciones(tk.Toplevel):


    def __init__(self, hotel: Hotel, master=None):
        super().__init__(master)
        self.hotel = hotel
        self.title("Habitaciones")
        self.geometry("760x260")
        self.resizable(False, False)

        # contenedor con layout absoluto (como setLayout(null) + setBounds)
        self.contenedor = tk.Frame(self)
        self.contenedor.place(x=0, y=0, relwidth=1, relheight=1)

        self._build()

    def _build(self):
        # Posiciones para etiquetas (como en Java)
        posiciones = [
            (20, 30), (160, 30), (300, 30), (440, 30), (580, 30),
            (20, 120), (160, 120), (300, 120), (440, 120), (580, 120)
        ]
        posDisp = [
            (20, 50), (160, 50), (300, 50), (440, 50), (580, 50),
            (20, 140), (160, 140), (300, 140), (440, 140), (580, 140)
        ]

        self.labelsHab = []
        self.labelsDisp = []

        for i in range(10):
            num = i + 1
            lblHab = tk.Label(self.contenedor, text=f"Habitación {num}")
            x, y = posiciones[i]
            lblHab.place(x=x, y=y, width=130, height=23)
            self.labelsHab.append(lblHab)

            habObj = self.hotel.listaHabitaciones[i]
            estado = "Disponible" if habObj.getDisponible() else "No disponible"
            lblDisp = tk.Label(self.contenedor, text=estado)
            xd, yd = posDisp[i]
            lblDisp.place(x=xd, y=yd, width=100, height=23)
            self.labelsDisp.append(lblDisp)

        # Selector y botón
        self.habitacionSeleccionada = tk.Label(self.contenedor, text="Habitación a reservar:")
        self.habitacionSeleccionada.place(x=250, y=180, width=135, height=23)

        self.campoHabitacionSeleccionadaVar = tk.StringVar(value="1")
        self.campoHabitacionSeleccionada = tk.Spinbox(
            self.contenedor, from_=1, to=10, textvariable=self.campoHabitacionSeleccionadaVar, width=5
        )
        self.campoHabitacionSeleccionada.place(x=380, y=180, width=40, height=23)

        self.botonAceptar = tk.Button(self.contenedor, text="Aceptar", command=self._onAceptar)
        self.botonAceptar.place(x=500, y=180, width=100, height=23)

    def _onAceptar(self):
        try:
            numero = int(self.campoHabitacionSeleccionadaVar.get())
            if not self.hotel.buscarHabitacionOcupada(numero):
                # Cierra esta y abre Ingreso
                self.withdraw()
                VentanaIngreso(self.hotel, numero, master=self.master)
            else:
                messagebox.showinfo("Mensaje", "La habitación está ocupada", parent=self)
        except Exception:
            messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)


class VentanaIngreso(tk.Toplevel):


    def __init__(self, hotel: Hotel, numeroHabitacionReservada: int, master=None):
        super().__init__(master)
        self.hotel = hotel
        self.numeroHabitacionReservada = numeroHabitacionReservada
        self.title("Ingreso")
        self.geometry("290x250")
        self.resizable(False, False)
        self._build()

    def _build(self):
        contenedor = tk.Frame(self)
        contenedor.grid(column=0, row=0, padx=6, pady=6, sticky="nsew")

        # Etiqueta habitación
        self.lblHabitacion = tk.Label(contenedor, text=f"Habitación: {self.numeroHabitacionReservada}")
        self.lblHabitacion.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        # Fecha ingreso
        self.lblFechaIngreso = tk.Label(contenedor, text="Fecha (aaaa-mm-dd):")
        self.lblFechaIngreso.grid(row=1, column=0, padx=3, pady=3, sticky="w")
        self.campoFechaIngreso = tk.Entry(contenedor)
        self.campoFechaIngreso.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

        # Huésped
        self.lblHuesped = tk.Label(contenedor, text="Huésped")
        self.lblHuesped.grid(row=2, column=0, padx=3, pady=3, sticky="w")

        # Nombre
        self.lblNombre = tk.Label(contenedor, text="Nombre:")
        self.lblNombre.grid(row=3, column=0, padx=3, pady=3, sticky="w")
        self.campoNombre = tk.Entry(contenedor)
        self.campoNombre.grid(row=3, column=1, padx=3, pady=3, sticky="ew")

        # Apellidos
        self.lblApellidos = tk.Label(contenedor, text="Apellidos:")
        self.lblApellidos.grid(row=4, column=0, padx=3, pady=3, sticky="w")
        self.campoApellidos = tk.Entry(contenedor)
        self.campoApellidos.grid(row=4, column=1, padx=3, pady=3, sticky="ew")

        # Documento
        self.lblDocumento = tk.Label(contenedor, text="Doc. Identidad:")
        self.lblDocumento.grid(row=5, column=0, padx=3, pady=3, sticky="w")
        self.campoDocumentoIdentidad = tk.Entry(contenedor)
        self.campoDocumentoIdentidad.grid(row=5, column=1, padx=3, pady=3, sticky="ew")

        # Botones
        self.btnAceptar = tk.Button(contenedor, text="Aceptar", command=self._onAceptar)
        self.btnAceptar.grid(row=6, column=0, padx=3, pady=3, sticky="ew")

        self.btnCancelar = tk.Button(contenedor, text="Cancelar", command=self._onCancelar)
        self.btnCancelar.grid(row=6, column=1, padx=3, pady=3, sticky="ew")

        contenedor.columnconfigure(1, weight=1)

    def _onAceptar(self):
        posicion = -1
        for i, hab in enumerate(self.hotel.listaHabitaciones):
            if hab.getNumeroHabitacion() == self.numeroHabitacionReservada:
                posicion = i
                try:
                    # Fecha
                    fechaIngresada = self.campoFechaIngreso.get().strip()
                    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()

                    # Huesped
                    nombres = self.campoNombre.get().strip()
                    apellidos = self.campoApellidos.get().strip()
                    docTxt = self.campoDocumentoIdentidad.get().strip()
                    if not nombres or not apellidos or not docTxt:
                        # En Java se usa un mensaje genérico
                        raise Exception("Campos obligatorios vacíos")
                    documento = int(docTxt)

                    huesped = Huesped(nombres, apellidos, documento)
                    huesped.setFechaIngreso(fecha)

                    hab.setHuesped(huesped)
                    hab.setDisponible(False)

                    # Actualiza lista
                    self.hotel.listaHabitaciones[posicion] = hab

                    messagebox.showinfo("Mensaje", "El huésped ha sido registrado", parent=self)
                    self.withdraw()
                    break

                except ValueError as ve:
                    # Error al convertir fecha o documento
                    if "unconverted data" in str(ve) or "does not match format" in str(ve):
                        messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado", parent=self)
                    else:
                        messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)
                except Exception:
                    messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)
                break

    def _onCancelar(self):
        self.withdraw()


class VentanaSalida(tk.Toplevel):


    def __init__(self, hotel: Hotel, numero: int, master=None):
        super().__init__(master)
        self.hotel = hotel
        self.numeroHabitacion = numero
        self.posicionHabitacion = -1
        self.habitacionOcupada: Optional[Habitacion] = None

        self.title("Salida huéspedes")
        self.geometry("260x260")
        self.resizable(False, False)
        self._build()

    def _build(self):
        contenedor = tk.Frame(self)
        contenedor.grid(column=0, row=0, padx=6, pady=6, sticky="nsew")

        # Habitación
        self.lblHabitacion = tk.Label(contenedor, text=f"Habitación: {self.numeroHabitacion}")
        self.lblHabitacion.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        # Fecha de ingreso (consulta desde Hotel)
        fecha = self.hotel.buscarFechaIngresoHabitacion(self.numeroHabitacion)
        self.lblFechaIngreso = tk.Label(contenedor, text=f"Fecha de ingreso: {fecha}")
        self.lblFechaIngreso.grid(row=1, column=0, padx=3, pady=3, sticky="w")

        # Fecha de salida
        self.lblFechaSalida = tk.Label(contenedor, text="Fecha de salida (aaaa-mm-dd): ")
        self.lblFechaSalida.grid(row=2, column=0, padx=3, pady=3, sticky="w")

        self.campoFechaSalida = tk.Entry(contenedor)
        self.campoFechaSalida.grid(row=3, column=0, padx=3, pady=3, sticky="ew")

        # Calcular
        self.btnCalcular = tk.Button(contenedor, text="Calcular", command=self._onCalcular)
        self.btnCalcular.grid(row=4, column=0, padx=3, pady=3, sticky="ew")

        # Cantidad de días
        self.cantidadDias = tk.Label(contenedor, text="Cantidad de días: ")
        self.cantidadDias.grid(row=5, column=0, padx=3, pady=3, sticky="w")

        # Total
        self.totalPago = tk.Label(contenedor, text="Total: $")
        self.totalPago.grid(row=6, column=0, padx=3, pady=3, sticky="w")

        # Registrar salida (deshabilitado al inicio)
        self.btnRegistrarSalida = tk.Button(
            contenedor, text="RegistrarSalida", state="disabled", command=self._onRegistrarSalida
        )
        self.btnRegistrarSalida.grid(row=7, column=0, padx=3, pady=3, sticky="ew")

        contenedor.columnconfigure(0, weight=1)

    def _onCalcular(self):
        try:
            fechaS_txt = self.campoFechaSalida.get().strip()
            fechaS = datetime.strptime(fechaS_txt, "%Y-%m-%d").date()

            # Buscar habitación por número
            for i, hab in enumerate(self.hotel.listaHabitaciones):
                if hab.getNumeroHabitacion() == self.numeroHabitacion:
                    self.posicionHabitacion = i
                    self.habitacionOcupada = hab
                    break

            if not self.habitacionOcupada or not self.habitacionOcupada.getHuesped():
                raise ValueError("La habitación no tiene huésped.")

            # Establecer fecha salida en huesped
            huesped = self.habitacionOcupada.getHuesped()
            fechaI = huesped.getFechaIngreso()
            if fechaI is None:
                raise ValueError("No hay fecha de ingreso registrada.")

            # Validación fecha salida > fecha ingreso
            if fechaI >= fechaS:
                messagebox.showerror("Mensaje", "La fecha de salida es menor que la de ingreso", parent=self)
                return

            # Set fecha salida y calcular
            huesped.setFechaSalida(fechaS)
            cantidad = huesped.obtenerDiasAlojamiento()
            self.cantidadDias.config(text=f"Cantidad de días: {cantidad}")
            valor = cantidad * self.habitacionOcupada.getPrecioDia()
            self.totalPago.config(text=f"Total: ${valor:,.0f}")

            # Habilitar registrar salida
            self.btnRegistrarSalida.config(state="normal")

        except ValueError as ve:
            if "time data" in str(ve) or "does not match format" in str(ve):
                messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado", parent=self)
            else:
                messagebox.showerror("Error", str(ve), parent=self)
        except Exception:
            messagebox.showerror("Error", "La fecha no está en el formato solicitado", parent=self)

    def _onRegistrarSalida(self):
        # Liberar habitación
        if self.habitacionOcupada:
            self.habitacionOcupada.setHuesped(None)
            self.habitacionOcupada.setDisponible(True)
            # Actualizar vector
            self.hotel.listaHabitaciones[self.posicionHabitacion] = self.habitacionOcupada

            messagebox.showinfo("Mensaje", "Se ha registrado la salida del huésped", parent=self)
            self.withdraw()


class VentanaPrincipal(tk.Tk):

    def __init__(self, hotel: Hotel):
        super().__init__()
        self.hotel = hotel
        self.title("Hotel")
        self.geometry("280x380")
        self.resizable(False, False)
        self._build()

    def _build(self):
        # Menú
        barraMenu = tk.Menu(self)
        menuOpciones = tk.Menu(barraMenu, tearoff=0)
        menuOpciones.add_command(label="Consultar habitaciones", command=self._onConsultarHabitaciones)
        menuOpciones.add_command(label="Salida de huéspedes", command=self._onSalidaHuespedes)
        barraMenu.add_cascade(label="Menú", menu=menuOpciones)
        self.config(menu=barraMenu)

    # Eventos de menú
    def _onConsultarHabitaciones(self):
        VentanaHabitaciones(self.hotel, master=self)

    def _onSalidaHuespedes(self):
        try:
            numeroHabitacion = simpledialog.askstring(
                "Salida de huéspedes", "Ingrese número de habitación", parent=self
            )
            if numeroHabitacion is None:
                return
            numero = int(numeroHabitacion)
            if numero < 1 or numero > 10:
                messagebox.showinfo("Mensaje", "El número de habitación debe estar entre 1 y 10", parent=self)
            elif self.hotel.buscarHabitacionOcupada(numero):
                VentanaSalida(self.hotel, numero, master=self)
            else:
                messagebox.showinfo("Mensaje", "La habitación ingresada no ha sido ocupada", parent=self)
        except Exception:
            messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)

class Principal:
    @staticmethod
    def main():
        hotel = Hotel()
        miVentanaPrincipal = VentanaPrincipal(hotel)
        miVentanaPrincipal.mainloop()


if __name__ == "__main__":
    Principal.main()
