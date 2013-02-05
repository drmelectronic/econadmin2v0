# -*- coding: utf-8 -*-

class Trabajador(models.Model):
    """Datos adicionales del Usuario"""
    user = models.ForeignKey(User, unique=True)
    persona = models.ForeignKey(Persona)
    nacimiento = models.DateField()
    ingreso = models.DateField()
    fin = models.DateField(null=True)
    activo = models.BooleanField()
    password = models.CharField(max_length=8)
    rol = models.ForeignKey(TrabajadorRol)
    partida = models.ForeignKey('Partida')
    asignacion = models.BooleanField(default=False)
    tipo = models.ForeignKey('TrabajadorTipo')
    afp = models.ForeignKey('AFP', null=True)
    cuspp = models.CharField(max_length=16, null=True)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.persona.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"



class Direccion(models.Model):
    """Direcciones"""
    nombre = models.CharField(max_length=128)
    distrito = models.ForeignKey(DirDistrito)
    postal = models.PositiveIntegerField(null=True)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ['nombre']


# Teléfonos


class Telefono(models.Model):
    """Telefonos de Empresas, Contactos y Personal"""
    numero = models.BigIntegerField()
    red = models.CharField(max_length=10, null=True)
    operador = models.ForeignKey(TelefonoOperador)
    tipolinea = models.ForeignKey(TelefonoTipo)
    usotelefono = models.ForeignKey(TelefonoUso)
    direccion = models.ForeignKey(Direccion)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.numero

    class Meta:
        """Configuraciones"""
        verbose_name = "Teléfono"
        verbose_name_plural = "Teléfonos"


# Correo



class Correo(models.Model):
    """Correo de personas"""
    nombre = models.EmailField(max_length=64)
    tipo = models.ForeignKey(CorreoTipo)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Correo"
        verbose_name_plural = "Correos"


# Monedas y Finanzas



class Cuenta(models.Model):
    """Cuentas en los bancos de Empresa y Personas"""
    numero = models.CharField(max_length=16)
    cci = models.CharField(max_length=23)
    tipo = models.ForeignKey(CuentaTipo)
    moneda = models.ForeignKey(Moneda)
    banco = models.ForeignKey(Banco)
    partida = models.ForeignKey('Partida')

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.banco.nombre + ' ' + self.moneda.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

# Vehículos, Empresas, Personas



class Vehiculo(models.Model):
    """Todos los vehiculos"""
    placa = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.placa

    class Meta:
        """Configuraciones"""
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"


class Empresa(models.Model):
    """Datos de Empresas"""
    razon = models.CharField(max_length=128)  # comercial si tipo=Marca
    comercial = models.CharField(max_length=32)  # codigo si tipo=Marca
    ruc = models.BigIntegerField(null=True, max_length=11)
    web = models.URLField(max_length=128, null=True)
    direcciones = models.ManyToManyField(Direccion)
    telefonos = models.ManyToManyField(Telefono)
    cuentas = models.ManyToManyField(Cuenta)
    vehiculos = models.ManyToManyField(Vehiculo)
    tipo = models.ForeignKey(EmpresaTipo)
    partida = models.ForeignKey('Partida')

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.comercial

    class Meta:
        """Configuraciones"""
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['comercial']


class Persona(models.Model):
    """Personas"""
    nombre = models.CharField(max_length=16)
    segundo = models.CharField(max_length=16)
    apellidos = models.CharField(max_length=128)
    titulo = models.CharField(max_length=5, null=True)
    sexo = models.ForeignKey(Sexo)
    estado_civil = models.ForeignKey(EstadoCivil)
    dni = models.BigIntegerField()
    licencia = models.CharField(max_length=9)
    direcciones = models.ManyToManyField(Direccion)
    telefonos = models.ManyToManyField(Telefono)
    correos = models.ManyToManyField(Correo)
    cuentas = models.ManyToManyField(Cuenta)
    vehiculos = models.ManyToManyField(Vehiculo)
    empresa = models.ForeignKey(Empresa)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    def _get_formal(self):
        """Nombre formal para documentos"""
        if self.titulo is None:
            return "%s %s" % (self.nombre, self.apellidos)
        return "%s. %s %s" % (self.titulo, self.nombre, self.apellidos)

    def _get_dni(self):
        """Completar de ceros el DNI"""
        return str(self.dni).zfill(8)

    def _get_completo(self):
        """Nombre completo para Cheques, Contratos, etc"""
        return "%s %s %s" % (self.nombre, self.segundo, self.apellidos)

    class Meta:
        """Configuraciones"""
        verbose_name = "Persona"
        verbose_name_plural = "Personal"


