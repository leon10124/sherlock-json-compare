# JSON Structure Compare

A small local JSON comparison tool for generated-field noise and reordered arrays.
No accounts, databases, AI model or paid APIs required. JSON inputs are processed in
memory on your loopback server, without input logs. This is not a hosted website or
a browser-only offline app. Demand and willingness to pay remain unvalidated.

## Run from source
Requires Python 3.10+. Run `python portable_json.py`, or double-click Start.cmd on
Windows. Your browser opens automatically; close the terminal to stop.

## Try a comparison

Windows: download and extract the [tested ZIP release](https://github.com/leon10124/sherlock-json-compare/releases/tag/v0.1.0), then double-click `JSON-Compare.exe`. Keep its local process running while using the browser interface. The Windows executable does not require Python.

Paste these values into the left and right inputs:

```json
{"updated":"2026-09-29","ids":[1,2]}
```

```json
{"updated":"2026-09-30","ids":[2,1]}
```

Add `/updated` to the ignored JSON Pointer paths and enable unordered arrays. The result is equal. With unordered arrays disabled, the changed ID order is reported. Keep that option disabled for sequences where order matters.

The [machine-readable examples](examples.json) include duplicate-count and boolean-versus-number cases. Every expected result was checked against the actual comparison engine before publication. All-array unordered mode applies recursively; an ignored path matches an exact location, not every field with the same name.

## Features and limits
Object member order is ignored. Exact JSON Pointer exclusions are supported.
Optional unordered arrays preserve duplicate counts; disable this for sequences.
Numbers are compared strictly by parsed Python number type. Duplicate object keys
and non-finite numbers are rejected. Each input: 256 KiB, depth 64, 10,000 nodes.
At most 200 changes are returned. No JSON Patch compatibility is claimed.
Never paste credentials. The service rejects foreign Host and Origin headers.

## Test
Run `python test_json_compare.py`. Tests include structural edge cases and starting
the actual standalone HTTP server to compare Unicode values and block cross-origin
requests. Windows binary packaging has separate executable smoke-test evidence;
the tested Windows package is available on the [release page](https://github.com/leon10124/sherlock-json-compare/releases/tag/v0.1.0).

## Status
Functions verified locally; software package publicly distributed on GitHub.
This is not a publicly hosted web application. No independent users or revenue confirmed.
