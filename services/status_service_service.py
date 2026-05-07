from data.database import SessionLocal
from models.status_payments import StatusPaymentModel




class StatusPaymentService:
    def get_all_status_payments(self):
        session = SessionLocal()

        try:
            status_payments = session.query(StatusPaymentModel).all()
            return status_payments
        finally:
            session.close()