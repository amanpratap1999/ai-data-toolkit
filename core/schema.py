"""
Pydantic data models for structured invoice parsing.
Provides strict validation and clean JSON schema generation for LLM prompting.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str = Field(description="Description of the good or service delivered")
    quantity: float = Field(default=1.0, description="Quantity or hours billed")
    unit_price: float = Field(description="Unit price or hourly rate")
    total_price: float = Field(description="Total price for this line item (quantity * unit_price)")


class InvoiceData(BaseModel):
    invoice_number: str = Field(description="Unique invoice number or reference code")
    issue_date: Optional[str] = Field(default=None, description="Date the invoice was issued")
    due_date: Optional[str] = Field(default=None, description="Due date or payment deadline")
    payment_terms: Optional[str] = Field(default=None, description="Payment terms e.g. Net 30, Due upon receipt")

    # Vendor Details
    vendor_name: str = Field(description="Name of the company or person issuing the invoice")
    vendor_address: Optional[str] = Field(default=None, description="Physical address of vendor")
    vendor_email: Optional[str] = Field(default=None, description="Email or contact info for vendor")

    # Customer Details
    customer_name: Optional[str] = Field(default="Guest / Walk-in Customer", description="Name of the client or company being billed")
    customer_address: Optional[str] = Field(default=None, description="Billing address of customer")
    customer_email: Optional[str] = Field(default=None, description="Customer contact email")

    # Financial Breakdown
    line_items: List[LineItem] = Field(default_factory=list, description="List of itemized goods or services")
    subtotal: Optional[float] = Field(default=None, description="Subtotal before taxes or discounts")
    discounts: float = Field(default=0.0, description="Any discounts applied")
    tax_amount: float = Field(default=0.0, description="Total tax or state surcharges")
    total_amount: float = Field(description="Final balance due / total invoice amount")
    currency: str = Field(default="USD", description="Currency code (e.g. USD, EUR, INR)")
