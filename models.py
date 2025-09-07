from peewee import CharField, IntegerField, AutoField, ForeignKeyField, DateField, DateTimeField, Model, TextField, DecimalField
from database import db_connection
import datetime
import hashlib
import json


class JSONField(TextField):
    def db_value(self, value):
        if value is not None:
           return json.dumps(value)
        return None
    def python_value(self, value):
        if value is not None:
            return json.loads(value)
        return None 

class BaseModel(Model):
    class Meta:
        database = db_connection
        
class Roles(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, unique=True, null=False)

class Users(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, null=False)
    email = CharField(max_length=255, null=False)
    password = CharField(max_length=255, null=False)
    phone = CharField(max_length=20, null=False)
    role_id = ForeignKeyField(Roles, on_delete='CASCADE', backref='user_role', on_update='CASCADE')
    address = TextField(null=True)

class PasswordChangeRequest(BaseModel):
    id = AutoField()
    user = ForeignKeyField(Users, backref='user_change', on_delete='CASCADE', null=False)
    code = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.datetime.now())
    expires_at = DateTimeField()

class UserToken(BaseModel):
    id = AutoField()
    user_id = ForeignKeyField(Users, on_delete='CASCADE', null=False, backref='us_token', on_update='CASCADE')
    token = CharField(max_length=255, null=False)
    created_at = DateTimeField(default=datetime.datetime.now(), null=False)
    expires_at = DateTimeField(null=False)

class Manufactures(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, null=False, unique=True)

class ComponentsTypes(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, null=False)
    description = TextField(null=True)

class Components(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, null=False)
    type_id = ForeignKeyField(ComponentsTypes, on_delete='SET NULL', null=True, backref='type_comp', on_update='CASCADE')
    manufactures_id = ForeignKeyField(Manufactures, on_delete='SET NULL', null=True, backref='man_comp', on_update='CASCADE')
    price = DecimalField(max_digits=15, decimal_places=2, null=False)
    stock_quantity = IntegerField(null=True, default=0)
    specification = JSONField(null=True)

class Configurations(BaseModel):
    id = AutoField()
    user_id = ForeignKeyField(Users, on_delete='CASCADE', backref='user_config', on_update='CASCADE')
    name_config = CharField(max_length=255, null=True)
    description = TextField(null=True)
    created_at = DateField(default=datetime.datetime.now())

class ConfigurationsComponents(BaseModel):
    id = AutoField()
    configuration_id = ForeignKeyField(Configurations, on_delete='CASCADE', backref='config_components', on_update='CASCADE')
    components_id = ForeignKeyField(Components, on_delete='CASCADE', backref='component_config', on_update='CASCADE')
    quantity = IntegerField(null=False, default=1)

class OrdersStatus(BaseModel):
    id = AutoField()
    name = CharField(max_length=255, null=False, unique=True)

class Orders(BaseModel):
    id = AutoField()
    user_id = ForeignKeyField(Users, on_delete='CASCADE', backref='order_user', on_update='CASCADE')
    order_date = DateTimeField(null=False, default=datetime.datetime.now())
    total_amout = DecimalField(max_digits=15, decimal_places=2, null=False)
    status_id = ForeignKeyField(OrdersStatus, on_delete='CASCADE', backref='order_status', on_update='CASCADE')

class OrderConfigurations(BaseModel):
    id = AutoField()
    order_id = ForeignKeyField(Orders, on_delete='CASCADE', backref='order_config', on_update='CASCADE')
    configuration_id = ForeignKeyField(Configurations, on_delete='CASCADE', backref='config_con', on_update='CASCADE')
    quantity = IntegerField(null=False, default=1)
    price_at_time = DecimalField(max_digits=15, decimal_places=2, null=False)

tables = [Roles,
          Users,
          PasswordChangeRequest,
          UserToken,
          Manufactures,
          ComponentsTypes,
          Components,
          Configurations,
          ConfigurationsComponents,
          OrdersStatus,
          Orders,
          OrderConfigurations]

def init_tables():
    try:
        db_connection.create_tables(tables, safe=True)
        print(f'Таблицы успешно созданы. Количество: {len(tables)}.')
    except Exception as e:
        print(f'Ошибка при создании таблиц: {e}.')

init_tables()
    
    
    
    