# Import all models to ensure SQLAlchemy can resolve relationships
from app.models.owner import Owner
from app.models.customer import Customer
from app.models.pass_type import PassType
from app.models.pass_field import PassField
from app.models.pass_model import PassModel
from app.models.customer_pass import CustomerPass
from app.models.stamp import Stamp
from app.models.reward import Reward

__all__ = [
    "Owner",
    "Customer", 
    "PassType",
    "PassField",
    "PassModel",
    "CustomerPass",
    "Stamp",
    "Reward"
]