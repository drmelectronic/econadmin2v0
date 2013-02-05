# -*- coding: utf-8 *-*

import gtk
import gobject
from django.db.models import fields
from econadmin.models import *
from django.db.models import Q
from decimal import Decimal
import datetime
import Almacen
import Asistencia
import Balance
import Cambio
import Cheques
import Cotizaciones
import Compras
import Empresas
import Facturas
import Finanzas
import Guias
import Personas
import Planilla
import Requerimientos
import Tareas

class Selector:
    """Selector de Estado y Tipos"""
    def __init__(self):
        icon = gtk.Image()
        icon.set_from_file('econadmin/desktop/images/toolbar/Tipos.png')
        item = gtk.MenuToolButton(icon, "Tipos")
        menu = gtk.Menu()
        item.set_menu(menu)
        y = 0
        for estado in estados:
            nombre = estado.nombre
            check = gtk.CheckMenuItem(nombre, True)
            menu.attach(check, 0, 1, y, y + 1)
            y += 1
        menu.show_all()
        self.insert(item, 1)

class Toolbar(gtk.Toolbar):
    """Herramientas Básicas:
        Filtrar, Tipos, Nuevo, Editar/Copiar, Imprimir, Enviar"""
    def __init__(self, widget):
        """Creador de Toolbar"""
        super(Toolbar, self).__init__()
        self.modelo = widget.modelo
        self.widget = widget
        label = gtk.Label('Buscar:')
        self.entry = gtk.Entry()
        self.entry.connect('activate', self.nuevo)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(self.entry)
        item = gtk.ToolItem()
        item.add(hbox)
        self.insert(item, 0)
        self.item_nuevo = ToolButton('Nuevo', self.nuevo)
        self.insert(self.item_nuevo, 1)
        self.item_editar = ToolButton('Editar', self.editar)
        self.insert(self.item_editar, 2)
        self.item_eliminar = ToolButton('Eliminar', self.eliminar)
        self.insert(self.item_eliminar, 3)
        self.item_imprimir = ToolButton('Imprimir', self.imprimir)
        self.insert(self.item_imprimir, 4)
        self.item_enviar = ToolButton('Enviar', self.enviar)
        self.insert(self.item_enviar, 5)
        self.item_info = ToolButton('Info', self.info)
        self.insert(self.item_info, 6)
        self.entry.connect('changed', self.filtrar)

    def filtrar(self, widget):
        self.widget.vista.filter.refilter()

    def set_text(self, texto):
        """Escribir el texto de busqueda"""
        self.entry.set_text(texto)

    def nuevo(self, *args):
        """Crear nuevo elemento"""
        texto = self.entry.get_text()
        self.widget.new_defaults()
        nuevo = Nuevo(self.widget, texto.title())
        nuevo.connect('save', self.widget.nuevo)
        print 'connect', nuevo, self.widget.nuevo
        return

    def editar(self, *args):
        """Modificar elemento"""
        return

    def eliminar(self, *args):
        """Eliminar elemnto"""
        return

    def imprimir(self, *args):
        """Imprimir"""
        return

    def enviar(self, *args):
        """Enviar por e-mail"""
        return

    def info(self, *args):
        """Ver más infomación"""
        return


class ToolButton(gtk.ToolButton):
    """Crear rápidamente ToolButton"""
    def __init__(self, image, funcion):
        """Constructor"""
        icon = gtk.Image()
        icon.set_from_file('econadmin/desktop/images/toolbar/%s.png' % image)
        super(ToolButton, self).__init__(icon, image)
        self.connect('clicked', funcion)


class Form:
    """Campo de Formulario"""
    def __init__(self, nombre, label, w):
        """Constructor"""
        self.name = nombre
        self.label = label
        self.widget = w

    def set_text(self, texto):
        self.widget.set_text(texto)

    def set_valor(self, texto):
        if type(texto) is str or type(texto) is int:
            self.widget.set_valor(texto)
        elif texto is None:
            return
        else:
            self.widget = EntryForeign(texto)


