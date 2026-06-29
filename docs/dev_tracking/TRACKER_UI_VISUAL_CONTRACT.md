# Tracker UI Visual Contract

Locked: 2026-06-29T13:12:21

## Purpose

The UI Common Tracker Kit is the shared visual contract for tracker-like cockpits.

It prevents repeated UI drift between Migration Tracker, CDC Tracker, Dev Tracker, Tool Registry CDC, and future tracker cockpits.

## Visual oracle

Migration Tracker is the visual oracle.

All tracker previews must use the common tracker kit or prove parity with it.

## Required render types

- migration_tracker_oracle
- cdc_tracker
- dev_tracker
- tool_registry_tracker
- benchmark_tracker

## Mandatory UI tokens

- separate cockpit sections
- blue progress bars
- percent per phase or step
- status badges
- route pills
- operator cards
- full lifecycle phase coverage
- no generic standalone HTML used as release evidence

## Cockpit bindings

- Migration Tracker: visual oracle
- CDC Delivery Tracker: CDC source and delivery status
- CDC Dev Tracker: CDC operator page
- Dev Tracking: lifecycle cockpit
- Tool Registry CDC: tool registry contract tracking

## Preview rule

Visual tests are mandatory before Reflex deployment.

A local HTML preview is only a static preview. Public deployment also requires real browser/runtime visual evidence.
