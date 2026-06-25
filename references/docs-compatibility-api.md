# Docs, Compatibility, And Interfaces

Use this for user docs, developer docs, deployment docs, API/CLI/SDK design, cross-platform checks, and hardware/device compatibility.

## Documentation Audiences

Write for the audience that needs the doc:

- User: what it is, who it helps, install, start, use, success signal, common problems.
- Developer: structure, modules, startup flow, config, interfaces, tests, extension points.
- Deployment: environment, dependencies, config, env vars, Docker, logs, start/stop, persistence, upgrade, rollback.
- Demo: goal, steps, input, expected output, current capability, limitations, backup path.
- API caller: endpoint or command, parameters, response, errors, limits, examples.

Small projects need at least README, Quick Start, config notes, test notes, and troubleshooting.

Use `assets/templates/` when creating reusable docs.

## Cross-Platform Checklist

Consider:

- Windows, macOS, Linux
- x86_64 and ARM64
- Python, Node, Go, Java, or browser versions
- Chrome, Edge, Safari
- bash, zsh, PowerShell
- local, Docker, and server execution
- online and offline modes
- dev, test, and production environments

For paths:

- Avoid local absolute paths.
- Use cross-platform path APIs.
- Do not assume `/` or `\` manually.
- Show platform-specific commands when needed.

If full compatibility is not verified, state supported platforms, unverified platforms, known limits, and adaptation steps.

## Device Compatibility

For hardware, robotics, phones, embedded devices, cameras, microphones, sensors, or simulators, check:

- Device may be absent.
- Permission may be missing.
- Driver may be missing.
- Device name may differ.
- Sampling rate, resolution, or encoding may differ.
- Connection may be USB, Bluetooth, Wi-Fi, serial, CAN, gRPC, HTTP, or other.
- Device may disconnect during use.
- Simulator, mock, demo, or offline mode may be needed.

Prefer real-device mode plus simulator/mock/offline demo mode.

## Interface Design

If others may call the feature, design the smallest stable interface:

- HTTP API
- gRPC API
- CLI command
- SDK or package API
- Webhook
- Config file
- Plugin interface
- Event callback
- Message queue
- Local function

State:

- Caller
- Input
- Output
- Error shape
- Auth and rate limits
- Logs
- Versioning
- Backward compatibility
- Examples

Avoid exposing internal implementation details or temporary fields as long-term contracts.

## Plain-Language Explanations

For non-technical users, explain terms simply:

- API: a program entry point other programs can call.
- Database: where data is stored.
- Cache: saved common data so it does not need to reload every time.
- Backend: logic and data handling.
- Frontend: what users see and click.
- Deployment: putting the program somewhere it can run.
- Dependency: an external tool or package the project needs.
- Test: a check that behavior matches expectation.
