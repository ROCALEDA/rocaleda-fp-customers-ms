from fastapi import FastAPI

from app.health.controllers import health_controller
from app.health.services.health_service import HealthService


class Initializer:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self.init_health_module()

    def init_health_module(self):
        health_service = HealthService()
        health_controller.initialize(health_service)
        self.app.include_router(health_controller.router)

