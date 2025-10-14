# DEC-DEMO-0001: Add "Clear" Button to Calculator

**Date:** 2025-10-09

**Status:** Accepted

## Context

Users of our calculator application have no quick way to reset the current calculation to zero. If they make a mistake, they must manually backspace or complete the incorrect calculation and start a new one. This is inefficient and frustrating.

## Decision

We will add a "Clear" (C) button to the calculator's main interface. Pressing this button will reset the current input and displayed value to '0'. This provides a fast and intuitive way for users to recover from errors.

## Consequences

- The UI of the calculator will need to be updated to include the new button.
- A new logic function will be required to handle the "clear" action.
- This feature will be tracked under the requirement ID `REQ-DEMO-0001`.
