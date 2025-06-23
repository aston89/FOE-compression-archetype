import json
import struct

def eval_opcode_stack(ops):
    stack = []
    i = 0
    while i < len(ops):
        op = ops[i]
        if op == 0x10:
            i += 1
            stack.append(ops[i])
        elif op == 0x01:
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        elif op == 0x02:
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif op == 0x03:
            b, a = stack.pop(), stack.pop()
            stack.append(a << b)
        elif op == 0x04:
            b, a = stack.pop(), stack.pop()
            stack.append(a ^ b)
        elif op == 0x05:
            b, a = stack.pop(), stack.pop()
            stack.append(a % b if b != 0 else 0)
        elif op == 0xF0 or op == 0xFE:
            break
        i += 1
    return stack[0] if len(stack) == 1 else None

def decompress_foe_file(foe_path, dict_path, output_path):
    with open(dict_path, "r") as f:
        foe_dict = json.load(f)
    formula_lookup = {i: entry["formula"] for i, entry in enumerate(foe_dict)}

    with open(foe_path, "rb") as f:
        magic = f.read(4)
        if magic != b"FOE\x01":
            raise ValueError("Not a FOE v1 file.")
        meta_len = struct.unpack(">I", f.read(4))[0]
        meta = json.loads(f.read(meta_len))
        chunk_size = meta["chunk_size"]
        rest = f.read()

    output = bytearray()
    i = 0
    while i < len(rest):
        flag = rest[i]
        if flag == 0xFF:
            output.extend(rest[i+1:i+1+chunk_size])
            i += 1 + chunk_size
        else:
            formula = formula_lookup.get(flag)
            if formula:
                val = eval_opcode_stack(formula)
                output.extend(val.to_bytes(chunk_size, byteorder="big"))
            i += 1

    with open(output_path, "wb") as out:
        out.write(output)
