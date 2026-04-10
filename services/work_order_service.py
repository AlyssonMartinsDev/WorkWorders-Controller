from data.database import SessionLocal
from models.work_orders import WorkOrderModel
from sqlalchemy.orm import joinedload


class WorkOrderService:

    def test_service(self):
        print("Service iniciado com sucesso")

    def create_work_order(self, data):
        


        session = SessionLocal()

        try:


            work_order = WorkOrderModel(
                client_name=data["name"],
                phone=data["phone"],
                access_remote=data["idAccessRemote"],
                description=data["description"],
                date=data["date"],
                price=data["price"],
                status_payment=data["statusPayment"],
                status_service=data["statusService"]


            )
            session.add(work_order)
            session.commit()
            session.refresh(work_order)

            return work_order
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()



    def get_all_work_orders(self):
        session = SessionLocal()

        try:
            work_orders = session.query(WorkOrderModel)\
                .options(
                    joinedload(WorkOrderModel.client),
                    joinedload(WorkOrderModel.status_service),
                    joinedload(WorkOrderModel.status_payment),
                    joinedload(WorkOrderModel.remote_access)
                )\
                .all()

            return work_orders

        except Exception as e:
            print(e)
            return []
        finally:
            session.close()









