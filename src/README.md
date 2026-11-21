# Runtime code

Empty on purpose. The layout comes with ADR-0005 (languages) and ADR-0006 (data plane).

Planned split (candidate):

- CORE runs in its own process. It has no dependency on the agent layer.
- The agent layer reads CORE output. It cannot write to the alarm bus.