class Formulario(list):
    """Crea los widgets para formulario"""
    def __init__(self, modelo):
        """Constructor"""
        super(Formulario, self).__init__()
        campos = modelo._meta.fields
        size = 0
        for c in campos:
            nombre = c.name
            etiqueta = nombre.title()
            label = gtk.Label(etiqueta)
            if isinstance(c, fields.related.ForeignKey):
                modelo = c.rel.to
                w = EntryForeign(modelo)
            if isinstance(c, fields.CharField):
                w = EntryChar(c.max_length)
            if isinstance(c, fields.BigIntegerField):
                w = EntryInteger(c.max_length)
            if isinstance(c, fields.PositiveIntegerField):
                w = EntryInteger(10)
            if isinstance(c, fields.PositiveSmallIntegerField):
                w = EntryInteger(5)
            if isinstance(c, fields.URLField):
                w = EntryChar(c.max_length)
            if isinstance(c, fields.DecimalField):
                w = EntryDecimal(c.max_digits, c.decimal_places)
            if isinstance(c, fields.DateField):
                w = EntryDate()
            if isinstance(c, fields.DateTimeField):
                w = EntryDateTime()
            if c.editable and nombre != 'id':
                w.connect('activate', self.siguiente)
                size = max(len(etiqueta), size)
                widget = Form(nombre, label, w)
                self.append(widget)
        for e in self:
            e.label.set_size_request(size * 10, 25)

    def siguiente(self, widget):
        """Al presionar ENTER pasar al siguiente"""
        window = widget.get_toplevel()
        window.do_move_focus(window, gtk.DIR_TAB_FORWARD)


class EntryForeign(gtk.Entry):
    """Entry que buscar en la Tabla coincidencias"""
    def __init__(self, modelo):
        """Creador de Entry"""
        super(EntryForeign, self).__init__()
        self.modelo = modelo
        self.set_width_chars(20)
        self.connect('activate', self.buscar)
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFCCCC'))

    def buscar(self, *args):
        """Busca se existe una coincidencia sino abre dialogo"""
        texto = self.get_text()
        campos = self.modelo._meta.fields
        query = Q()
        for c in campos:
            if not isinstance(c, fields.related.ForeignKey):
                field = c.name
                q = Q(**{"%s__icontains" % field : texto})
                query = query | q
        elementos = self.modelo.objects.filter(query)
        if len(elementos) == 1:
            self.objeto = elementos[0]
            self.set_text(self.objeto.__str__())
            self.id = self.objeto.id
            self.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
        else:
            self.busqueda = Busqueda(self, texto)
            self.busqueda.connect('usar', self.usar)

    def nuevo(self, ventana):
        """Usar objeto desde la Ventana NUEVO"""
        self.objeto = ventana.objeto
        self.set_text(self.objeto.__str__())
        self.id = self.objeto.id
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
        ventana.destroy()
        self.busqueda.destroy()

    def usar(self, ventana):
        """Usar objeto desde Ventana BUSQUEDA"""
        self.objeto = self.busqueda.objeto
        self.set_text(self.objeto.__str__())
        self.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
        self.busqueda.destroy()

    def valor(self):
        """Devuelve el objeto escrito"""
        try:
            objeto = self.objeto
        except AttributeError:
            objeto = None
        return objeto

    def set_valor(self, texto):
        self.set_text(texto)
        self.buscar()


class EntryChar(gtk.Entry):
    """Entry que acepta texto"""
    def __init__(self, max_length):
        """Constructor"""
        super(EntryChar, self).__init__(max_length)
        self.set_width_chars(20)

    def valor(self):
        """Devuelve el texto"""
        return self.get_text()

    def set_valor(self, texto):
        self.set_text(texto)


class EntryInteger(gtk.Entry):
    """Entry que acepta sólo números"""
    def __init__(self, max_length):
        super(EntryInteger, self).__init__(max_length)
        self.set_width_chars(20)
        self.connect('key-press-event', self.key_press)

    def key_press(self, widget, event):
        key = event.keyval
        if (48 <= key and key <= 57) or (
            65456 <= key and key <= 65465) or (
            key == 65361 or key == 65363 or key == 65293) or (
            key == 65421 or key == 65307 or key == 65288):
            # 48 al 57 números,
            # 65456 al 65465 numpad
            # backspace = 65288
            # return = 65293 intro= 65421 escape=65307
            return False  # escribir
        else:
            print key
            return True  # terminar señal

    def valor(self):
        """Devuelve el número"""
        return int(self.get_text())

    def set_valor(self, texto):
        self.set_text(str(texto))


