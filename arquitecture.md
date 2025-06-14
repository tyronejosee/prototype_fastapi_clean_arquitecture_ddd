# Layers and Responsibilities

## 🧠 **`domain/` → Core Business Logic**

Defines **what** the system does, regardless of how it's implemented.

* `entities/`: domain models with behavior, not just data.
* `value_objects/`: immutable types with rules (e.g., `Email`, `Price`, `PhoneNumber`).
* `repositories/`: abstract interfaces for persistence.
* `services/`: pure domain logic that doesn’t belong to a specific entity.
* `aggregates/` (if applicable): groups of entities that operate as a single unit.
* `exceptions.py`: domain-specific errors (not HTTP errors).

## ⚙️ **`application/` → Use Case Coordinator**

Orchestrates the flow between entities, repositories, and domain services.

* `services/` (or `use_cases/`): **Application Services** coordinating domain actions.
* `schemas/`: DTOs (Pydantic models) for input/output.
* `commands/` and `queries/` (optional): to implement CQRS.
* `interfaces` or `ports` (optional): abstractions for external adapters.

## 🏗️ **`infrastructure/` → Technical Implementation**

Concrete details for persistence, external APIs, events, etc.

* `repositories/`: concrete implementations (e.g., using SQLAlchemy).
* `models/`: ORM models if separated from the domain.
* `services/`: external service adapters (email, Stripe, Redis).
* `gateways/`, `clients/`: communication with external APIs.
* `mappers/`: ORM ↔ domain entity mapping (if applicable).
* `cache/`, `queues/`, `events/`: technical integrations.

## 🌐 **`interfaces/` → System Input/Output**

Entry point for users or external systems.

* `api/routes/`: controllers (FastAPI, REST, GraphQL).
* `cli/`: CLI commands if any.
* `http/requests`, `responses/`: input/output mapping (optional).
* `dependencies/`: dependency injection.
* `event_handlers/`, `webhooks/`: event-based integrations.

## 🧩 **`core/` → Cross-cutting Infrastructure**

Configuration, security, and common utilities.

* `config.py`: environment variables.
* `security.py`: token generation/validation.
* `logger.py`
* `exceptions.py` (global)
* `database.py`, `settings.py`