# Acceso de Usuarios


# Almacén




class StockInsumo(models.Model):
    """Insumos para fabricación de Equipos"""
    componente = models.ForeignKey('StockModelo')
    cantidad = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.componente.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"


class StockModelo(models.Model):
    """Modelos de Componentes y Equipos"""
    nombre = models.CharField(max_length=32)
    codigo = models.CharField(max_length=8)
    marca = models.ForeignKey(Empresa)
    sumar = models.BooleanField(default=True)  # No importa marca
    insumos = models.ManyToManyField(StockInsumo)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"


class StockModeloProcedimiento(models.Model):
    """Procedimiento -> Datos"""
    procedimiento = models.ForeignKey(StockProcedimiento)
    modelo = models.ForeignKey(StockModelo)
    tiempo = models.PositiveSmallIntegerField()
    #problema

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.procedimiento.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"


class StockPropiedad(models.Model):
    """Propiedades de los Componentes y Equipos"""
    nombre = models.CharField(max_length=16)
    imprimir = models.BooleanField(default=False)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"


class StockCategoria(models.Model):
    """Clasificación de Componentes y Equipos"""
    nombre = models.CharField(max_length=32)
    padre = models.ForeignKey('self', blank=True)
    propiedades = models.ManyToManyField(StockPropiedad)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class StockPrecio(models.Model):
    """Precios de los Componentes y Equipos"""
    valor = models.DecimalField(max_digits=10, decimal_places=3)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    proveedor = models.ForeignKey(Empresa)
    modelo = models.ForeignKey(StockModelo)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.valor

    class Meta:
        """Configuraciones"""
        verbose_name = "Precio"
        verbose_name_plural = "Precios"


class Stock(models.Model):
    """"Componentes y Equipos en nuestro Almacén"""
    serie = models.CharField(max_length=16, null=True)
    cantidad = models.DecimalField(max_digits=7, decimal_places=3)
    modelo = models.ForeignKey(StockModelo)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        if self.serie is None:
            return self.modelo.nombre
        return self.serie

    def get_codigo(self):
        """Obtener el código único del equipo"""
        if self.serie is None:
            return self.modelo.nombre
        return self.serie + ' / ' + self.modelo.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class StockServicioTipo(models.Model):
    """Venta, Reparación, Mantenimiento"""
    nombre = models.CharField(max_length=16)
    procedimientos = models.ManyToManyField(StockProcedimiento)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"


class StockServicio(models.Model):
    """Servicios: reparaciones, cambios, hechos a un equipo"""
    servicio = models.ForeignKey(StockServicioTipo)
    modelo = models.ForeignKey(StockModelo)
    fecha = models.DateField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.servicio.nombre + '/' + self.modelo.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Servicio"
        verbose_name_plural = "Servicio"


class StockMovimiento(models.Model):
    """Entradas a Salidas de Componentes y Equipos"""
    modelo = models.ForeignKey(StockModelo)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    entrada = models.BooleanField()  # True=Entrada, False=Salida
    fecha = models.DateTimeField(default=datetime.now)
    log = models.CharField(max_length=32)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        if not entrada:
            cantidad = self.cantidad * -1
        else:
            cantidad = self.cantidad
        return self.modelo.nombre + ' (' + cantidad + ')'

    class Meta:
        """Configuraciones"""
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"


# Requerimientos


class RequerimientoEstado(models.Model):
    """Recibido, Cotizado, Anulado"""
    nombre = models.CharField(max_length=8)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class Requerimiento(models.Model):
    """Requerimiento recibidos para cotizar"""
    empresa = models.ForeignKey(Empresa)
    contacto = models.ForeignKey(Persona)
    cotizar = models.ForeignKey(Trabajador)
    tipo = models.ForeignKey(StockServicioTipo)
    estado = models.ForeignKey(RequerimientoEstado, editable=False, default=1)
    fecha = models.DateTimeField(default=datetime.now)
    #garantia = Boolean

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.fecha

    class Meta:
        """Configuraciones"""
        verbose_name = "Requerimiento"
        verbose_name_plural = "Requerimientos"


class RequerimientoItem(models.Model):
    """Líneas de cada Requerimiento"""
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    descripcion = models.CharField(max_length=256)
    requerimiento = models.ForeignKey(Requerimiento)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.descripcion

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


# Cotizaciones


class CotizacionEstado(models.Model):
    """Cotizado, Enviado, Aceptado, Anulado"""
    nombre = models.CharField(max_length=8)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class CotizacionGarantia(models.Model):
    """3 meses, 1 año, 1 año por defecto..., etc"""
    nombre = models.CharField(max_length=256)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"


