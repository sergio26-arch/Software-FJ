# Estudiantes: Sergio Andrés Campos García - Anthony Stiven Beltran Rodriguez - Juan Camilo Cardozo Gomez
# Grupo: 213023_37
# Sistema Integral de Gestion SOFTWARE FJ
# Clientes - Servicios - Reservas



import tkinter as tk
from tkinter import messagebox, ttk

from abc import ABC, abstractmethod

from datetime import datetime



# Registro de eventos y errores

#1
def registrar_log(mensaje):

    try:

        with open(
            "Software_FJ_logs.txt",
            "a",
            encoding="utf-8"
        ) as archivo:


            archivo.write(
                f"{datetime.now()} --> {mensaje}\n"
            )


    except Exception as error:

        print(
            "Error creando archivo log:",
            error
        )



# Excepciones personalizadas


#
class ErrorSistema(Exception):

    pass


class ClienteInvalidoError(ErrorSistema):

    pass


class ServicioInvalidoError(ErrorSistema):

    pass


class ReservaInvalidaError(ErrorSistema):

    pass


class OperacionNoPermitidaError(ErrorSistema):

    pass



# Clase abstracta general



class Entidad(ABC):


    def __init__(self, identificacion):

        self._identificacion = identificacion



    @property
    def identificacion(self):

        return self._identificacion



    @abstractmethod
    def mostrar(self):

        pass




# Clase cliente



class Cliente(Entidad):


    def __init__(
            self,
            identificacion,
            nombre,
            correo
    ):


        super().__init__(
            identificacion
        )



        if identificacion is None or str(identificacion).strip() == "":


            raise ClienteInvalidoError(
                "La identificación es obligatoria"
            )



        if not isinstance(nombre, str) or nombre.strip() == "":


            raise ClienteInvalidoError(
                "El nombre no puede estar vacío"
            )



        if not isinstance(correo, str) or "@" not in correo or "." not in correo:


            raise ClienteInvalidoError(
                "Correo electrónico inválido"
            )



        # Encapsulación

        self.__nombre = nombre

        self.__correo = correo




    @property
    def nombre(self):

        return self.__nombre




    @property
    def correo(self):

        return self.__correo



    def mostrar(self):


        return (

            f"{self.__nombre} | "
            f"{self.__correo}"

        )



# Clase abstracta servicio


class Servicio(Entidad, ABC):


    contador = 1



    def __init__(
            self,
            nombre,
            precio
    ):


        super().__init__(
            Servicio.contador
        )


        Servicio.contador += 1



        if not isinstance(nombre, str) or nombre.strip() == "":

            raise ServicioInvalidoError(
                "El nombre del servicio no puede estar vacío"
            )


        if isinstance(precio, bool) or not isinstance(precio, (int, float)):

            raise ServicioInvalidoError(
                "El precio debe ser un valor numérico"
            )


        if precio <= 0:

            raise ServicioInvalidoError(
                "El precio debe ser mayor a cero"
            )



        self.nombre = nombre

        self.precio = precio



    @abstractmethod
    def calcular_costo(self,*args):

        pass



    @abstractmethod
    def descripcion(self):

        pass

    def mostrar(self):

        return (
            f"{self.nombre} - "
            f"${self.precio}"
        )

    
# Servicio reserva de salas


class ReservaSala(Servicio):


    def calcular_costo(self, *args, **kwargs):

        horas = 1

        impuesto = False


        if len(args) > 0:

            horas = args[0]


        if "impuesto" in kwargs:

            impuesto = kwargs["impuesto"]



        if isinstance(horas, bool) or not isinstance(horas, (int, float)):

            raise ServicioInvalidoError(
                "La cantidad de horas debe ser numérica"
            )


        if horas <= 0:

            raise ServicioInvalidoError(
                "La cantidad de horas debe ser mayor a cero"
            )



        costo = self.precio * horas


        if impuesto:

            costo *= 1.19


        return costo



    def descripcion(self):

        return "Reserva de sala"



