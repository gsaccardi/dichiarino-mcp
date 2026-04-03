# Check Digit Algorithm - Codice Fiscale

## Odd-position values (positions 1, 3, 5, 7, 9, 11, 13)

| Char | Value | Char | Value | Char | Value |
|------|-------|------|-------|------|-------|
| 0 | 1 | A | 1 | N | 19 |
| 1 | 0 | B | 0 | O | 15 |
| 2 | 5 | C | 5 | P | 3 |
| 3 | 7 | D | 7 | Q | 6 |
| 4 | 9 | E | 9 | R | 2 |
| 5 | 13 | F | 13 | S | 4 |
| 6 | 15 | G | 15 | T | 16 |
| 7 | 17 | H | 17 | U | 10 |
| 8 | 19 | I | 19 | V | 22 |
| 9 | 21 | J | 21 | W | 14 |
| - | - | K | 2 | X | 25 |
| - | - | L | 4 | Y | 24 |
| - | - | M | 18 | Z | 23 |

## Even-position values (positions 0, 2, 4, 6, 8, 10, 12, 14)

Face value: `0→0, 1→1, …, 9→9`, `A→0, B→1, C→2, …, Z→25`

## Check digit formula

```python
total = sum(odd_value[cf[i]] for i in odd_positions) \
      + sum(even_value[cf[i]] for i in even_positions)
check_char = chr(ord('A') + (total % 26))
```

Valid CF: `cf[15] == check_char`
