from data.database import SessionLocal
from models.status_services import StatusServiceModel



class StatusServiceService:
    def get_all_status_service(self):
        session = SessionLocal()

        try:
            status_services = session.query(StatusServiceModel).all()

            return status_services
        finally:
            session.close()