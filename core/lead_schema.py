"""
Pydantic data models for structured business lead extraction and data cleaning.
Features:
- Deterministic phone number normalization (E.164 and standard US format)
- Automatic website domain enrichment from business emails
- Email string sanitization
- Automated CRM Lead Completeness Scoring (0 to 100%)
"""

import re
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


def clean_phone_number(raw_phone: Optional[str]) -> Optional[str]:
    """Sanitizes raw phone strings into clean formatted telephone numbers."""
    if not raw_phone:
        return None
    # Extract only digits and leading plus
    digits = re.sub(r"[^\d]", "", raw_phone)
    if not digits:
        return None

    # Handle standard 10-digit US/Canada numbers
    if len(digits) == 10:
        return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith("1"):
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    elif len(digits) >= 10:
        return f"+{digits}"
    return raw_phone.strip()


def infer_website_from_email(email: Optional[str], current_website: Optional[str]) -> Optional[str]:
    """Infers company website from business email if website is missing."""
    if current_website and current_website.lower() not in ("n/a", "none", ""):
        return current_website

    if not email or "@" not in email:
        return None

    domain = email.split("@")[-1].strip().lower()
    # Skip generic consumer email providers
    GENERIC_DOMAINS = {
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "icloud.com", "aol.com", "protonmail.com", "zoho.com"
    }
    if domain in GENERIC_DOMAINS:
        return None

    return f"https://www.{domain}"


class BusinessLead(BaseModel):
    company_name: str = Field(description="Name of the business or practice / firm")
    contact_name: Optional[str] = Field(default=None, description="Primary contact person name")
    title_or_role: Optional[str] = Field(default=None, description="Title, role, or credentials e.g. CEO, MD, DDS, Partner")
    
    # Contact Info
    primary_email: Optional[str] = Field(default=None, description="Primary email address")
    secondary_email: Optional[str] = Field(default=None, description="Secondary or alternate email if found")
    phone: Optional[str] = Field(default=None, description="Sanitized telephone number")
    website: Optional[str] = Field(default=None, description="Website URL including https:// if present")

    # Address Breakdown
    street_address: Optional[str] = Field(default=None, description="Street and suite/floor number")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="2-letter state code or province")
    postal_code: Optional[str] = Field(default=None, description="ZIP or postal code")

    # Business Intelligence
    specialties: List[str] = Field(default_factory=list, description="List of primary services or practice areas")
    notes: Optional[str] = Field(default=None, description="Additional context e.g. hours, insurance, fee schedule")

    @field_validator("primary_email", "secondary_email", mode="before")
    @classmethod
    def sanitize_email(cls, v):
        if not v or not isinstance(v, str):
            return None
        # Clean trailing punctuation, semicolons, mailto: prefixes
        cleaned = re.sub(r"^mailto:", "", v.strip(), flags=re.IGNORECASE)
        cleaned = cleaned.strip(";, \t\r\n")
        # If multiple emails in string, take the first valid one
        if ";" in cleaned or "," in cleaned:
            parts = [p.strip() for p in re.split(r"[;,]", cleaned) if "@" in p]
            cleaned = parts[0] if parts else cleaned
        return cleaned.lower() if "@" in cleaned else None

    @field_validator("phone", mode="before")
    @classmethod
    def sanitize_phone(cls, v):
        return clean_phone_number(v)

    def model_post_init(self, __context):
        # Auto-enrich website from email domain if missing
        if not self.website:
            inferred = infer_website_from_email(self.primary_email, self.website)
            if inferred:
                self.website = inferred

    @property
    def completeness_score(self) -> int:
        score = 0
        if self.company_name:
            score += 15
        if self.primary_email and "@" in self.primary_email:
            score += 30
        if self.phone and len(self.phone) >= 7:
            score += 20
        if self.contact_name or self.title_or_role:
            score += 15
        if self.website:
            score += 10
        if self.city or self.state or self.street_address:
            score += 10
        return min(score, 100)

    @property
    def quality_tier(self) -> str:
        score = self.completeness_score
        if score >= 80:
            return "HIGH QUALITY"
        if score >= 50:
            return "MEDIUM"
        return "INCOMPLETE"


class LeadDirectory(BaseModel):
    leads: List[BusinessLead] = Field(default_factory=list, description="List of parsed business lead records")
