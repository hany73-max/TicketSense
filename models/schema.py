from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import VARCHAR, DATE, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Customers(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    customer_email: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    customer_age: Mapped[int] = mapped_column(nullable=False)
    customer_gender: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)

    tickets: Mapped[List["Tickets"]] = relationship(back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.customer_id}, name='{self.customer_name}')>"


class Tickets(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=False)
    ticket_type: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    ticket_subject: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    ticket_description: Mapped[str] = mapped_column(String, nullable=False)
    ticket_status: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    product_purchased: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    date_of_purchase: Mapped[date] = mapped_column(DATE, nullable=False)

    resolution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ticket_priority: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    ticket_channel: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)
    first_response_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    time_to_resolution: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    customer_satisfaction_rating: Mapped[Optional[int]] = mapped_column(nullable=True)

    customer: Mapped["Customers"] = relationship(back_populates="tickets")

    def __repr__(self):
        return f"<Ticket(id={self.ticket_id}, subject='{self.ticket_subject}')>"