# Servicio alquiler equipos



class AlquilerEquipo(Servicio):


    def calcular_costo(self, *args, **kwargs):

        dias = 1

        descuento = 0


        if len(args) > 0:

            dias = args[0]


        if "descuento" in kwargs:

            descuento = kwargs["descuento"]



        if isinstance(dias, bool) or not isinstance(dias, (int, float)):

            raise ServicioInvalidoError(
                "La cantidad de días debe ser numérica"
            )


        if dias <= 0:

            raise ServicioInvalidoError(
                "La cantidad de días debe ser mayor a cero"
            )


        if descuento < 0 or descuento > 1:

            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 1"
            )



        costo = self.precio * dias


        costo -= costo * descuento


        return costo



    def descripcion(self):

        return "Alquiler de equipos"



# Servicio asesoria



class AsesoriaEspecializada(Servicio):


    def calcular_costo(self, *args, **kwargs):

        horas = 1


        if len(args) > 0:

            horas = args[0]



        if isinstance(horas, bool) or not isinstance(horas, (int, float)):

            raise ServicioInvalidoError(
                "La cantidad de horas debe ser numérica"
            )


        if horas <= 0:

            raise ServicioInvalidoError(
                "Cantidad de horas incorrecta"
            )


        return self.precio * horas



    def descripcion(self):

        return "Asesoría especializada"



# Clase reserva



class Reserva:


    def __init__(
            self,
            cliente,
            servicio,
            duracion
    ):


        if duracion <=0:

            raise ReservaInvalidaError(
                "La duración debe ser mayor a cero"
            )



        self.cliente = cliente

        self.servicio = servicio

        self.duracion = duracion

        self.estado = "CREADA"




    def confirmar(self):

        if self.estado == "CANCELADA":

            raise OperacionNoPermitidaError(
                "No se puede confirmar una reserva cancelada"
            )


        self.estado="CONFIRMADA"



    def cancelar(self):

        if self.estado == "CANCELADA":

            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada"
            )


        self.estado="CANCELADA"



    def procesar(self):


        if self.estado == "CANCELADA":

            raise OperacionNoPermitidaError(
                "No se puede procesar una reserva cancelada"
            )


        try:


            costo = self.servicio.calcular_costo(
                self.duracion
            )


        except Exception as error:


            registrar_log(
                f"Error procesando reserva: {error}"
            )


            raise ReservaInvalidaError(
                "No fue posible procesar la reserva"
            ) from error


        else:


            return costo


        finally:


            registrar_log(
                "Proceso de reserva finalizado"
            )



    def mostrar(self):


        return (

            f"{self.cliente.nombre} | "
            f"{self.servicio.descripcion()} | "
            f"{self.estado}"

        )



# ============================================================
# Simulación de operaciones (mínimo 10)
# El sistema continúa activo aunque ocurran errores graves
# ============================================================



