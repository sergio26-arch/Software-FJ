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



        if nombre.strip()=="":


            raise ClienteInvalidoError(
                "El nombre no puede estar vacío"
            )



        if "@" not in correo:


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

        self.estado="CONFIRMADA"



    def cancelar(self):

        self.estado="CANCELADA"



    def procesar(self):


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
