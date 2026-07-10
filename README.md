# Hardware Test Platform (Desktop)

## Overview

Hardware Test Platform este aplicația desktop responsabilă pentru controlul echipamentelor de test și coordonarea execuției testelor automate.

Aplicația comunică cu:

* surse de alimentare (Power Supplies);
* Raspberry Pi Test Server (prin REST API);
* în viitor alte dispozitive (camere, PLC-uri, cititoare de coduri de bare, multimetre etc.).

Scopul proiectului este construirea unei platforme modulare și extensibile pentru testarea produselor electronice.

---

# Architecture

```
Desktop Application
│
├── UI
│
├── Core
│   ├── DeviceManager
│   ├── PiClient
│   └── (future) TestRunner
│
└── Devices
    ├── Power Supplies
    │   ├── Base
    │   ├── Manager
    │   └── Plugins
    │
    ├── Cameras (future)
    ├── Barcode Readers (future)
    ├── Raspberry Pi (API Client)
    └── Other Devices...
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
│   ├── device_manager.py
│   └── pi_client.py
│
├── devices/
│   └── power_supplies/
│       ├── __init__.py
│       ├── base.py
│       ├── manager.py
│       └── owon.py
│
├── ui/
│   ├── __init__.py
│   └── main_window.py
│
├── products/
│
└── reports/
```

---

# Power Supply Plugin System

Fiecare sursă de alimentare este implementată ca un plugin.

Exemplu:

```
devices/power_supplies/

    owon.py
    rigol.py
    keysight.py
```

Toate plugin-urile moștenesc:

```
PowerSupplyBase
```

și sunt încărcate automat prin:

```
PowerSupplyManager
```

Astfel, adăugarea unei noi surse presupune doar crearea unui nou fișier Python.

Nu este necesară modificarea aplicației.

---

# DeviceManager

`DeviceManager` reprezintă punctul unic de acces către toate dispozitivele disponibile.

În prezent gestionează:

* PowerSupplyManager
* PiClient

În viitor va gestiona și:

* CameraManager
* BarcodeManager
* PLCManager
* MultimeterManager

GUI-ul comunică exclusiv cu `DeviceManager`, fără a cunoaște implementările interne.

---

# Raspberry Pi Integration

Desktop-ul nu execută teste direct.

Toate testele hardware sunt executate pe Raspberry Pi.

Comunicarea se face prin REST API.

Exemple:

```
GET /tests

GET /tests/{id}

POST /tests/{id}/run
```

Aceste endpoint-uri sunt accesate prin clasa:

```
PiClient
```

GUI-ul nu conține apeluri HTTP directe.

---

# Configuration

Configurația aplicației este stocată în:

```
config.json
```

Exemplu:

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

Fișierul este încărcat prin:

```
config/settings.py
```

și este accesibil în aplicație prin:

```python
settings.raspberry_pi.host
settings.raspberry_pi.port
settings.application.theme
```

---

# Current Status

Implemented:

* Project architecture
* Modular Power Supply system
* PowerSupplyBase
* OwonPowerSupply plugin
* Automatic plugin discovery
* DeviceManager
* Raspberry Pi REST client
* Typed application configuration

Communication between Desktop and Raspberry Pi has been successfully tested.

---

# Planned Features

## Test Runner

Motor responsabil pentru executarea secvențelor de test.

Acesta va coordona:

* sursa de alimentare;
* Raspberry Pi;
* alte dispozitive.

GUI-ul va apela doar:

```python
test_runner.run(product)
```

---

## Product Editor

Utilizatorul va putea crea produse noi și defini secvențe de test personalizate.

Exemplu:

```
Product

├── Set Voltage
├── Enable Output
├── RGB Test
├── Current Measurement
├── Disable Output
```

Ordinea va putea fi modificată prin interfața grafică.

---

## Reports

Generarea automată a rapoartelor de test.

---

## Additional Device Support

Planificat:

* Rigol Power Supplies
* Keysight Power Supplies
* Cameras
* Barcode Readers
* PLCs
* Multimeters
* Relay Boards

Fiecare dispozitiv va fi implementat ca plugin și detectat automat.

---

# Design Principles

* Modular architecture
* Plugin-based devices
* Automatic discovery
* Separation of UI and business logic
* Configuration outside the source code
* Extensible hardware support
* Clean and maintainable codebase

---

# Current Goal

Construirea unei platforme complete de testare hardware în care:

* Desktop-ul orchestrează execuția testelor;
* Raspberry Pi execută testele hardware;
* Dispozitivele sunt extensibile prin plugin-uri;
* Produsele și secvențele de test sunt configurabile din interfața grafică.