def ejecutar_simulacion():


    clientes = []

    servicios = []

    reservas = []


    print("=" * 55)

    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")

    print("=" * 55)



    # ---- Operación 1: Cliente válido ----

    try:

        cliente_ok = Cliente(101, "Ana Torres", "ana@fj.com")

        clientes.append(cliente_ok)

        registrar_log(f"Cliente registrado: {cliente_ok.mostrar()}")

        print(f"[OP 1] Cliente creado -> {cliente_ok.mostrar()}")


    except ErrorSistema as error:

        registrar_log(f"OP 1 fallida: {error}")

        print(f"[OP 1] ERROR controlado -> {error}")



    # ---- Operación 2: Cliente con nombre vacío (inválido) ----

    try:

        Cliente(102, "   ", "pedro@fj.com")


    except ErrorSistema as error:

        registrar_log(f"OP 2 fallida: {error}")

        print(f"[OP 2] ERROR controlado -> {error}")



    # ---- Operación 3: Cliente con correo inválido (sin @) ----

    try:

        Cliente(103, "Luis Gómez", "luis-correo-invalido")


    except ErrorSistema as error:

        registrar_log(f"OP 3 fallida: {error}")

        print(f"[OP 3] ERROR controlado -> {error}")



    # ---- Operación 4: Crear servicio Reserva de Sala (válido) ----

    try:

        sala = ReservaSala("Sala Ejecutiva", 50000)

        servicios.append(sala)

        registrar_log(f"Servicio creado: {sala.mostrar()}")

        print(f"[OP 4] Servicio creado -> {sala.mostrar()}")


    except ErrorSistema as error:

        registrar_log(f"OP 4 fallida: {error}")

        print(f"[OP 4] ERROR controlado -> {error}")



    # ---- Operación 5: Crear servicio Alquiler de Equipo (válido) ----

    try:

        equipo = AlquilerEquipo("Proyector 4K", 30000)

        servicios.append(equipo)

        registrar_log(f"Servicio creado: {equipo.mostrar()}")

        print(f"[OP 5] Servicio creado -> {equipo.mostrar()}")


    except ErrorSistema as error:

        registrar_log(f"OP 5 fallida: {error}")

        print(f"[OP 5] ERROR controlado -> {error}")



    # ---- Operación 6: Crear servicio Asesoría Especializada (válido) ----

    try:

        asesoria = AsesoriaEspecializada("Asesoría Legal", 80000)

        servicios.append(asesoria)

        registrar_log(f"Servicio creado: {asesoria.mostrar()}")

        print(f"[OP 6] Servicio creado -> {asesoria.mostrar()}")


    except ErrorSistema as error:

        registrar_log(f"OP 6 fallida: {error}")

        print(f"[OP 6] ERROR controlado -> {error}")



    # ---- Operación 7: Reserva válida + procesamiento ----

    try:

        reserva_ok = Reserva(cliente_ok, sala, 3)

        reserva_ok.confirmar()

        costo = reserva_ok.procesar()

        reservas.append(reserva_ok)

        registrar_log(f"Reserva procesada por ${costo}")

        print(f"[OP 7] {reserva_ok.mostrar()} -> costo ${costo}")


    except ErrorSistema as error:

        registrar_log(f"OP 7 fallida: {error}")

        print(f"[OP 7] ERROR controlado -> {error}")



    # ---- Operación 8: Sobrecarga -> costo de sala con impuesto ----

    try:

        costo_imp = sala.calcular_costo(2, impuesto=True)

        registrar_log(f"Costo sala con impuesto: ${costo_imp}")

        print(f"[OP 8] Costo sala 2h con impuesto -> ${costo_imp}")


    except ErrorSistema as error:

        registrar_log(f"OP 8 fallida: {error}")

        print(f"[OP 8] ERROR controlado -> {error}")



    # ---- Operación 9: Sobrecarga -> costo de equipo con descuento ----

    try:

        costo_desc = equipo.calcular_costo(5, descuento=0.15)

        registrar_log(f"Costo equipo con descuento: ${costo_desc}")

        print(f"[OP 9] Costo equipo 5 días con 15% desc -> ${costo_desc}")


    except ErrorSistema as error:

        registrar_log(f"OP 9 fallida: {error}")

        print(f"[OP 9] ERROR controlado -> {error}")



    # ---- Operación 10: Reserva con duración inválida (fallida) ----

    try:

        Reserva(cliente_ok, equipo, 0)


    except ErrorSistema as error:

        registrar_log(f"OP 10 fallida: {error}")

        print(f"[OP 10] ERROR controlado -> {error}")



    # ---- Operación 11: Servicio con parámetro inválido (asesoría, 0 horas) ----

    try:

        asesoria.calcular_costo(0)


    except ErrorSistema as error:

        registrar_log(f"OP 11 fallida: {error}")

        print(f"[OP 11] ERROR controlado -> {error}")



    # ---- Operación 12: Operación no permitida (procesar reserva cancelada) ----

    try:

        reserva_falla = Reserva(cliente_ok, asesoria, 4)

        reserva_falla.cancelar()

        costo_falla = reserva_falla.procesar()

        print(f"[OP 12] {reserva_falla.mostrar()} -> costo ${costo_falla}")


    except ErrorSistema as error:

        registrar_log(f"OP 12 fallida: {error}")

        print(f"[OP 12] ERROR controlado -> {error}")



    # ---- Operación 13: Creación de servicio con precio inválido (fallida) ----

    try:

        ReservaSala("Sala Fantasma", -1000)


    except ErrorSistema as error:

        registrar_log(f"OP 13 fallida: {error}")

        print(f"[OP 13] ERROR controlado -> {error}")



    print("=" * 55)

    print(f"Clientes registrados: {len(clientes)}")

    print(f"Servicios creados:    {len(servicios)}")

    print(f"Reservas procesadas:  {len(reservas)}")

    print("Simulación finalizada. El sistema permaneció estable.")

    print("=" * 55)



