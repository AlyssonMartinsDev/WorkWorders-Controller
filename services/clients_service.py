import email
from data.database import SessionLocal
from models.clients import ClientsModel
from utils.validators import Validators


class ClientsService:

    def create_client(self, data, session = None):

        own_session = session is None
        session = session or SessionLocal()

        try:
            print(f"dados no service de client{data}")
            # Limpando os dados
            name = data.get("name", "").strip()
            phone = data.get("phone", "").strip()
            


            # Primeira regra de negócio: O nome e o telefone são obrigatórios.
            if not name or not phone:
                raise ValueError("O nome e o telefone são obrigatórios.")


            # Segunda regra de negócio: O nome do cliente deve ter pelo menos 3 caracteres.
            if len(name) < 3:
                raise ValueError("O nome do cliente deve ter pelo menos 3 caracteres.")

            # Terceira regra de negócio: O telefone deve ser válido.
            Validators.validate_phone(phone)

            email = data.get("email", "").strip()

            # Quarta regra de negócio: O email deve ser válido.
            if email:
                Validators.validate_email(email)

            notes = data.get("notes", "").strip()

            # Quinta regra de negócio: As notas do cliente devem ter no máximo 255 caracteres.
            if notes and len(notes) > 255:
                raise ValueError("As notas do cliente devem ter no máximo 255 caracteres.")

            # Sexta regra de negocio: o telefone deve ser único.
            if session.query(ClientsModel).filter(ClientsModel.phone == phone).first():
                raise ValueError("Já existe um cliente com este telefone.")

            # Montando o objeto cliente
            client = ClientsModel(
                name= name,
                phone= phone,
                email= email,
                notes= notes
            )

            # Salvando o cliente no banco de dados
            session.add(client)

            # gerando o id sem confirmar a transação
            session.flush()

            # Atualizando o objeto cliente com os dados do banco de dados
            session.refresh(client)

            # Confirmando a transação se foi criada uma sessão própria
            if own_session:
                session.commit()

            return client
        except Exception as e:

            if own_session:
                session.rollback()

            raise e
        finally:
            if own_session:
                session.close()           
                



    def get_all_clients(self):

        session = SessionLocal()


        try:
            clients = session.query(ClientsModel).all()

            return clients
        except Exception as e:
           
            session.rollback()
            raise e
        finally:
            session.close()

            
    
    def get_client_by_id(self, id):
        session = SessionLocal()

        try:
            client = session.query(ClientsModel).filter(ClientsModel.id == id).first()

            return client
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close

    
    




