def toy_sha8_nonlinear(key_string):
    """
    Encrypts an 8-bit string using a non-linear Ripple-XOR + AND logic.
    Logic: H[i] = K[i] ^ (H[i-1] AND H[i-2])
    """
    # Convert string '0110...' to a list of integers [0, 1, 1, 0...]
    bits = [int(b) for b in key_string]
    hash_result = [0] * 8

    # 1. Bit 0 is the anchor (Direct copy)
    hash_result[0] = bits[0]

    # 2. Bit 1 is linear (XOR with previous bit result)
    hash_result[1] = bits[1] ^ hash_result[0]

    # 3. Bits 2 through 7 are NON-LINEAR
    # Each bit is XORed with the 'AND' of the two previous results
    for i in range(2, 8):
        # The Non-Linear 'CCX' logic
        non_linear_term = hash_result[i-1] & hash_result[i-2]
        hash_result[i] = bits[i] ^ non_linear_term

    # Convert back to a string for easy reading
    return "".join(str(b) for b in hash_result)

# --- TEST CASE ---
test_key = "01100101"
result_hash = toy_sha8_nonlinear(test_key)

print(f"Classical Non-Linear Encryption")
print(f"-------------------------------")
print(f"Input Key:  {test_key}")
print(f"Output Hash: {result_hash}")

print(f"\nVerification Table (First 10 entries):")
print(f"Key      | Non-Linear Hash")
print(f"--------------------------")
for i in range(256):
    key = format(i, '08b')
    print(f"{key} -> {toy_sha8_nonlinear(key)}")