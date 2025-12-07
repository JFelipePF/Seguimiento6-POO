# -*- coding: utf-8 


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from enum import Enum


class TipoCargo(Enum):
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"

class TipoGenero(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class Empleado:


    def __init__(self, nombre: str, apellidos: str, cargo: TipoCargo,
                 genero: TipoGenero, salarioDia: float, diasTrabajados: int,
                 otrosIngresos: float, pagosSalud: float, aportePensiones: float):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salarioDia = salarioDia
        self.diasTrabajados = diasTrabajados
        self.otrosIngresos = otrosIngresos
        self.pagosSalud = pagosSalud
        self.aportePensiones = aportePensiones

    # Métodos getters (mismo nombre que en Java)
    def getNombre(self): return self.nombre
    def getApellidos(self): return self.apellidos
    def getCargo(self): return self.cargo
    def getGenero(self): return self.genero
    def getSalarioDia(self): return self.salarioDia
    def getDiasTrabajados(self): return self.diasTrabajados
    def getOtrosIngresos(self): return self.otrosIngresos
    def getPagosSalud(self): return self.pagosSalud
    def getAportePensiones(self): return self.aportePensiones

    def calcularNomina(self) -> float:
        """Salario mensual = (días trabajados * sueldo por día) + otros ingresos - salud - pensiones"""
        return (self.salarioDia * self.diasTrabajados) + self.otrosIngresos - self.pagosSalud - self.aportePensiones


class ListaEmpleados:
  
    def __init__(self):
        self.lista: list[Empleado] = []
        self.totalNomina: float = 0.0

    def agregarEmpleado(self, a: Empleado):
        self.lista.append(a)

    def calcularTotalNomina(self) -> float:
        # En Java se acumulaba sin reset, aquí lo corregimos para evitar doble conteo.
        self.totalNomina = sum(e.calcularNomina() for e in self.lista)
        return self.totalNomina

    def obtenerMatriz(self):
      
        datos = []
        self.totalNomina = 0.0
        for e in self.lista:
            sueldo = e.calcularNomina()
            datos.append([e.getNombre(), e.getApellidos(), f"{sueldo:.2f}"])
            self.totalNomina += sueldo
        return datos

    def convertirTexto(self) -> str:
     
        texto = ""
        for e in self.lista:
            texto += (
                f"Nombre = {e.getNombre()}\n"
                f"Apellidos = {e.getApellidos()}\n"
                f"Cargo = {e.getCargo().value}\n"
                f"Género = {e.getGenero().value}\n"
                f"Salario = ${e.getSalarioDia():.2f}\n"
                f"Días trabajados = {e.getDiasTrabajados()}\n"
                f"Otros ingresos = ${e.getOtrosIngresos():.2f}\n"
                f"Pagos salud = ${e.getPagosSalud():.2f}\n"
                f"Aportes pensiones = ${e.getAportePensiones():.2f}\n---------\n"
            )
        total = self.calcularTotalNomina()
        texto += f"Total nómina = ${total:.2f}"
        return texto


# ==========================
# Clase: VentanaAgregarEmpleado
# ==========================

class VentanaAgregarEmpleado(tk.Toplevel):

    def __init__(self, lista: ListaEmpleados, master=None):
        super().__init__(master)
        self.lista = lista
        self.inicio()
        self.title("Agregar Empleado")
        self.geometry("300x400+100+100")
        self.resizable(False, False)

    def inicio(self):
        # Contenedor (equivalente a getContentPane con null layout)
        self.contenedor = tk.Frame(self)
        self.contenedor.place(x=0, y=0, relwidth=1, relheight=1)

        # Etiquetas y campos
        self.nombre = tk.Label(self.contenedor, text="Nombre:")
        self.nombre.place(x=20, y=20, width=135, height=23)
        self.campoNombre = tk.Entry(self.contenedor)
        self.campoNombre.place(x=160, y=20, width=100, height=23)

        self.apellidos = tk.Label(self.contenedor, text="Apellidos:")
        self.apellidos.place(x=20, y=50, width=135, height=23)
        self.campoApellidos = tk.Entry(self.contenedor)
        self.campoApellidos.place(x=160, y=50, width=100, height=23)

        self.cargo = tk.Label(self.contenedor, text="Cargo:")
        self.cargo.place(x=20, y=80, width=135, height=23)
        self.campoCargo = ttk.Combobox(self.contenedor, state="readonly",
                                       values=[TipoCargo.DIRECTIVO.value,
                                               TipoCargo.ESTRATEGICO.value,
                                               TipoCargo.OPERATIVO.value])
        self.campoCargo.current(0)
        self.campoCargo.place(x=160, y=80, width=100, height=23)

        # Género (radio buttons)
        self.genero = tk.Label(self.contenedor, text="Género:")
        self.genero.place(x=20, y=110, width=100, height=30)
        self.grupoGeneroVar = tk.StringVar(value=TipoGenero.MASCULINO.value)
        self.masculino = tk.Radiobutton(self.contenedor, text="Masculino",
                                        variable=self.grupoGeneroVar,
                                        value=TipoGenero.MASCULINO.value)
        self.masculino.place(x=160, y=110, width=100, height=30)
        self.femenino = tk.Radiobutton(self.contenedor, text="Femenino",
                                       variable=self.grupoGeneroVar,
                                       value=TipoGenero.FEMENINO.value)
        self.femenino.place(x=160, y=140, width=100, height=30)

        # Salario por día
        self.salarioDia = tk.Label(self.contenedor, text="Salario por día:")
        self.salarioDia.place(x=20, y=170, width=135, height=23)
        self.campoSalarioDia = tk.Entry(self.contenedor)
        self.campoSalarioDia.place(x=160, y=170, width=100, height=23)

        # Días trabajados
        self.numeroDias = tk.Label(self.contenedor, text="Días trabajados al mes:")
        self.numeroDias.place(x=20, y=200, width=135, height=23)
        self.campoNumeroDias = tk.Spinbox(self.contenedor, from_=1, to=31)
        self.campoNumeroDias.delete(0, "end")
        self.campoNumeroDias.insert(0, "30")
        self.campoNumeroDias.place(x=160, y=200, width=40, height=23)

        # Otros ingresos
        self.otrosIngresos = tk.Label(self.contenedor, text="Otros ingresos:")
        self.otrosIngresos.place(x=20, y=230, width=135, height=23)
        self.campoOtrosIngresos = tk.Entry(self.contenedor)
        self.campoOtrosIngresos.place(x=160, y=230, width=100, height=23)

        # Pagos salud
        self.aportesSalud = tk.Label(self.contenedor, text="Pagos por salud:")
        self.aportesSalud.place(x=20, y=260, width=135, height=23)
        self.campoAportesSalud = tk.Entry(self.contenedor)
        self.campoAportesSalud.place(x=160, y=260, width=100, height=23)

        # Pensiones
        self.pensiones = tk.Label(self.contenedor, text="Aportes pensiones:")
        self.pensiones.place(x=20, y=290, width=135, height=23)
        self.campoPensiones = tk.Entry(self.contenedor)
        self.campoPensiones.place(x=160, y=290, width=100, height=23)

        # Botones
        self.agregar = tk.Button(self.contenedor, text="Agregar", command=self.añadirEmpleado)
        self.agregar.place(x=20, y=320, width=100, height=23)
        self.limpiar = tk.Button(self.contenedor, text="Borrar", command=self.limpiarCampos)
        self.limpiar.place(x=160, y=320, width=80, height=23)

    def limpiarCampos(self):
        self.campoNombre.delete(0, "end")
        self.campoApellidos.delete(0, "end")
        self.campoSalarioDia.delete(0, "end")
        self.campoNumeroDias.delete(0, "end")
        self.campoNumeroDias.insert(0, "0")
        self.campoOtrosIngresos.delete(0, "end")
        self.campoAportesSalud.delete(0, "end")
        self.campoPensiones.delete(0, "end")

    def añadirEmpleado(self):
        # Cargo
        itemSeleccionado = self.campoCargo.get()
        if itemSeleccionado == "Directivo":
            tipoC = TipoCargo.DIRECTIVO
        elif itemSeleccionado == "Estratégico":
            tipoC = TipoCargo.ESTRATEGICO
        else:
            tipoC = TipoCargo.OPERATIVO

        # Género
        tipoG = TipoGenero.MASCULINO if self.grupoGeneroVar.get() == "Masculino" else TipoGenero.FEMENINO

        try:
            valor1 = self.campoNombre.get()
            valor2 = self.campoApellidos.get()
            valor3 = float(self.campoSalarioDia.get())
            valor4 = int(self.campoNumeroDias.get())
            valor5 = float(self.campoOtrosIngresos.get())
            valor6 = float(self.campoAportesSalud.get())
            valor7 = float(self.campoPensiones.get())

            e = Empleado(valor1, valor2, tipoC, tipoG, valor3, valor4, valor5, valor6, valor7)
            self.lista.agregarEmpleado(e)

            messagebox.showinfo("Mensaje", "El empleado ha sido agregado")
            self.limpiarCampos()
        except Exception:
            messagebox.showerror("Error", "Campo nulo o error en formato de número")




class VentanaNomina(tk.Toplevel):

    def __init__(self, lista: ListaEmpleados, master=None):
        super().__init__(master)
        self.lista = lista
        self.inicio()
        self.title("Nómina de Empleados")
        self.geometry("350x250+120+120")
        self.resizable(False, False)

    def inicio(self):
        self.contenedor = tk.Frame(self)
        self.contenedor.place(x=0, y=0, relwidth=1, relheight=1)

        self.empleados = tk.Label(self.contenedor, text="Lista de empleados:")
        self.empleados.place(x=20, y=10, width=135, height=23)

        datos = self.lista.obtenerMatriz()
        titulos = ("NOMBRE", "APELLIDOS", "SUELDO")

        # Tabla (Treeview)
        self.tabla = ttk.Treeview(self.contenedor, columns=titulos, show="headings")
        for t in titulos:
            self.tabla.heading(t, text=t)
            self.tabla.column(t, width=100, anchor="w")
        for fila in datos:
            self.tabla.insert("", "end", values=fila)
        self.tabla.place(x=20, y=50, width=310, height=100)

        # Total nómina mensual
        self.nomina = tk.Label(self.contenedor, text=f"Total nómina mensual = $ {self.lista.totalNomina:.2f}")
        self.nomina.place(x=20, y=160, width=250, height=23)



class VentanaPrincipal(tk.Tk):
  
    def __init__(self):
        super().__init__()
        self.empleados = ListaEmpleados()
        self.inicio()
        self.title("Nómina")
        self.geometry("280x380+80+80")
        self.resizable(False, False)

    def inicio(self):
        self.contenedor = tk.Frame(self)
        self.contenedor.place(x=0, y=0, relwidth=1, relheight=1)

        # Barra de menú
        self.barraMenu = tk.Menu(self)
        self.menuOpciones = tk.Menu(self.barraMenu, tearoff=0)
        self.itemMenu1 = "Agregar empleado"
        self.itemMenu2 = "Calcular nómina"
        self.itemMenu3 = "Guardar archivo"

        self.menuOpciones.add_command(label=self.itemMenu1, command=self._accionAgregar)
        self.menuOpciones.add_command(label=self.itemMenu2, command=self._accionCalcular)
        self.menuOpciones.add_separator()
        self.menuOpciones.add_command(label=self.itemMenu3, command=self._accionGuardar)

        self.barraMenu.add_cascade(label="Menú", menu=self.menuOpciones)
        self.config(menu=self.barraMenu)

    # Eventos de menú (equivalentes a actionPerformed en Java)
    def _accionAgregar(self):
        ventanaAgregar = VentanaAgregarEmpleado(self.empleados, master=self)
        ventanaAgregar.grab_set()
        ventanaAgregar.focus_force()

    def _accionCalcular(self):
        ventanaNomina = VentanaNomina(self.empleados, master=self)
        ventanaNomina.grab_set()
        ventanaNomina.focus_force()

    def _accionGuardar(self):
        carpeta = filedialog.askdirectory(title="Selecciona el directorio destino")
        if not carpeta:
            return
        try:
            contenido = self.empleados.convertirTexto()
            ruta = f"{carpeta}/Nómina.txt"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)

            messagebox.showinfo("Mensaje", f"El archivo de la nómina 'Nómina.txt' se ha creado en:\n{carpeta}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear el archivo:\n{e}")



class Principal:
    @staticmethod
    def main():
        miVentanaPrincipal = VentanaPrincipal()
        miVentanaPrincipal.mainloop()


# Ejecutar
if __name__ == "__main__":
    Principal.main()