class EntryDecimal(gtk.Entry):
    """Entry que acepta sólo números"""
    def __init__(self, max_digits, decimal_places):
        super(EntryDecimal, self).__init__(max_digits + decimal_places + 1)
        self.set_width_chars(20)
        self.connect('key-press-event', self.key_press)

    def key_press(self, widget, event):
        key = event.keyval
        if (48 <= key and key <= 57) or (
            65456 <= key and key <= 65465) or (
            key == 65361 or key == 65363 or key == 65293) or (
            key == 65421 or key == 65307 or key == 65288):
            # números, return = 65293 intro= 65421 escape=65307
            return False  # escribir
        else:
            print key
            return True  # terminar señal

    def valor(self):
        """Devuelve el decimal"""
        return Decimal(self.get_text())

    def set_valor(self, texto):
        self.set_text(texto)


class EntryDate(gtk.Entry):
    """Entry que acepta sólo números"""
    def __init__(self,):
        super(EntryDate, self).__init__()
        self.set_width_chars(20)
        self.connect('key-press-event', self.key_press)
        self.connect('key-release-event', self.key_release)


    def key_press(self, widget, event):
        key = event.keyval
        if (48 <= key and key <= 57) or (
            65456 <= key and key <= 65465) or (
            key == 65361 or key == 65363 or key == 65293) or (
            key == 65421 or key == 65307):
            # números, return = 65293 intro= 65421 escape=65307
            return False  # escribir
        else:
            return True  # terminar señal

    def key_release(self, widget, event):
        return False

    def valor(self):
        """Devuelve la fecha"""
        return datetime.datetime(self.get_text())

    def set_valor(self, dias):
        fecha = datetime.date.today() + datetime.timedelta(dias)
        self.set_text(str(fecha))


class EntryDateTime(gtk.Entry):
    """Entry que acepta sólo números"""
    def __init__(self,):
        super(EntryDateTime, self).__init__()
        self.set_width_chars(20)
        self.connect('key-press-event', self.key_press)
        self.connect('key-release-event', self.key_release)

    def key_press(self, widget, event):
        key = event.keyval
        if (48 <= key and key <= 57) or (
            65456 <= key and key <= 65465) or (
            key == 65361 or key == 65363 or key == 65293) or (
            key == 65421 or key == 65307):
            # números, return = 65293 intro= 65421 escape=65307
            return False  # escribir
        else:
            return True  # terminar señal

    def key_release(self, widget, event):
        return False

    def set_valor(self, texto):
        self.set_text(str(texto))

class Busqueda(gtk.Dialog):
    """Búsqueda de elementos en una tabla"""
    __gsignals__ = {'usar': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ())}

    def __init__(self, entry, texto):
        """Constructor de Ventana"""
        super(Busqueda, self).__init__(
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        )
        self.modelo = entry.modelo
        titulo = self.modelo._meta.verbose_name
        self.set_title('Búsqueda: %s' % titulo)
        self.toolbar = Toolbar(entry)
        self.toolbar.set_text(texto)
        self.toolbar.entry.connect('changed', self.filtrar)
        self.vbox.pack_start(self.toolbar, False, False, 0)
        self.liststore = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
        self.actualizar()
        columnas = ("NOMBRE",)  # id
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.set_size_request(400, 150)
        self.vbox.pack_start(self.sw, True, True, 0)
        self.filter = self.liststore.filter_new()
        self.filter.set_visible_func(self.filtro)
        self.sort = gtk.TreeModelSort(self.filter)
        self.sort.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.treeview = gtk.TreeView(self.sort)
        self.treeview.connect('row-activated', self.usar)
        for i, columna in enumerate(columnas):
            cell = gtk.CellRendererText()
            tv = gtk.TreeViewColumn(columna)
            tv.pack_start(cell, True)
            tv.set_attributes(cell, text=i)
            self.treeview.append_column(tv)
        self.sw.add(self.treeview)
        self.show_all()

    def filtro(self, model, iter):
        nombre = model.get_value(iter, 0)
        texto = self.toolbar.entry.get_text()
        palabras = texto.split(' ')
        for p in palabras:
            if p.upper() in nombre.upper():
                return True
        return False

    def filtrar(self, widget):
        self.filter.refilter()

    def actualizar(self):
        """Actualizar la lista"""
        self.liststore.clear()
        elementos = self.modelo.objects.all()
        for e in elementos:
            self.liststore.append((
                e.__str__(),
                e))

    def usar(self, widget, path, column):
        self.objeto = self.sort[path][1]
        self.emit('usar')
        print 'usar', self, self.objeto