# ============================================================
# Interfaz gráfica (Tkinter)
# ============================================================



class AplicacionFJ:


    TIPOS_SERVICIO = {
        "Reserva de Sala": ReservaSala,
        "Alquiler de Equipo": AlquilerEquipo,
        "Asesoría Especializada": AsesoriaEspecializada,
    }



    def __init__(self, root):

        self.root = root

        self.root.title("Sistema Integral de Gestión - Software FJ")

        self.root.geometry("780x580")


        # Listas internas (sin base de datos)

        self.clientes = []

        self.servicios = []

        self.reservas = []


        contenedor = ttk.Notebook(self.root)

        contenedor.pack(fill="both", expand=True, padx=10, pady=10)


        self._construir_tab_clientes(contenedor)

        self._construir_tab_servicios(contenedor)

        self._construir_tab_reservas(contenedor)


        ttk.Button(
            self.root,
            text="Ejecutar simulación de consola (13 operaciones)",
            command=self._correr_simulacion,
        ).pack(pady=(0, 10))



    # ---------------- Pestaña Clientes ----------------

    def _construir_tab_clientes(self, contenedor):

        marco = ttk.Frame(contenedor)

        contenedor.add(marco, text="Clientes")


        ttk.Label(marco, text="Identificación:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cli_id = ttk.Entry(marco)
        self.cli_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cli_nombre = ttk.Entry(marco)
        self.cli_nombre.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Correo:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.cli_correo = ttk.Entry(marco)
        self.cli_correo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            marco,
            text="Registrar cliente",
            command=self.registrar_cliente,
        ).grid(row=3, column=0, columnspan=2, pady=8)

        self.tabla_clientes = ttk.Treeview(
            marco,
            columns=("id", "nombre", "correo"),
            show="headings",
            height=10,
        )
        self.tabla_clientes.heading("id", text="ID")
        self.tabla_clientes.heading("nombre", text="Nombre")
        self.tabla_clientes.heading("correo", text="Correo")
        self.tabla_clientes.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")


    def registrar_cliente(self):

        try:

            cliente = Cliente(
                self.cli_id.get(),
                self.cli_nombre.get(),
                self.cli_correo.get(),
            )

            self.clientes.append(cliente)

            self.tabla_clientes.insert(
                "",
                "end",
                values=(cliente.identificacion, cliente.nombre, cliente.correo),
            )

            self._refrescar_combos()

            registrar_log(f"[GUI] Cliente registrado: {cliente.mostrar()}")

            messagebox.showinfo("Éxito", "Cliente registrado correctamente")

            self.cli_id.delete(0, tk.END)
            self.cli_nombre.delete(0, tk.END)
            self.cli_correo.delete(0, tk.END)


        except ErrorSistema as error:

            registrar_log(f"[GUI] Error registrando cliente: {error}")

            messagebox.showerror("Error", str(error))


        except Exception as error:

            registrar_log(f"[GUI] Error inesperado (cliente): {error}")

            messagebox.showerror("Error inesperado", str(error))



    # ---------------- Pestaña Servicios ----------------

    def _construir_tab_servicios(self, contenedor):

        marco = ttk.Frame(contenedor)

        contenedor.add(marco, text="Servicios")


        ttk.Label(marco, text="Tipo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.serv_tipo = ttk.Combobox(
            marco,
            values=list(self.TIPOS_SERVICIO.keys()),
            state="readonly",
        )
        self.serv_tipo.current(0)
        self.serv_tipo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.serv_nombre = ttk.Entry(marco)
        self.serv_nombre.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Precio:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.serv_precio = ttk.Entry(marco)
        self.serv_precio.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(
            marco,
            text="Crear servicio",
            command=self.crear_servicio,
        ).grid(row=3, column=0, columnspan=2, pady=8)

        self.tabla_servicios = ttk.Treeview(
            marco,
            columns=("id", "tipo", "nombre", "precio"),
            show="headings",
            height=10,
        )
        self.tabla_servicios.heading("id", text="ID")
        self.tabla_servicios.heading("tipo", text="Tipo")
        self.tabla_servicios.heading("nombre", text="Nombre")
        self.tabla_servicios.heading("precio", text="Precio")
        self.tabla_servicios.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")


    def crear_servicio(self):

        try:

            clase = self.TIPOS_SERVICIO[self.serv_tipo.get()]


            try:

                precio = float(self.serv_precio.get().strip())


            except ValueError as error:

                raise ServicioInvalidoError(
                    "El precio debe ser un valor numérico"
                ) from error


            servicio = clase(self.serv_nombre.get(), precio)

            self.servicios.append(servicio)

            self.tabla_servicios.insert(
                "",
                "end",
                values=(
                    servicio.identificacion,
                    servicio.descripcion(),
                    servicio.nombre,
                    servicio.precio,
                ),
            )

            self._refrescar_combos()

            registrar_log(f"[GUI] Servicio creado: {servicio.mostrar()}")

            messagebox.showinfo("Éxito", "Servicio creado correctamente")

            self.serv_nombre.delete(0, tk.END)
            self.serv_precio.delete(0, tk.END)


        except ErrorSistema as error:

            registrar_log(f"[GUI] Error creando servicio: {error}")

            messagebox.showerror("Error", str(error))


        except Exception as error:

            registrar_log(f"[GUI] Error inesperado (servicio): {error}")

            messagebox.showerror("Error inesperado", str(error))



    # ---------------- Pestaña Reservas ----------------

    def _construir_tab_reservas(self, contenedor):

        marco = ttk.Frame(contenedor)

        contenedor.add(marco, text="Reservas")


        ttk.Label(marco, text="Cliente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.res_cliente = ttk.Combobox(marco, values=[], state="readonly")
        self.res_cliente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Servicio:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.res_servicio = ttk.Combobox(marco, values=[], state="readonly")
        self.res_servicio.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Duración:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.res_duracion = ttk.Entry(marco)
        self.res_duracion.grid(row=2, column=1, padx=5, pady=5)

        barra = ttk.Frame(marco)
        barra.grid(row=3, column=0, columnspan=3, pady=8)

        ttk.Button(barra, text="Crear reserva", command=self.crear_reserva).grid(row=0, column=0, padx=4)
        ttk.Button(barra, text="Confirmar", command=self.confirmar_reserva).grid(row=0, column=1, padx=4)
        ttk.Button(barra, text="Cancelar", command=self.cancelar_reserva).grid(row=0, column=2, padx=4)
        ttk.Button(barra, text="Procesar", command=self.procesar_reserva).grid(row=0, column=3, padx=4)

        self.tabla_reservas = ttk.Treeview(
            marco,
            columns=("cliente", "servicio", "estado", "costo"),
            show="headings",
            height=10,
        )
        self.tabla_reservas.heading("cliente", text="Cliente")
        self.tabla_reservas.heading("servicio", text="Servicio")
        self.tabla_reservas.heading("estado", text="Estado")
        self.tabla_reservas.heading("costo", text="Costo")
        self.tabla_reservas.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")


    def _refrescar_combos(self):

        self.res_cliente["values"] = [c.mostrar() for c in self.clientes]

        self.res_servicio["values"] = [
            f"{s.descripcion()} - {s.nombre}" for s in self.servicios
        ]


    def _reserva_seleccionada(self):

        seleccion = self.tabla_reservas.selection()

        if not seleccion:

            raise OperacionNoPermitidaError(
                "Debe seleccionar una reserva de la lista"
            )

        indice = int(seleccion[0])

        return indice, self.reservas[indice]


    def _pintar_fila(self, indice, reserva, costo=None):

        if costo is None and self.tabla_reservas.exists(str(indice)):

            costo = self.tabla_reservas.item(str(indice), "values")[3]


        valores = (
            reserva.cliente.nombre,
            reserva.servicio.descripcion(),
            reserva.estado,
            costo if costo is not None else "-",
        )


        if self.tabla_reservas.exists(str(indice)):

            self.tabla_reservas.item(str(indice), values=valores)


        else:

            self.tabla_reservas.insert("", "end", iid=str(indice), values=valores)


    def crear_reserva(self):

        try:

            indice_cliente = self.res_cliente.current()

            indice_servicio = self.res_servicio.current()


            if indice_cliente < 0 or indice_servicio < 0:

                raise ReservaInvalidaError(
                    "Debe seleccionar un cliente y un servicio"
                )


            try:

                duracion = int(self.res_duracion.get().strip())


            except ValueError as error:

                raise ReservaInvalidaError(
                    "La duración debe ser un número entero"
                ) from error


            reserva = Reserva(
                self.clientes[indice_cliente],
                self.servicios[indice_servicio],
                duracion,
            )

            self.reservas.append(reserva)

            self._pintar_fila(len(self.reservas) - 1, reserva)

            registrar_log(f"[GUI] Reserva creada: {reserva.mostrar()}")

            messagebox.showinfo("Éxito", "Reserva creada correctamente")


        except ErrorSistema as error:

            registrar_log(f"[GUI] Error creando reserva: {error}")

            messagebox.showerror("Error", str(error))


        except Exception as error:

            registrar_log(f"[GUI] Error inesperado (reserva): {error}")

            messagebox.showerror("Error inesperado", str(error))


    def confirmar_reserva(self):

        try:

            indice, reserva = self._reserva_seleccionada()

            reserva.confirmar()

            self._pintar_fila(indice, reserva)

            registrar_log(f"[GUI] Reserva confirmada: {reserva.mostrar()}")

            messagebox.showinfo("Éxito", "Reserva confirmada")


        except ErrorSistema as error:

            registrar_log(f"[GUI] Error confirmando reserva: {error}")

            messagebox.showerror("Error", str(error))


    def cancelar_reserva(self):

        try:

            indice, reserva = self._reserva_seleccionada()

            reserva.cancelar()

            self._pintar_fila(indice, reserva)

            registrar_log(f"[GUI] Reserva cancelada: {reserva.mostrar()}")

            messagebox.showinfo("Éxito", "Reserva cancelada")


        except ErrorSistema as error:

            registrar_log(f"[GUI] Error cancelando reserva: {error}")

            messagebox.showerror("Error", str(error))


    def procesar_reserva(self):

        try:

            indice, reserva = self._reserva_seleccionada()

            costo = reserva.procesar()

            self._pintar_fila(indice, reserva, costo)

            registrar_log(f"[GUI] Reserva procesada por ${costo}")

            messagebox.showinfo("Éxito", f"Reserva procesada. Costo: ${costo}")


        except ErrorSistema as error:

            registrar_log(f"[GUI] Error procesando reserva: {error}")

            messagebox.showerror("Error", str(error))


    def _correr_simulacion(self):

        ejecutar_simulacion()

        messagebox.showinfo(
            "Simulación",
            "Simulación ejecutada. Revise la consola y el archivo de logs.",
        )



if __name__ == "__main__":

    ventana = tk.Tk()

    AplicacionFJ(ventana)

    ventana.mainloop()
