from fastapi import FastAPI

from app.customer.controllers import customer_controller
from app.customer.services.customer_service import CustomerService
from app.customer.repositories.customer_repository import CustomerRepository
from app.database import models, database
from app.health.controllers import health_controller
from app.health.services.health_service import HealthService


class Initializer:
    def __init__(self, app: FastAPI):
        self.app = app
        self.customer_service = None

    def setup(self):
        self.init_health_module()
        self.init_customer_module()
        self.init_database()

    def init_health_module(self):
        health_service = HealthService()
        health_controller.initialize(health_service)
        self.app.include_router(health_controller.router)

    def init_customer_module(self):
        customer_repository = CustomerRepository()
        customer_service = CustomerService(customer_repository)
        customer_controller.initialize(customer_service)
        self.app.include_router(customer_controller.router)
        self.customer_service = customer_service

    def init_database(self):
        models.Base.metadata.create_all(bind=database.engine)
