from models.remote_access import RemoteAccess
from data.database import SessionLocal


class AccessRemoteService:

    def create_access_remote(self, data, session = None):
        own_session = session is None
        session = session or SessionLocal()

        try:

            # Limpando os dados
            code = data.get("code", "").strip()
            access_type = data.get("access_type", "").strip()
            password = data.get("password", "").strip()

            # Primeira regra de negocio: todos os campos são obrigatórios.
            if not code or not type or not password:
                raise ValueError("Todos os campos do acesso remoto são obrigatórios.")


            # Montando o objeto acesso remoto

            access_remote = RemoteAccess(
                code=code,
                password=password,
                type=access_type
            )

            # Salvando o acesso remoto no banco de dados

            session.add(access_remote)
            session.flush()
            session.refresh(access_remote)

            # Confirmando a transação se foi criada uma sessão própria
            if own_session:
                session.commit()

            return access_remote

        except Exception as e:
            if own_session:
                session.rollback()

            raise e

        finally:
            if own_session:
                session.close()
        