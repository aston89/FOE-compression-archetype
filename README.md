# FOE: Functional Opcode Encoding

FOE (Functional Opcode Encoding) is a novel compression prototype that represents binary data chunks as stack-based symbolic formulas using a custom bytecode language.

Unlike traditional entropy-based compressors (like LZ77, Huffman, Brotli), FOE attempts to *describe* binary values using simple mathematical expressions encoded in opcodes (e.g., `PUSH`, `MUL`, `ADD`, `SHL`).  
This approach is especially useful for semi-structured or patterned data, such as logs, telemetry, numerical datasets, or static configuration blocks.

---

## Concept Summary

- Binary chunks (e.g. 64-bit) are interpreted as large integers.
- A small virtual machine with a symbolic instruction set (bytecode) is used to generate mathematical expressions.
- If a formula evaluates to a chunk’s value, we store the formula’s ID instead of the raw data.
- A dictionary of formulas acts as the compression vocabulary (shared between encoder and decoder).
- The system is modular and stack-based for minimal runtime cost and compatibility with embedded systems.

---

## Opcode Set (v0.1)

| Opcode | Mnemonic | Action                           |
|--------|----------|----------------------------------|
| `0x10` | `PUSH`   | Push a 1-byte literal to stack   |
| `0x01` | `MUL`    | Multiply top two stack values    |
| `0x02` | `ADD`    | Add top two stack values         |
| `0x03` | `SHL`    | Bitwise left shift               |
| `0x04` | `XOR`    | Bitwise XOR                      |
| `0x05` | `MOD`    | Modulo                           |
| `0xF0` | `REF`    | Reference a precomputed formula  |
| `0xFE` | `END`    | End of formula                   |

Example:
```hex
0x10 0x06   # PUSH 6  
0x10 0x09   # PUSH 9  
0x01        # MUL  
0x10 0x03   # PUSH 3  
0x02        # ADD  
0xFE        # END  

---

## Compression Workflow:
Split binary data into fixed-length chunks (e.g., 64-bit).
For each chunk, calculate its integer representation.
Try to match this value using a formula from the dictionary.
If found, store its ID (e.g. 2 bytes)
Else, store the raw data with a marker flag (e.g. 9 bytes)
Total file size = matched formulas + unmatched raw chunks.

---

## Test Results:
File Type	Match Rate	Compression Gain
Structured BIN	~20%	~5–12%
Randomized BIN	<1%	Negative
The current prototype uses a dictionary with ~400 formulas like PUSH a, PUSH b, OP, END.
Larger dictionaries (and recursive formulas) improve match rate but increase dictionary size.

---

## Why?
Traditional compression relies on symbol frequency and entropy modeling. FOE proposes a different perspective:
If a value is mathematically expressible with low cost (few opcodes), then that expression is a form of compression.

It doesn’t replace LZ or Brotli — it complements them.

---

## Usage example:

python foe_cli.py compress input.bin output.foe dictionaries/foe_simple.json
python foe_cli.py decompress output.foe restored.bin dictionaries/foe_simple.json

# Contribution :
This is an early research prototype.
The goal is to explore a new philosophy of compression, not to dethrone Brotli !


