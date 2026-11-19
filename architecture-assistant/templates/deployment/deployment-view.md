# Deployment Diagram — {{environment_name}}

Software-system/container scope: {{scope}} · Environment: {{production/staging/development/etc.}} · Audience: {{audience}} · Status/evidence date: {{status_and_date}}

```mermaid
flowchart TB
  %% Show deployment nodes/technology boundaries and deployed instances of registered software systems/containers.
  %% Distinguish infrastructure nodes from C2 containers. Keep nodes nested where useful.
  %% Use stable registry IDs for software; label communication protocols and trust boundaries.
```

## Diagram key

- {{shape/style}} = {{deployment node, software instance, infrastructure node, trust zone}}

## Topology, assumptions and validation

Deployment nodes and nesting: {{physical/virtual/containerized/execution environments}}. Deployed system/container instances and scaling/replicas: {{IDs and counts, or unresolved}}. Infrastructure services (DNS, gateway, load balancer, firewall, queue, secrets/telemetry): {{known elements}}. Network/trust boundaries and flows: {{}}. Availability/failover/recovery/observability: {{}}. Assumptions and related ADRs: {{}}. Do not invent an environment topology; list unknowns explicitly. Renderer/parser and visual review: {{tool/result or NOT_VERIFIED}}.
