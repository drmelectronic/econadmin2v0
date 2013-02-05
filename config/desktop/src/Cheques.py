# -*- coding: utf-8 *-*

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
sys.path += [os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]]

from econadmin.models import *
import gtk
import widgets
import gobject


class Ventana(gtk.Window):
    """Explorador de Requerimientos"""
    def __init__(self):
        """Creador de Ventana"""
        super(Ventana, self).__init__()
        self.modelo = Cheque
        self.set_title(self.modelo._meta.verbose_name_plural)
        self.store = (str, str, str, str, str, str, str, gobject.TYPE_PYOBJECT)
        self.columnas = ("CODIGO", "GIRO", "DESDE", "MONTO", "NOMBRE", "CUENTA")  # color,objeto
        self.atributos = ('numero', 'fecha', 'desde', 'monto', 'nombre', 'cuenta', 'estado')
        self.vista = widgets.Vista(self)
        self.toolbar = widgets.Toolbar(self)
        # Construccion
        main_vbox = gtk.VBox(False, 0)
        self.add(main_vbox)
        main_vbox.pack_start(self.toolbar, False, False, 0)
        hpaned = gtk.HPaned()
        main_vbox.pack_start(hpaned, True, True, 0)
        hpaned.add1(self.vista)
        self.detalles = widgets.Detalle(self)
        hpaned.add2(self.detalles)
        self.set_size_request(500, 200)
        self.show_all()

    def new_defaults(self, persona=True):
        """Datos por defecto al abrir la ventana de creación NUEVO"""
        fila = self.vista.get_values()
        if fila is None:
            codigo = None
            cuenta = None
        else:
            codigo = int(fila[0]) + 1
            cuenta = fila[5]
        fecha = 0
        desde = 0
        monto = None
        if persona:
            nombre = Persona
        else:
            nombre = Empresa
        self.defaults = (codigo, fecha, desde, monto, nombre, cuenta)

    def nuevo(self, *args):
        """Que hacer cuando se crea uno nuevo"""
        print 'nuevo sobreescrito'


class Nuevo(gtk.Dialog):
    """Ventana de Creación de Nuevo Requerimiento"""
    def __init__(self):
        """Creado de Ventana Nuevo"""
        super(Nuevo, self).__init__(
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        )
        campos = widgets.Formulario(Requerimiento)
        self.set_title('Nuevo Requerimiento')
        for e in campos:
            hbox = gtk.HBox(False, 0)
            self.vbox.pack_start(hbox)
            hbox.pack_start(e.label)
            hbox.pack_start(e.widget)
        but_guardar = gtk.Button('Guardar')
        self.action_area.pack_start(but_guardar)
        but_guardar.connect('clicked', self.guardar)
        self.show_all()

    def guardar(self, *args):
        """Ventana de """
        nuevo = Requerimiento()
        for e in self.campos:
            print e.name, ': ', e.valor
            setattr(nuevo, e.name, e.valor)
        nuevo.save()

