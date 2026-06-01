from data.database import SessionLocal

from models.status_payments import StatusPaymentModel
from models.status_services import StatusServiceModel


def seed_database():
    session = SessionLocal()

    try:
        # STATUS PAGAMENTO
        payment_status = [
            "PENDENTE",
            "PAGO",
            "DEVENDO"
        ]

        for status_name in payment_status:

            exists = (
                session.query(StatusPaymentModel)
                .filter(StatusPaymentModel.name == status_name)
                .first()
            )

            if not exists:
                session.add(
                    StatusPaymentModel(
                        name=status_name
                    )
                )

        # STATUS SERVIÇO
        service_status = [
            "EM ANDAMENTO",
            "FINALIZADO",
            "AGUARDANDO CLIENTE",
            "REJEITADO",
        ]

        for status_name in service_status:

            exists = (
                session.query(StatusServiceModel)
                .filter(StatusServiceModel.name == status_name)
                .first()
            )

            if not exists:
                session.add(
                    StatusServiceModel(
                        name=status_name
                    )
                )

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()