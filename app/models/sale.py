from pydantic import BaseModel , Field ,ConfigDict
from datetime import date

class Sale(BaseModel):
    product_id: int
    quantity: int
    sale_date: date
    total_value: float
    
    model_config = ConfigDict(
        populate_by_name= True,
        arbitrary_types_allowed=True,
      )