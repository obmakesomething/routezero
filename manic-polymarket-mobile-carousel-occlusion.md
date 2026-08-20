# Manic Polymarket mobile carousel edge occlusion

## Summary

On the public Manic Polymarket surface, fixed trailing controls on the mobile category and sort carousels overlap labels and pointer hit areas of scrollable items that pass beneath them.

A trusted touch swipe successfully moves the carousel, but it does not eliminate the collision; the overlap shifts to another item at the carousel edge.

## Reproduction scope

Observed on Chromium mobile emulation with an iPhone-style user agent at:

- 360×844
- 375×844
- 390×844
- 412×844
- 430×844

Touch gestures were dispatched as trusted Chrome DevTools Protocol touch events.

## Result

- Category carousel scroll succeeded: 5/5 profiles.
- Sort carousel scroll succeeded: 5/5 profiles.
- The originally obscured item recovered after a swipe: 5/5 profiles.
- Category-edge occlusion remained after the swipe: 5/5 profiles.
- Sort-edge occlusion remained after the swipe: 5/5 profiles.

At 390px, the initially affected `Economy` and `Newest` controls recover after swiping, while the collision moves to other items such as `Politics` / `Weather` and `Competitive`.

## Expected

Scrollable filter items should remain visually legible and pointer-accessible throughout the horizontal scroll range. Fixed controls should reserve enough inset space that carousel items do not pass underneath their interactive hit areas.

## Suggested correction

Reserve leading/trailing scroll insets equal to the fixed controls' occupied widths, or move the fixed controls outside the scroll viewport. A visual gradient alone is insufficient because the problem includes hit-target occlusion.

## Evidence boundary

This report is limited to the reproduced Chromium mobile responsive behavior. Physical iPhone Safari was not evaluated.

No login, OAuth, wallet connection, signature, trade, order, deposit, withdrawal, or funds action was used to reproduce this issue.

The full screenshot evidence and reproduction packet were submitted through the official Manic Typeform on 2026-08-20 and transmitted to Manic support.
