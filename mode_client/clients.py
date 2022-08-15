from json import JSONDecodeError
from typing import Any, Dict, List, Literal, Optional

import httpx
from pydantic import parse_obj_as

from mode_client.models import (
    Account,
    Query,
    QueryRun,
    Report,
    ReportRun,
    ReportRuns,
    Space,
)


class ModeBaseClient:
    def __init__(self, workspace: str, token: str, password: str):
        self.client = httpx.Client(
            base_url=f"https://app.mode.com/api/{workspace}",
            auth=httpx.BasicAuth(token, password),
            timeout=10.0,
        )

    def request(
        self,
        method: str,
        resource: str,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        if params:
            params = {k: v for k, v in params.items() if v}

        response = self.client.request(
            method=method, url=resource, json=json, params=params
        )
        response.raise_for_status()

        try:
            return response.json()
        except JSONDecodeError:
            return response.text


class ModeAccountClient(ModeBaseClient):
    def __init__(self, _: str, token: str, password: str):
        super().__init__("", token, password)

    def get(self, account: str) -> Account:
        response = self.request("GET", f"/{account}")

        return Account.parse_obj(response)


class ModeQueryClient(ModeBaseClient):
    def get(self, report: str, query: str) -> Query:
        response = self.request("GET", f"/reports/{report}/queries/{query}")

        return Query.parse_obj(response)

    def list(self, report: str) -> List[Query]:
        response = self.request("GET", f"/reports/{report}/queries")

        return parse_obj_as(List[Query], response["_embedded"]["queries"])

    def create(
        self, report: str, raw_query: str, data_source_id: int, name: str
    ) -> Query:
        json = {
            "query": {
                "raw_query": raw_query,
                "data_source_id": data_source_id,
                "name": name,
            }
        }
        response = self.request("POST", f"/reports/{report}/queries", json=json)

        return Query.parse_obj(response)

    def update(
        self, report: str, query: str, raw_query: str, data_source_id: int, name: str
    ) -> Query:
        json = {
            "query": {
                "raw_query": raw_query,
                "data_source_id": data_source_id,
                "name": name,
            }
        }
        response = self.request(
            "PATCH", f"/reports/{report}/queries/{query}", json=json
        )

        return Query.parse_obj(response)

    def delete(self, report: str, query: str):
        self.request("DELETE", f"/reports/{report}/queries/{query}")


class ModeQueryRunClient(ModeBaseClient):
    def get(self, report: str, run: str, query_run: str) -> QueryRun:
        response = self.request(
            "GET", f"/reports/{report}/runs/{run}/query_runs/{query_run}"
        )

        return QueryRun.parse_obj(response)

    def list(self, report: str, run: str) -> List[QueryRun]:
        response = self.request("GET", f"/reports/{report}/runs/{run}/query_runs")

        return parse_obj_as(List[QueryRun], response["_embedded"]["query_runs"])


class ModeReportClient(ModeBaseClient):
    def get(self, report: str) -> Report:
        response = self.request("GET", f"/reports/{report}")

        return Report.parse_obj(response)

    def list(
        self,
        data_source: Optional[str] = None,
        space: Optional[str] = None,
        _filter: Optional[str] = None,
        order: Literal["asc", "desc"] = "desc",
        order_by: Literal["created_at", "updated_at"] = "updated_at",
    ) -> List[Report]:
        assert (
            bool(data_source) + bool(space) == 1
        ), "Only one of data_source, space can be defined"

        url = (
            f"/spaces/{space}/reports"
            if space
            else f"/data_sources/{data_source}/reports"
        )

        params = {"filter": _filter, "order": order, "order_by": order_by}
        response = self.request("GET", url, params=params)

        return parse_obj_as(List[Report], response["_embedded"]["reports"])

    def delete(self, report: str) -> None:
        self.request("DELETE", f"/reports/{report}")

    def archive(self, report: str) -> Report:
        response = self.request("PATCH", f"/reports/{report}/archive")
        return Report.parse_obj(response)

    def unarchive(self, report: str) -> Report:
        response = self.request("PATCH", f"/reports/{report}/unarchive")

        return Report.parse_obj(response)

    def sync(self, report: str, commit_message: Optional[str] = None) -> Report:
        json = {"commit_message": commit_message}
        response = self.request("PATCH", f"/reports/{report}/sync_to_github", json=json)

        return Report.parse_obj(response)


class ModeReportRunClient(ModeBaseClient):
    def get(self, report: str, run: str) -> ReportRun:
        response = self.request("GET", f"/reports/{report}/runs/{run}")

        return ReportRun.parse_obj(response)

    def list(
        self,
        report: str,
        filter_: Optional[str] = None,
        order: Literal["asc", "desc"] = "desc",
        order_by: Literal["created_at", "updated_at"] = "updated_at",
    ) -> ReportRuns:
        params = {"filter": filter_, "order": order, "order_by": order_by}
        raw_response = self.request("GET", f"/reports/{report}/runs", params=params)
        response = {
            "pagination": raw_response["pagination"],
            "report_runs": raw_response["_embedded"]["report_runs"],
        }

        return ReportRuns.parse_obj(response)

    def clone(self, report: str, run: str) -> ReportRun:
        response = self.request("POST", f"/reports/{report}/runs/{run}/clone")
        return ReportRun.parse_obj(response)

    def create(self, report: str, json: Dict[str, Any]) -> ReportRun:
        response = self.request("POST", f"/reports/{report}/runs", json=json)
        return ReportRun.parse_obj(response)


class ModeSpaceClient(ModeBaseClient):
    def get(self, space: str) -> Space:
        response = self.request("GET", f"/spaces/{space}")
        return Space.parse_obj(response)

    def list(self, filter_: Literal["all", "custom"] = "custom") -> List[Space]:
        params = {"filter": filter_}
        response = self.request("GET", "/spaces", params=params)
        spaces = response["_embedded"]["spaces"]

        return parse_obj_as(List[Space], spaces)

    def create(self, name: str, description: str) -> Space:
        json = {"space": {"name": name, "description": description}}
        response = self.request("POST", "/spaces", json=json)

        return Space.parse_obj(response)

    def update(self, space: str, name: str, description: str) -> Space:
        json = {"space": {"name": name, "description": description}}
        response = self.request("POST", f"/spaces/{space}", json=json)

        return Space.parse_obj(response)

    def delete(self, space: str):
        response = self.request("DELETE", f"/spaces/{space}")

        return Space.parse_obj(response)


class ModeClient:
    def __init__(self, workspace: str, token: str, password: str):
        self.workspace = workspace
        self.token = token
        self.password = password

    @property
    def account(self):
        return ModeAccountClient(self.workspace, self.token, self.password)

    @property
    def query(self):
        return ModeQueryClient(self.workspace, self.token, self.password)

    @property
    def query_run(self):
        return ModeQueryRunClient(self.workspace, self.token, self.password)

    @property
    def report(self):
        return ModeReportClient(self.workspace, self.token, self.password)

    @property
    def report_run(self):
        return ModeReportRunClient(self.workspace, self.token, self.password)

    @property
    def space(self):
        return ModeSpaceClient(self.workspace, self.token, self.password)
