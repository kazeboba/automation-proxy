import re
import mitmproxy.ctx as ctx
from mitmproxy import http
from file_worker import FileWorker

file_worker = FileWorker()


def response(flow: http.HTTPFlow) -> None:
    url = flow.request.url
    if not flow.response.content: return
    cfg = file_worker.get_proxy_params()

    "STATUS CODE override"
    cfg_status = cfg.get("status")
    if cfg_status:
        for api, sc in list(cfg_status.items()):
            "If 'api' in URI (compiling with 're')"
            if bool(re.compile(api).search(url)):
                "Changing the STATUS CODE"
                flow.response.status_code = int(sc[0] if isinstance(sc, list) else sc)
                ctx.log.info(f"Status code was mocked '{api}' -> {sc}")
                if not isinstance(sc, list):
                    del cfg_status[api]
                    "Updating a 'config.json'"
                    file_worker.set_proxy_param("status", cfg_status)
                    cfg["status"] = cfg_status
                break

    "MOCK params"
    cfg_mock: dict = cfg.get("mock")
    if cfg_mock:
        for mock_api, params in list(cfg_mock.items()):
            if bool(re.compile(mock_api).search(url)):
                data = flow.response.content.decode()
                modified = file_worker.mock(params[0] if isinstance(params, list) else params, data)
                if modified:
                    flow.response.content = modified.encode()
                    ctx.log.info(f"Param {params} were mocked for '{mock_api}'")
                else:
                    ctx.log.info(f"No matches found for {params}")
                if not isinstance(params, list):
                    del cfg_mock[mock_api]
                    file_worker.set_proxy_param("mock", cfg_mock)
                    cfg["mock"] = cfg_mock
                break

    "SAVE RESPONSE to file"
    cfg_response: list = cfg.get("get_response")
    if cfg_response:
        for i, resp_api in enumerate(list(cfg_response)):
            if bool(re.compile(resp_api[0] if isinstance(resp_api, list) else resp_api).search(url)):
                ctx.log.info(f"Response '{url}' was saved with #{i}")
                file_worker.set_proxy_temp_file(f"response_{i}.json", flow.response.get_text())
                if not isinstance(resp_api, list):
                    cfg_response.pop(i)
                    file_worker.set_proxy_param("get_response", cfg_response)
                    cfg["get_response"] = resp_api
                break
