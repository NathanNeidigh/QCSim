def toy_sha8_hash(input_key_str):
    """
    Classical version of the 8-bit Shift-XOR Hash.
    Mimics: circuit.cx(key[i], key[i+1])
    """
    # Convert string to list of integers
    x = [int(bit) for bit in input_key_str]
    
    # Replicate the Ripple XOR logic (Forward Hash)
    # Each bit is XORed with the one before it
    for i in range(1, 8):
        x[i] = x[i] ^ x[i-1]

    # Convert back to string
    return "".join(str(bit) for bit in x)

# 1. Create the full mapping
hash_to_key_map = {}

for i in range(256):
    # Create an 8-bit binary string (e.g., "00001010")
    key_str = format(i, '08b')
    # Generate the hash
    hash_str = toy_sha8_hash(key_str)
    # Store it
    hash_to_key_map[hash_str] = key_str

# 2. Sort the hashes numerically to make the table easy to read
sorted_hashes = sorted(hash_to_key_map.keys())

# 3. Print the formatted list
print(f"{'Hash':<8}  | {'Key':<8}")
print("-" * 20)

for h in sorted_hashes:
    print(f"{h} -> {hash_to_key_map[h]}")