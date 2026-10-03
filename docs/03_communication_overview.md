# Communication Overview

| Mechanism | Roles | Use for |
|---|---|---|
| **Topics** | Publisher / Subscriber | Data streams |
| **Services** | Client / Server | Quick computations or actions |
| **Actions** | Client / Server | Longer tasks, with cancel, feedback, etc. |

## Publisher

Publishes a message of some type, on some topic, at some frequency.
- **Frequency** needs some form of time control: `create_timer(period, callback)`.
- **The callback** publishes every time it's called.

## Subscriber

Always listens on a topic and receives messages of a given type as and when they arrive.
- **Always:** no timer needed.
- **As and when they arrive:** a callback receives each message object.

## Service server

Offers a service to do something. Clients see the offer and send requests.
- Processes each client request as it arrives, so it needs a callback.

## Service client

Creates a request, sends it, and receives the response later, after the server has processed it.
- **Waiting for the server:** needs some form of waiting mechanism.
- **Receiving the response:** set up a callback.
- **The response arrives later:** use a future object.

## Action server and client

Actions are built from several services and topics underneath. See [05_actions.md](05_actions.md).
