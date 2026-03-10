def toy_sha4_hash(input_key_str):
    """
    Classical version of the Shift-XOR Hash used in the 4-bit Quantum Oracle.
    """
    # 1. Convert string "0110" to list of bits [0, 1, 1, 0]
    x = [int(bit) for bit in input_key_str]
    
    if len(x) != 4:
        raise ValueError("Input must be exactly 4 bits long.")

    # 2. Replicate the Forward Hash (Block B)
    # circuit.cx(key[0], key[1]) -> x[1] = x[1] ^ x[0]
    x[1] = x[1] ^ x[0]
    
    # circuit.cx(key[1], key[2]) -> x[2] = x[2] ^ x[1]
    x[2] = x[2] ^ x[1]
    
    # circuit.cx(key[2], key[3]) -> x[3] = x[3] ^ x[2]
    x[3] = x[3] ^ x[2]

    # 3. Convert back to string
    result_hash = "".join(str(bit) for bit in x)
    return result_hash

print(f"{'Key (Input)':<12} | {'Hash (Output)':<12}")
print("-" * 28)

# Loop through all numbers from 0 to 15 (0000 to 1111)
for i in range(16):
    # Format the number as a 4-bit binary string
    candidate = format(i, '04b')
    h = toy_sha4_hash(candidate)
    
    # Highlight our specific target from the Quantum script
    if candidate == "0110":
        print(f"{candidate:<12} | {h:<12} <--- TARGET")
    else:
        print(f"{candidate:<12} | {h:<12}")