# Estudiantes: Sergio Andrés Campos García - Anthony Stiven Beltran Rodriguez
# Grupo: 213023_37
# Sistema Integral de Gestion SOFTWARE FJ
# Clientes - Servicios - Reservas



import tkinter as tk
from tkinter import messagebox, ttk

from abc import ABC, abstractmethod

from datetime import datetime



# Registro de eventos y errores


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