class CotizacionPago(models.Model):
    """Al Contado, Adelanto, ..."""
    nombre = models.CharField(max_length=32)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"


class CotizacionPlazo(models.Model):
    """5 días, 7 días útiles, ..."""
    nombre = models.CharField(max_length=32)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Plazo"
        verbose_name_plural = "Plazos"


class CotizacionValidez(models.Model):
    """15 días, 1 meses, etc"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Validez"
        verbose_name_plural = "Validez"


class CotizacionAtencion(models.Model):
    """Atencion, CC, CCO, CCOO"""
    nombre = models.CharField(max_length=8)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Atención"
        verbose_name_plural = "Atención"


class Cotizacion(models.Model):
    """Cotizaciones"""
    codigo = models.PositiveSmallIntegerField()
    fecha = models.DateField()
    requerimiento = models.ForeignKey(Requerimiento)
    estado = models.ForeignKey(CotizacionEstado)
    plazo = models.ForeignKey(CotizacionPlazo, null=True)
    garantia = models.ForeignKey(CotizacionGarantia, null=True)
    validez = models.ForeignKey(CotizacionValidez, null=True)
    pago = models.ForeignKey(CotizacionPago, null=True)
    moneda = models.ForeignKey(Moneda)
    firma = models.ForeignKey(Trabajador)
    observacion = models.CharField(max_length=256)
    atencion = models.ManyToManyField(Persona, through='CotizacionPersona')

    def get_codigo(self):
        """Devuelve en formato 12-056"""
        return '%d-%d' % (self.fecha.year, self.codigo)

    def __str__(self):
        """Devuelve el resumen de la cotizacion"""
        return self.codigo

    def get_total(self):
        """Devuelve el monto total"""
        return

    class Meta:
        """Configuraciones"""
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"


class CotizacionItem(models.Model):
    """Líneas de cada cotizacion"""
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    modelo = models.ForeignKey(StockModelo, null=True)
    servicio = models.ForeignKey(StockServicioTipo)
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    cotizacion = models.ForeignKey(Cotizacion)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.servicio.nombre + '/' + self.modelo.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


class CotizacionPersona(models.Model):
    """Contactos que recibiran la Cotización"""
    cotizacion = models.ForeignKey(Cotizacion)
    persona = models.ForeignKey(Persona)
    tipo = models.ForeignKey(CotizacionAtencion)
    orden = models.PositiveSmallIntegerField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.persona.nombre


    class Meta:
        """Configuraciones"""
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

# Guías de Entrada / Salida


class GuiaMotivo(models.Model):
    """Motivos para traslados de bienes en guías"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Motivo"
        verbose_name_plural = "Motivos"


class GuiaEntrada(models.Model):
    """Guías de Entrada Clientes y Proveedores"""
    codigo = models.CharField(max_length=10)
    fecha = models.DateField()
    motivo = models.ForeignKey(GuiaMotivo)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.codigo

    class Meta:
        """Configuraciones"""
        verbose_name = "Guía Entrada"
        verbose_name_plural = "Guías Entrada"


class GuiaEstado(models.Model):
    """Borrador, Impresa, Aceptada, Anulada"""
    nombre = models.CharField(max_length=8)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class GuiaSalida(models.Model):
    """Guías de Salida de la Empresa"""
    serie = models.PositiveSmallIntegerField()
    numero = models.PositiveIntegerField()
    fecha = models.DateField()
    observacion = models.CharField(max_length=64)
    estado = models.ForeignKey(GuiaEstado)
    direccion = models.ForeignKey(Direccion)
    motivo = models.ForeignKey(GuiaMotivo)
    cotizacion = models.ForeignKey(Cotizacion)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.fecha

    def get_codigo(self):
        """Devuelve en formato 001-00564"""
        return str(self.serie).zfill(3) + '-' + str(self.numero).zfill(6)

    class Meta:
        """Configuraciones"""
        verbose_name = "Guía Salida"
        verbose_name_plural = "Guías Salida"


# Facturación


class FacturaEstado(models.Model):
    """Borrador, Impresa, Aceptada, Anulada"""
    nombre = models.CharField(max_length=8)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class Factura(models.Model):
    """Facturas Emitidas"""
    serie = models.PositiveSmallIntegerField()
    numero = models.PositiveIntegerField()
    fecha = models.DateField()
    estado = models.ForeignKey(FacturaEstado)
    cotizacion = models.ForeignKey(Cotizacion)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.fecha)

    def _get_codigo(self):
        return str(self.serie).zfill(3) + '-' + str(self.numero).zfill(6)

    class Meta:
        """Configuraciones"""
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"


