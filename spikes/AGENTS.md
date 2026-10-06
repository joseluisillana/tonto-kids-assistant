# Exploration context

Read [root](../AGENTS.md) and [workflow](../docs/ai-assisted-workflow.md) first.

`ui_kivy/main.py` is a standalone 800×480 Kivy press/release exploration.
`ui_kivy/test_main.py` is its ad hoc widget harness; its attempted mock window
setup is historical, not the validated product testing command. Neither invokes
backend HTTP or the client conversation loop. Depends on Kivy; no runtime product
consumer was found. Used as design evidence for the touch UI choice in D024.

Product Kivy widgets live under [client](../client/AGENTS.md) and their verified
tests under [tests](../tests/AGENTS.md). Read
[touch spec](../specs/raspberry-touch-ui.md) and
[decisions](../docs/decisions.md#d024---raspberry-touch-ui-tech-stack) before promoting
experimental findings. Changes here do not automatically alter production
architecture. No dedicated official spike test/build target exists; do not claim
test all covers spikes. Use the actual product `./tonto.sh test ui` for product
widget validation, not as a substitute for spike evidence or real hardware.
