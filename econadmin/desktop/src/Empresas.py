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
        self.modulo = "Requerimientos"
        main_vbox = gtk.VBox(False, 0)
        self.add(main_vbox)
        estados = RequerimientoEstado.objects.all()
        self.toolbar = widgets.Toolbar(self.modulo, estados)
        main_vbox.pack_start(self.toolbar, False, False, 0)
        hpaned = gtk.HPaned()
        main_vbox.pack_start(hpaned, True, True, 0)
        self.liststore = gtk.ListStore(str, str, str, str, str, int)
        self.actualizar()
        columnas = ("FECHA", "EMPRESA", "DESCRIPCION", "ENCARGADO")  # color,id
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.set_size_request(400, 150)
        hpaned.add1(self.sw)
        self.detalles = gtk.Label('Detalles')
        hpaned.add2(self.detalles)
        self.filter = self.liststore.filter_new()
        self.filter.set_visible_func(self.filtro)
        self.sort = gtk.TreeModelSort(self.filter)
        self.sort.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.treeview = gtk.TreeView(self.sort)
        for i, columna in enumerate(columnas):
            cell = gtk.CellRendererText()
            tv = gtk.TreeViewColumn(columna)
            tv.pack_start(cell, True)
            tv.set_attributes(cell, text=i)
            self.treeview.append_column(tv)
        self.sw.add(self.treeview)
        self.set_size_request(500, 200)
        self.show_all()
        print self.sw

    def filtro(self, model, iter):
        """Búsqueda por Texto y Estado"""
        return True

    def actualizar(self):
        """Actualizar la lista"""
        self.liststore.clear()
        print 'sql'
        requerimientos = Requerimiento.objects.select_related(depth=1).all()
        print requerimientos
        for r in requerimientos:
            self.liststore.append(
                r.fecha,
                r.empresa.comercial,
                r.requerimiento_linea_set.all.descripcion,
                r.cotizar.nombre,
                r.estado.nombre,
                r.id)


class Nuevo(gtk.Dialog):
    """Ventana de Creación de Nuevo Requerimiento"""
    def __init__(self):
        """Creado de Ventana Nuevo"""
        super(Nuevo, self).__init__(
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        )
        self.set_title('Nueva Empresa')
        campos = widgets.Formulario(Empresa)
        for nombre, l, w in campos:
            hbox = gtk.HBox(False, 0)
            self.vbox.pack_start(hbox)
            hbox.pack_start(l)
            hbox.pack_start(w)
        self.show_all()
