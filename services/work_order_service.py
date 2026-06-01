

from data.database import SessionLocal
from models.work_orders import WorkOrderModel
from sqlalchemy.orm import joinedload

from services.clients_service import ClientsService
from services.access_remote_service import AccessRemoteService



class WorkOrderService:
    def __init__(self):
        self.clients_service = ClientsService()
        self.access_remote_service = AccessRemoteService()

    def create_work_order(self, data):
        session = SessionLocal()

        try:

            if not data.get("client_id"):
                client_data = data.get("client_data")

                client = self.clients_service.create_client(client_data, session=session)

                data["client_id"] = client.id

            




            work_order_data = data.get("order_data")
            if not work_order_data.get("description"):
                raise ValueError("Descrição é obrigatória")

            if not work_order_data.get("price"):
                raise ValueError("Preço é obrigatório")
            
            if not work_order_data.get("status_service"):
                raise ValueError("Status de serviço é obrigatório")
            
            if not work_order_data.get("status_payment"):
                raise ValueError("Status de pagamento é obrigatório")

            work_order = WorkOrderModel(
                client_id= data.get("client_id") or client.id,
                description= work_order_data.get("description"),
                price= work_order_data.get("price"),
                status_service_id= work_order_data.get("status_service"),
                status_payment_id= work_order_data.get("status_payment")
            )

            
            session.add(work_order)
            session.flush()
            session.refresh(work_order)

            if data.get("access_remote_data"):
                remote_access_data = data.get("access_remote_data")
                remote_access_data["work_order_id"] = work_order.id
                self.access_remote_service.create_access_remote(remote_access_data, session=session)
            session.commit()


            return "Ordem de serviço criada com sucesso"
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
                    joinedload(WorkOrderModel.remote_accesses)
                )\
                .all()

            return work_orders

        except Exception as e:
            
            return []
        finally:
            session.close()

    def update_status_service(self, work_orer_id, status_service_id):
        session = SessionLocal()

        try:
            work_order = session.query(WorkOrderModel).filter(WorkOrderModel.id == work_orer_id).first()

            if not work_order:
                raise ValueError("Ordem de serviço não encontrada")

            work_order.status_service_id = status_service_id

            session.commit()

            return "Status de serviço atualizado com sucesso"
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_status_payment(self, work_orer_id, status_payment_id):
        session = SessionLocal()

        try:
            work_order = session.query(WorkOrderModel).filter(WorkOrderModel.id == work_orer_id).first()

            if not work_order:
                raise ValueError("Ordem de serviço não encontrada")

            work_order.status_payment_id = status_payment_id

            session.commit()

            return "Status de pagamento atualizado com sucesso"
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
        
    def delete_work_order_by_id(self, work_order_id, session = None):
        
        own_session = session is None
        if own_session:
            session = SessionLocal()

        try:
            work_order = session.query(WorkOrderModel).filter(WorkOrderModel.id == work_order_id).first()

            if not work_order:
                raise ValueError("Ordem de serviço não encontrada")

            session.delete(work_order)

            if own_session:
                session.commit()

            return "Ordem de serviço deletada com sucesso"
        except Exception as e:
            if own_session:
                session.rollback()
            raise e
        finally:            
            if own_session:
                session.close()










