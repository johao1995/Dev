from odoo import models,api,fields
from datetime import date

class Presupuesto(models.Model):
    _name='movies.presupuesto'
    _description='Presupuesto de Peliculas'

    name=fields.Char(string="Nombre",size=100)
    clasification=fields.Selection(string="Clasificacion",selection=[
        ('G','G'),#Publico General
        ('PG','PG'),#Se recomienda compañia de un adulto
        ('PG-13','PG-13'),#Mayores de 13
        ('R','R'),#En compañia de un adulto obligatorio
        ('NC-17','NC-17'),#Mayores de 18

    ],default="G")
    date_streno=fields.Date(string="Fecha Estreno")
    puntuacion=fields.Integer(string="Puntuacion",related="puntuacion2")
    puntuacion2=fields.Integer(string="Puntuacion2")
    active=fields.Boolean(string="Estado")
    director_id=fields.Many2one(string="Director",comodel_name="res.partner")
    genero_ids=fields.Many2many(string="Genero",comodel_name="movies.genero")
    category_director_id=fields.Many2one(string="Categoria",comodel_name="movies.category.operarios",
                                         default=lambda self:self.env.ref('movies.movies_category_operarios_director'))
    #domain=[('name','=','Director')]
    #  default=lambda self:self.env['movies.category.operarios'].search(['name','=','Director']))
    description=fields.Text(string="Description")
    image=fields.Binary(string="Imagen")
    link_trailer=fields.Char(string="Link")
    is_book=fields.Boolean(string="Version Libro")
    book_pdf=fields.Binary(string="Libro")
    state=fields.Selection(string="Estado Presupuesto",selection=[
        ('aprobado','Aprobado'),
        ('borrador','Borrador')
    ],default="borrador")
    name_clasification=fields.Char()
    date_aprob=fields.Date(string="Fecha Aprobado")
    date_creation=fields.Date(string="Fecha Creacion")
    factura=fields.Char(string="Factura")
    comment=fields.Html(string="Comentario")
    detail_id=fields.One2many(string="Detalles",comodel_name="movies.detail.presupuesto",inverse_name="presupuesto_id")
    currency_id=fields.Many2one(string="Moneda",comodel_name="res.currency",default=lambda self:self.env.company.currency_id.id)
    importe_base=fields.Monetary(string="Importe Base",compute="compute_total")
    impuesto=fields.Monetary(string="Impuesto",compute="compute_total")
    total=fields.Monetary(string="Total",compute="compute_total")

    def compute_total(self):
        importe=0
        for rec in self:
            for i  in rec.detail_id:
                importe+=i.importe
        
            rec.importe_base=importe
            rec.impuesto=rec.importe_base*0.18
            rec.total=rec.importe_base+rec.impuesto

    @api.onchange('clasification')
    def onchange_name_clasification(self):
        if self.clasification:
            if self.clasification=='G':
                self.name_clasification='Publico General'
            elif self.clasification=='PG':
                self.name_clasification='Se recomienda compañia de un adulto'
            elif self.clasification=='PG-13':
                self.name_clasification='Mayores de 13'
            elif self.clasification=='R':
                self.name_clasification='En compañia de un adulto obligatorio'
            elif self.clasification=='NC-17':
                self.name_clasification='Mayores de 18'
        else:
            self.clasification=False

    def Aprobado(self):
        self.state="aprobado"
        self.date_aprob=date.today()

    def Borrador(self):
        self.state="borrador"

    @api.model
    def create(self,value):
        obj_factura=self.env['ir.sequence'].next_by_code('movies.presupuesto')

        print(obj_factura)
        value['factura']=obj_factura
        value['date_creation']=date.today()
        return super(Presupuesto,self).create(value)