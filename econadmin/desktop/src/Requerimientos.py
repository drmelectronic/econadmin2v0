# -*- coding: utf-8 *-*

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
sys.path += [os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]]

from econadmin.models import *
import gtk
import widgets


class Ventana(gtk.Window):
    """Explorador de Requerimientos"""
    def __init__(self):
        """Creador de Ventana"""
        super(Ventana, self).__init__()
        self.modelo = Requerimiento
        self.set_title(self.modelo._meta.verbose_name_plural)
        main_vbox = gtk.VBox(False, 0)
        self.add(main_vbox)
        self.toolbar = widgets.Toolbar(self)
        self.toolbar.entry.connect('changed', self.filtrar)
        main_vbox.pack_start(self.toolbar, False, False, 0)
        hpaned = gtk.HPaned()
        main_vbox.pack_start(hpaned, True, True, 0)
        self.store = (str, str, str, str, str, int)
        self.columnas = ("FECHA", "EMPRESA", "DESCRIPCION", "ENCARGADO")  # color,id

        self.vista = widgets.Vista(self)
        hpaned.add1(self.vista)
        self.detalles = widgets.Detalle(self)
        hpaned.add2(self.detalles)
        self.set_size_request(500, 200)
        self.show_all()

    def filtrar(self, widget):
        self.vista.filter.refilter()

    def nuevo(self, *args):
        Nuevo()


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

