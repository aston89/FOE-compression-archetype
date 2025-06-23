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

def compress_to_foe(input_path, dict_path, output_path, chunk_size=8):
    with open(dict_path, "r") as f:
        foe_dict = json.load(f)
    foe_lookup = {entry["result"]: idx for idx, entry in enumerate(foe_dict)}

    with open(input_path, "rb") as f:
        raw = f.read()

    metadata = {
        "dict": Path(dict_path).name,
        "chunk_size": chunk_size,
        "total_chunks": len(raw) // chunk_size
    }

    header = b"FOE\x01"
    meta_bytes = json.dumps(metadata).encode("utf-8")
    foe_data = bytearray()
    foe_data.extend(struct.pack(">I", len(meta_bytes)))
    foe_data.extend(meta_bytes)

    for i in range(0, len(raw) - chunk_size + 1, chunk_size):
        chunk = raw[i:i + chunk_size]
        val = int.from_bytes(chunk, byteorder="big")
        if val in foe_lookup:
            foe_data.append(foe_lookup[val])
        else:
            foe_data.append(0xFF)
            foe_data.extend(chunk)

    with open(output_path, "wb") as out:
        out.write(header)
        out.write(foe_data)
