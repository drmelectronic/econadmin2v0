#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time
from decimal import Decimal

# VERBOSE NAME = ?
# VERBOSE NAME PLURAL = Titulo para ventanas

# Direcciones


class Banco(models.Model):
    """Todos los bancos del Perú"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"


class CorreoTipo(models.Model):
    """Trabajo, Personal, etc"""
    nombre = models.CharField(max_length=8)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"


class CuentaTipo(models.Model):
    """Ahorro, Corriente"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"


class DirDepartamento(models.Model):
    """Todos los departamentos"""
    nombre = models.CharField(max_length=32)
    codigo = models.PositiveSmallIntegerField()
    pais = models.ForeignKey(DirPais)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nombre']


class DireccionDistrito(models.Model):
    """Todos los distritos"""
    nombre = models.CharField(max_length=32)
    provincia = models.ForeignKey(DirProvincia)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['nombre']


class DireccionPais(models.Model):
    """Todos los países"""
    nombre = models.CharField(max_length=32)
    codigo = models.PositiveSmallIntegerField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "País"
        verbose_name_plural = "Paises"
        ordering = ['nombre']



class DireccionProvincia(models.Model):
    """Todas las provincias"""
    nombre = models.CharField(max_length=32)
    departamento = models.ForeignKey(DirDepartamento)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['nombre']


class DireccionTipo(models.Model):
    """Casa/Dirección Legal, Almacen"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"
        ordering = ['nombre']


class EmpresaTipo(models.Model):
    """Nosotros, Clientes, Proveedores, Marcas, Independientes"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"


class EstadoCivil(models.Model):
    """Soltero, Casado, etc"""
    nombre = models.CharField(max_length=1)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado Civil"


class Moneda(models.Model):
    """Monedas del sistema"""
    nombre = models.CharField(max_length=32)
    simbolo = models.CharField(max_length=3)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.simbolo

    class Meta:
        """Configuraciones"""
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"


class Procedimiento(models.Model):
    """Desensamblaje, Limpieza, OverHold"""
    nombre = models.CharField(max_length=32)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Procedimiento"
        verbose_name_plural = "Propcedimientos"


class Sexo(models.Model):
    """Masculino, Feminino"""
    nombre = models.CharField(max_length=1)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        verbose_name = "Sexo"


class TelefonoOperador(models.Model):
    """Operadores de Telefonía"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"


class TelefonoTipo(models.Model):
    """Fijo, Celular, RPM"""
    nombre = models.CharField(max_length=8)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"


class TelefonoUso(models.Model):
    """Casa, Trabajo, Personal"""
    nombre = models.CharField(max_length=8)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Uso"
        verbose_name_plural = "Usos"


class TipoCambio(models.Model):
    """Entre Sol y Dólar"""
    tk = models.DecimalField(max_digits=4, decimal_places=3)
    fecha = models.DateField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.tk)

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo de Cambio"


class TrabajadorEstado(models.Model):
    """Activo, Inactivo"""
    nombre = models.CharField(max_length=8)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class TrabajadorPermiso(models.Model):
    """Permisos en el sistema para los usuarios"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"


class TrabajadorRol(models.Model):
    """Tipo de Trabajador"""
    nombre = models.CharField(max_length=16)
    orden = models.PositiveSmallIntegerField()
    permisos = models.ManyToManyField(TrabajadorPermiso)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class UserProfile(models.Model):
    """"""