class FacturaItem(models.Model):
    """Líneas de cada factura"""
    item = models.ForeignKey(CotizacionItem)
    factura = models.ForeignKey(Factura)
    opcional = models.CharField(max_length=1024, null=True)

    def __str__(self):
        """Devuelve texto de la linea a imprimir"""
        if self.opcional is None:
            return
        return self.opcional

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


# Contabilidad


class Comprobante(models.Model):
    """Codificacion aprobada por SUNAT"""
    codigo = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=16)
    descripcion = models.CharField(max_length=512)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Comprobante"
        verbose_name_plural = "Comprobantes"


class CompraRegla(models.Model):
    """Neto, Total, Total - NG, Neto - NG, Aduana, Zona Rigida"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Regla"
        verbose_name_plural = "Reglas"


class Compra(models.Model):
    """Facturas, Boletas, Nota de Credito, etc"""
    fecha = models.DateField()
    tipo = models.ForeignKey(Comprobante)
    serie = models.PositiveSmallIntegerField()
    numero = models.PositiveIntegerField()
    proveedor = models.ForeignKey(Empresa)
    moneda = models.ForeignKey(Moneda)
    gravado = models.DecimalField(max_digits=10, decimal_places=2)
    no_gravado = models.DecimalField(max_digits=10, decimal_places=2)
    igv = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    regla = models.ForeignKey(CompraRegla)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.fecha)

    class Meta:
        """Configuraciones"""
        verbose_name = "Compra"
        verbose_name_plural = "Compras"


class CompraItem(models.Model):
    """Detalle de facturas"""
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    modelo = models.ForeignKey(StockModelo)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    factura = models.ForeignKey(Compra)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.modelo.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


class Percepcion(models.Model):
    """Percepciones pagadas"""
    serie = models.PositiveSmallIntegerField()
    numero = models.PositiveIntegerField()
    fecha = models.DateField()
    proveedor = models.ForeignKey(Empresa)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.fecha)

    class Meta:
        """Configuraciones"""
        verbose_name = "Percepción"
        verbose_name_plural = "Percepciones"


class ItemPercepcion(models.Model):
    """Compras con percepcion y monto"""
    factura = models.ForeignKey(Compra, unique=True)
    percepcion = models.ForeignKey(Percepcion)
    percibido = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.percibido)

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


class Retencion(models.Model):
    """Retenciones recibidas"""
    serie = models.PositiveSmallIntegerField()
    numero = models.PositiveIntegerField()
    fecha = models.DateField()
    cliente = models.ForeignKey(Empresa)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.fecha)

    class Meta:
        """Configuraciones"""
        verbose_name = "Retención"
        verbose_name_plural = "Retenciones"


class ItemRetencion(models.Model):
    """Compras con percepcion y monto"""
    factura = models.ForeignKey(Compra, unique=True)
    retencion = models.ForeignKey(Retencion)
    retenido = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.retenido)

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


class Detraccion(models.Model):
    """Detracciones depositadas"""
    numero = models.BigIntegerField()
    usuario = models.CharField(max_length=8, null=True)
    cliente = models.ForeignKey(Empresa)
    periodo = models.DateField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.numero

    class Meta:
        """Configuraciones"""
        verbose_name = "Detracción"
        verbose_name_plural = "Detracciones"


class DetraccionItem(models.Model):
    """Facturas consideradas en la detraccion"""
    factura = models.ForeignKey(Factura, unique=True)
    detraccion = models.ForeignKey(Detraccion)
    detraido = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.detraido)

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


class Honorarios(models.Model):
    """Recibos por honorarios"""
    fecha = models.DateField()
    serie = models.PositiveSmallIntegerField()
    numero = models.PositiveIntegerField()
    proveedor = models.ForeignKey(Empresa)
    moneda = models.ForeignKey(Moneda)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    retenido = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cancelado = models.DateField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.fecha)

    class Meta:
        """Configuraciones"""
        verbose_name = "Recibo Honorario"
        verbose_name_plural = "Recibos Honorario"


class BalanceMes(models.Model):
    """Resultado de Compras Ventas"""
    periodo = models.DateField()
    percepcion = models.BooleanField()
    retencion = models.BooleanField()
    retencion_tercera = models.BooleanField()
    ventas = models.PositiveIntegerField()
    exportacion = models.PositiveIntegerField()
    compras = models.PositiveIntegerField()
    no_gravadas = models.PositiveIntegerField()
    importaciones = models.PositiveIntegerField()
    renta = models.DecimalField(max_digits=3, decimal_places=2)
    saldo_tributo = models.PositiveIntegerField()
    saldo_retencion = models.PositiveIntegerField()
    saldo_percepcion = models.PositiveIntegerField()

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.periodo)

    class Meta:
        """Configuraciones"""
        verbose_name = "Balance"
        verbose_name_plural = "Balances"


# Finanzas


class Partida(models.Model):
    """Árbol de clasificacion de Partidas contables
    Inicio: Activo, Pasivo, Ingreso, Egreso, Patrimonio"""
    nombre = models.CharField(max_length=32)
    parent = models.ForeignKey('self', null=True, default=None)
    soles = models.DecimalField(max_digits=10, decimal_places=2,
        default=Decimal('0.0'), editable=False)
    dolares = models.DecimalField(max_digits=10, decimal_places=2,
        default=Decimal('0.0'), editable=False)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"


class PartidaItem(models.Model):
    """Asiento contable"""
    fecha = models.DateTimeField(default=datetime.now)
    descripcion = models.CharField(max_length=32)
    padre = models.ForeignKey(Partida, related_name='padre')
    viene = models.ForeignKey(Partida, related_name='viene')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    log = models.CharField(max_length=32)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.descripcion

    class Meta:
        """Configuraciones"""
        verbose_name = "Ítem"
        verbose_name_plural = "Ítems"


class ChequeEstado(models.Model):
    """Borrador, Impreso, Anulado"""
    nombre = models.CharField(max_length=8)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estado"


class Cheque(models.Model):
    """Listado de cheques"""
    numero = models.BigIntegerField(max_length=8)
    fecha = models.DateField(default=datetime.now)
    desde = models.DateField(default=datetime.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nombre = models.CharField(max_length=64)
    cuenta = models.ForeignKey(Cuenta)
    estado = models.ForeignKey(ChequeEstado, editable=False, default=1)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Cheque"
        verbose_name_plural = "Cheque"


# Planilla


class AFP(models.Model):
    """AFPs"""
    nombre = models.CharField(max_length=16)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "AFP"
        verbose_name_plural = "AFPs"


class TrabajadorTipo(models.Model):
    """Según SUNAT"""
    nombre = models.CharField(max_length=32)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tipo"
        verbose_name_plural = "Tipo"


class PlanillaSueldo(models.Model):
    """Sueldo y datos por periodo"""
    trabajador = models.ForeignKey(Trabajador)
    periodo = models.DateField()
    permanente = models.DecimalField(max_digits=7, decimal_places=2)
    asignacion = models.DecimalField(max_digits=7, decimal_places=2)
    bonificacion = models.DecimalField(max_digits=7, decimal_places=2)
    gratificacion = models.DecimalField(max_digits=7, decimal_places=2)
    comision = models.DecimalField(max_digits=7, decimal_places=2)
    prima = models.DecimalField(max_digits=7, decimal_places=2)
    aporte = models.DecimalField(max_digits=7, decimal_places=2)
    onp = models.DecimalField(max_digits=7, decimal_places=2)
    essalud = models.DecimalField(max_digits=7, decimal_places=2)
    retencion = models.DecimalField(max_digits=7, decimal_places=2)
    descuentos = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.periodo + '/' + self.trabajador.persona.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Sueldo"
        verbose_name_plural = "Sueldo"


# Proyectos


class TareaEstado(models.Model):
    """Planificado, Iniciado, Terminado, Cancelado"""
    nombre = models.CharField(max_length=16)
    color = models.CharField(max_length=7)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class Tarea(models.Model):
    """Tareas que tiene que hacer el personal"""
    nombre = models.CharField(max_length=32)
    trabajador = models.ForeignKey(Trabajador)
    procedimiento = models.ForeignKey(StockModeloProcedimiento)
    tiempo = models.PositiveSmallIntegerField()
    estado = models.ForeignKey(TareaEstado)

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return self.nombre

    class Meta:
        """Configuraciones"""
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"


class Proyecto(models.Model):
    """Planificacion de ejecución de un Trabajo"""
    nombre = models.CharField(max_length=32)
    cotizacion = models.ForeignKey(Cotizacion)
    responsable = models.ForeignKey(Trabajador)
    tareas = models.ManyToManyField(Tarea)

    class Meta:
        """Configuraciones"""
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"


class Jornada(models.Model):
    """Hora de Entrada Salida"""
    trabajador = models.ForeignKey(Trabajador)
    fecha = models.DateField(auto_now=True)
    inicio = models.TimeField(auto_now=True)
    fin = models.TimeField(time(18))

    def __str__(self):
        """Usar nombre en lugar de ID al imprimir"""
        return str(self.fecha)

    class Meta:
        """Configuraciones"""
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"
