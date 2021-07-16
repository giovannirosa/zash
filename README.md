# ZASH (Zero-Aware Smart Home System)

This repository is the implementation of ZASH (Zero-Aware Smart Home System), a system to provide Access Control for a Smart Home System using Continuous Authentication with Zero Trust in order to continuously verify users authenticity, powered by edge computing to dismiss unreliable service providers and capable of processing request originated from any means. The system is designed with user levels (e.g., admin, adult, child, visitor), device classes (e.g., critical, non-critical) and actions (e.g., view, control, manage) in order to mitigate possible undetected impersonation attack by contributing for devices isolation and actions differentiation. The CA process is constituted by three phases, being the first the verification among user, devices and actions using ontologies. The second phase is the verification of context information to check if they achieve expected trust for a requested action with a specific user level on a device class. The final phase consists of verifying whether the requested action makes sense considering a Markov Chain built on all previous activities.

# Execution

The only requirement to run the simulation is Python >= 3.6.

Simply execute: ```python3 zash.py```

It will generate log files under logs directory with the date and time of the execution.

Log files includes:

- activity_fail: requests that failed in activity manager.
- ontology_fail: requests that failed in ontology manager.
- context_fail: requests that failed in context manager.
- blocks: blocked requests.
- valid_proofs: requests that received valid proofs.
- invalid_proofs: requests that received invalid proofs.
- sim: simulation trace.
