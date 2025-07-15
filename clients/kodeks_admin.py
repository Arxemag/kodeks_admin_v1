import httpx
from typing import List, Dict, Optional

class KodeksAdminClient:
    def __init__(self, base_url: str, session_cookie: str):
        self.base_url = base_url
        self.session_cookie = session_cookie
        self.client = httpx.Client(base_url=self.base_url, cookies={"session": self.session_cookie})

    def get_cabinets(self) -> List[Dict]:
        query = """
        query {
          board {
            many {
              id
              title
              author
              hiddenOnStartPage
            }
          }
        }
        """
        response = self.client.post("/infoboard/graphql", json={"query": query})
        response.raise_for_status()
        data = response.json()
        return data["data"]["board"]["many"]

    def get_groups(self) -> List[Dict]:
        response = self.client.get("/users/groups")
        response.raise_for_status()
        # Предположим, что ответ JSON и содержит список групп с полями id и name
        return response.json()

    def create_group(self, group_name: str) -> Optional[Dict]:
        params = {"name": group_name}
        response = self.client.get("/users/groups", params=params)
        response.raise_for_status()
        return response.json()  # Возвращает созданную группу или ошибку

    def apply_acl(self, acl_params: Dict) -> bool:
        response = self.client.post("/admin/dirs", data=acl_params)
        response.raise_for_status()
        return response.status_code == 200
