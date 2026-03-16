# MITM Proxy Integration for UI Tests

<p align="center">
Programmable proxy layer for UI automation based on <b>mitmproxy</b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue)
![mitmproxy](https://img.shields.io/badge/mitmproxy-supported-green)
![platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-lightgrey)
![license](https://img.shields.io/badge/license-MIT-blue)

</p>

---

## Overview

Modern UI tests interact with applications only through the user interface.  
As a result, they are often **blind to the network layer**, which makes debugging and reproducing issues difficult.

This project integrates **mitmproxy** into the test framework to provide **network visibility and traffic control** for UI tests.

With this approach, UI tests can:

- inspect network traffic
- mock backend responses
- simulate error conditions
- capture API responses
- analyze WebSocket traffic

---

## Why Proxy in UI Tests?

UI tests without network access often suffer from:

- flaky tests
- hard-to-diagnose failures
- inability to reproduce backend states
- dependency on unstable environments
- lack of visibility into API behavior

Adding a programmable proxy solves these problems by exposing the network layer to the test framework.

---

## Features

### Network visibility

- log HTTP requests and responses
- inspect WebSocket traffic
- verify request sequence
- verify request count

### Traffic manipulation

- override HTTP status codes
- mock response payloads
- modify headers
- inject WebSocket messages

### Testing capabilities

- simulate backend failures
- simulate slow network
- reproduce complex client states
- validate client request structure

---

## Why mitmproxy

GUI tools like:

- Charles Proxy
- Proxyman
- Fiddler

are great for manual testing but not designed for automation.

**mitmproxy** provides a programmable alternative.

Key advantages:

- Python scripting API
- headless mode for CI
- HTTP and WebSocket support
- traffic interception and modification
- cross-platform open source

Documentation:  
https://docs.mitmproxy.org

---

## Installation

Install mitmproxy:

```bash
brew install mitmproxy
```
Official guide:  
https://docs.mitmproxy.org/stable/overview/installation/

---

## Certificate Installation

To intercept HTTPS traffic you must install the mitmproxy certificate on the device.

Documentation:  
https://docs.mitmproxy.org/stable/concepts/certificates/

---

## Running the Proxy

Start the proxy with a custom addon:

```bash
mitmweb -s proxy_handler.py
```

Available modes:

| Mode | Description |
|-----|-----|
| mitmproxy | interactive CLI |
| mitmweb | browser interface |
| mitmdump | headless mode |

---

## Architecture

The proxy is controlled through a configuration file shared with the test framework.

```
UI Tests
   │
   │ modify config.json
   ▼
Proxy Addon (proxy_handler.py)
   │
   ▼
Traffic interception
   │
   ▼
Request / Response manipulation
```

The test framework updates `config.json`, and the proxy dynamically applies rules to the traffic.

---

## Configuration

Example `config.json`

```json
{
  "status": {},
  "mock": {},
  "get_response": []
}
```

---

## Status Code Mocking

Override response status codes for specific APIs.

Example configuration:

```json
{
  "status": {
    "api/v1/user": 404,
    "api/v2/settings": 500
  }
}
```

Permanent override:

```json
{
  "status": {
    "api/v1/user": [404]
  }
}
```

---

## Example Usage in Tests

```python
proxy.set_status({
    "api/v1/user": 404
})
```

This allows tests to simulate backend errors without modifying the server.

---

## Benefits

Using mitmproxy in UI automation provides:

- deterministic test environments
- backend simulation
- improved debugging
- full network observability
- faster test execution

---

## Future Improvements

Planned features:

- WebSocket message injection
- WebSocket message modification
- network throttling
- request sequence validation
- traffic recording & replay

---

## License

MIT License

