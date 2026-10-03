# Services

Code: [`src/services_py`](../src/services_py)

**When:** a quick request → response: compute something, trigger an action, query a state. Not for continuous data (use topics) or long tasks (use actions).

## Naming conventions

- **The service name and the service server's node name are different things!**
- Service names start with a verb: `add_two_ints`.
- Callbacks are named `callback_<service_name>`: `callback_add_two_ints`.

## Client

Use `call_async` for non-blocking calls. **Always use `call_async`.**

## Command line

```bash
ros2 service list
ros2 service type /service_name
ros2 service find <service_type>
ros2 service call /service_name <service_type> "{data: 1}"
```

### Rename a service

```bash
ros2 run <pkg_name> <server_node_name> --ros-args -r old_service_name:=new_service_name
ros2 run <pkg_name> <client_node_name> --ros-args -r old_service_name:=new_service_name
```

**The service has to be renamed in both the server and the client!**

## rqt

Use the Service Caller plugin.

## See also

[03_communication_overview.md](03_communication_overview.md) · [05_actions.md](05_actions.md) · [09_executors.md](09_executors.md) (calling a service from inside a callback)