class Nuevo(gtk.Dialog):
    """Ventana de Creación de Nuevo para todas las tablas"""
    __gsignals__ = {'save': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ())}
    def __init__(self, widget, texto):
        """Creado de Ventana Nuevo"""
        super(Nuevo, self).__init__(
            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        )
        self.modelo = widget.modelo
        self.campos = Formulario(self.modelo)
        self.set_title('Nuevo ' + self.modelo._meta.verbose_name)
        self.set_defaults(widget.defaults)
        for e in self.campos:
            hbox = gtk.HBox(False, 0)
            self.vbox.pack_start(hbox)
            hbox.pack_start(e.label)
            hbox.pack_start(e.widget)
        self.campos[0].set_text(texto)
        but_guardar = gtk.Button('Guardar')
        self.action_area.pack_start(but_guardar)
        but_guardar.connect('clicked', self.guardar)
        self.show_all()

    def guardar(self, *args):
        """Guardar en Base de Datos"""
        self.objeto = self.modelo()
        for e in self.campos:
            print e.name, ': ', e.widget.valor()
            setattr(self.objeto, e.name, e.widget.valor())
        self.objeto.save()
        self.emit('save')
        print 'save', self

    def set_defaults(self, defaults):
        for i, campo in enumerate(self.campos):
            campo.set_valor(defaults[i])


class Vista(gtk.ScrolledWindow):
    """Navegador de elementos"""
    def __init__(self, widget):
        """Contructor"""
        super(Vista, self).__init__()
        self.store = widget.store
        self.modelo = widget.modelo
        self.columnas = widget.columnas
        self.atributos = widget.atributos
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.liststore = gtk.ListStore(*self.store)
        self.actualizar()
        self.filter = self.liststore.filter_new()
        self.filter.set_visible_func(self.filtro)
        self.sort = gtk.TreeModelSort(self.filter)
        self.sort.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.treeview = gtk.TreeView(self.sort)
        size = 0
        for i, columna in enumerate(self.columnas):
            size += len(columna)
            cell = gtk.CellRendererText()
            tv = gtk.TreeViewColumn(columna)
            tv.pack_start(cell, True)
            tv.set_attributes(cell, text=i)
            self.treeview.append_column(tv)
        self.add(self.treeview)
        self.set_size_request(size * 10, 150)

    def filtro(self, model, iter):
        """Búsqueda por Texto y Estado"""
        return True

    def actualizar(self):
        """Actualizar la lista"""
        self.liststore.clear()
        elementos = self.modelo.objects.select_related(depth=1).all()
        for r in elementos:
            fila = []
            for name in self.atributos:
                fila.append(getattr(r, name))
            fila.append(r)
            self.liststore.append(fila)

    def get_values(self):
        path, column = self.treeview.get_cursor()
        if path is None:
            return None
        path = int(path[0])
        return self.sort[path]


class Detalle(gtk.ScrolledWindow):
    """Navegador de elementos"""
    def __init__(self, widget):
        """Constructor"""
        super(Detalle, self).__init__()
        self.store = widget.store
        self.columnas = widget.columnas
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.label = gtk.Label('Detalle')
        self.add(self.label)
