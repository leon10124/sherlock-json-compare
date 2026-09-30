# JSON Structure Compare

A small local JSON comparison tool for generated-field noise and reordered arrays.
No accounts, databases, AI model or paid APIs required. JSON inputs are processed in
memory on your loopback server, without input logs. This is not a hosted website or
a browser-only offline app. Demand and willingness to pay remain unvalidated.

## Run from source
Requires Python 3.10+. Run `python portable_json.py`, or double-click Start.cmd on
Windows. Your browser opens automatically; close the terminal to stop.

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
no binary download is publicly published yet.

## Status
Verified locally. Not publicly deployed. No independent users or revenue confirmed.
