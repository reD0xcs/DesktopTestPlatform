# Hardware Test Platform (Desktop)

## Overview

The **Hardware Test Platform** is a desktop application designed to orchestrate automated hardware testing for electronic products.

It provides a modular and extensible architecture capable of controlling multiple types of laboratory equipment while executing configurable test sequences.

The application currently communicates with:

- Programmable Power Supplies
- Raspberry Pi Test Server (REST API)

Future support will include:

- Cameras
- Barcode Readers
- Multimeters
- PLCs
- Relay Boards
- Additional laboratory equipment

The long-term goal is to provide a flexible, plugin-based hardware testing platform suitable for production environments.

---

# Architecture

```
Desktop Application
│
├── UI
│   ├── Main Window
│   ├── Product Manager
│   ├── Product Editor
│   ├── Run Window
│   └── Dialogs
│
├── Core
│   ├── DeviceManager
│   ├── ActionRegistry
│   ├── ActionExecutor
│   ├── ProductSerializer
│   ├── PiClient
│   └── Configuration
│
├── Devices
│   ├── Power Supplies
│   │   ├── Base
│   │   ├── Manager
│   │   └── Plugins
│   │
│   ├── Raspberry Pi
│   ├── Cameras (future)
│   ├── Barcode Readers (future)
│   ├── Multimeters (future)
│   └── Other Devices...
│
└── Products
    └── JSON Files
```

---

# Current Project Structure

```
DesktopTestPlatform/

│
├── app.py
├── requirements.txt
├── config.json
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── core/
│   ├── action_executor.py
│   ├── action_registry.py
│   ├── device_manager.py
│   ├── pi_client.py
│   └── product_serializer.py
│
├── devices/
│   └── power_supplies/
│       ├── __init__.py
│       ├── base.py
│       ├── manager.py
│       └── owon.py
│
├── models/
│
├── ui/
│   ├── main_window.py
│   ├── product_editor.py
│   ├── product_manager.py
│   ├── run_window.py
│   ├── confirm_dialog.py
│   └── info_dialog.py
│
├── actions/
│
├── products/
│
├── reports/
│
└── logs/
```

---

# Product System

Each hardware test is stored as a **Product**.

A product consists of an ordered list of executable actions.

Example:

```
Power Supply → Set Voltage

Power Supply → Enable Output

System → Delay

Raspberry Pi → RGB Test

Power Supply → Disable Output
```

Products are stored as JSON files inside the `products/` directory and can be:

- Created
- Edited
- Saved
- Loaded
- Deleted
- Executed

---

# Product Editor

The Product Editor allows users to visually create and modify products.

Current features include:

- Create new products
- Save products
- Load existing products
- Delete products
- Add actions
- Remove actions
- Reorder actions
- Edit action parameters
- Confirmation dialogs
- Success notifications

---

# Product Manager

The Product Manager provides quick access to all available products.

Current features:

- Browse products
- Open products
- Create new products
- Delete products
- Run products

---

# Test Runner

The Test Runner executes product actions sequentially.

Current features:

- Execute products
- Overall progress bar
- Current step progress
- Live execution log
- Elapsed execution time
- Stop execution
- Success / Failure reporting

The execution engine delegates each action to the appropriate hardware controller through the `ActionExecutor`.

---

# Action System

Every executable operation is represented by an **Action**.

Examples:

```
system.delay

system.message

owon.set_voltage

owon.output_on

pi.rgb
```

Each action defines:

- Identifier
- Display name
- Category
- Description
- Parameters

The Product Editor automatically generates parameter editors based on the action definition.

---

# Action Executor

The `ActionExecutor` is responsible for executing product actions.

Depending on the action type, it dispatches commands to:

- System actions
- Power Supply devices
- Raspberry Pi
- Future hardware devices

This keeps the UI completely independent from hardware implementation details.

---

# DeviceManager

`DeviceManager` acts as the application's central hardware gateway.

Currently managed devices:

- PowerSupplyManager
- Raspberry Pi Client

Future additions:

- CameraManager
- BarcodeManager
- PLCManager
- MultimeterManager
- RelayManager

The graphical interface communicates exclusively with `DeviceManager`.

---

# Power Supply Plugin System

Every power supply is implemented as a plugin.

Example:

```
devices/power_supplies/

    owon.py
    rigol.py
    keysight.py
```

Each implementation inherits from:

```
PowerSupplyBase
```

Plugins are automatically discovered by:

```
PowerSupplyManager
```

Adding support for a new power supply only requires creating a new Python module.

No changes to the application core are necessary.

---

# Raspberry Pi Integration

Hardware-specific tests are executed remotely on a Raspberry Pi.

Communication is performed through a REST API.

Typical endpoints:

```
GET /tests

GET /tests/{id}

POST /tests/{id}/run
```

The desktop application communicates through:

```
PiClient
```

No HTTP requests are performed directly from the UI.

---

# Configuration

Application configuration is stored in:

```
config.json
```

Example:

```json
{
    "raspberry_pi": {
        "host": "192.168.1.37",
        "port": 8000
    },

    "application": {
        "theme": "dark",
        "refresh_rate": 500
    }
}
```

The configuration is loaded through:

```
config/settings.py
```

and exposed as strongly typed settings.

---

# Current Features

## Core

- Modular architecture
- Device Manager
- Action Registry
- Action Executor
- Product Serializer
- Typed configuration

## Hardware

- Plugin-based power supply system
- Automatic plugin discovery
- Owon power supply support
- Raspberry Pi REST client

## Product Management

- Create products
- Edit products
- Save / Load products
- Delete products
- JSON persistence

## Product Editor

- Visual action editor
- Parameter editor
- Step reordering
- Confirmation dialogs
- Success notifications

## Test Runner

- Product execution
- Progress tracking
- Step progress
- Live logging
- Stop execution
- Execution timer

---

# Planned Features

## Runner

- Pause / Resume
- Skip current step
- Retry failed step
- Estimated remaining time (ETA)
- Thread-safe UI updates
- PASS / FAIL status indicators

## Operator Actions

- Message dialogs
- Confirmation dialogs
- User input actions

## Validation Actions

- Wait for voltage
- Wait for GPIO
- Timeout support
- Measurement validation

## Product Variables

- User-defined variables
- Variable substitution
- Automatic timestamps

## Logging

- Automatic log files
- Execution reports
- PASS / FAIL summaries

## Product Manager

- Search
- Sorting
- Product metadata
- Duplicate products

## Device Manager

- Live connection status
- Connect / Disconnect
- Device information

## Product Editor

- Copy / Paste actions
- Duplicate actions
- Drag & Drop
- Enable / Disable actions
- Undo / Redo

## Import / Export

- Import JSON
- Export JSON
- Drag & Drop support
- Product templates

---

# Design Principles

- Modular architecture
- Plugin-based hardware support
- Automatic device discovery
- Separation of UI and business logic
- Strongly typed models
- JSON-based product storage
- Extensible action system
- Maintainable codebase

---

# Current Goal

The objective of the project is to build a complete, modular hardware testing platform where:

- The Desktop application orchestrates test execution.
- Raspberry Pi devices perform hardware-specific tests.
- Laboratory equipment is integrated through plugins.
- Products are fully configurable through a graphical interface.
- New hardware can be added with minimal changes to the existing codebase.