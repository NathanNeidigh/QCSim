def hex_to_17bit_binary(sign, hex_val):
    """
    Converts a +/- sign and 4-digit hex to a 17-bit binary string.
    The hex is converted to 16-bit 2's complement.
    """
    # Convert Hex to integer
    val = int(hex_val, 16)
    
    # Handle 16-bit 2's complement logic for the Hex part
    binary_16 = format(val & 0xFFFF, '016b')
    
    # Add the 17th bit based on the sign (+ is 0, - is 1)
    sign_bit = "0" if sign == "+" else "1"
    
    return sign_bit + binary_16

def sha17_nonlinear(key_string):
    # 17-bit Non-Linear Ripple-AND Hash
    bits = [int(b) for b in key_string]
    hash_result = [0] * 17
    hash_result[0] = bits[0]
    hash_result[1] = bits[1] ^ hash_result[0]

    for i in range(2, 17):
        non_linear_term = hash_result[i-1] & hash_result[i-2]
        hash_result[i] = bits[i] ^ non_linear_term

    return "".join(str(b) for b in hash_result)

# ADD INPUT DATA HERE
input_sign = "-"
input_hex = "6273" # 4-digit hex

# Step 1: Encode
binary_key = hex_to_17bit_binary(input_sign, input_hex)

# Step 2: Hash
final_hash = sha17_nonlinear(binary_key)

print(f"\n\nSigned 4-value hex encoder")
print(f"Input:        {input_sign}{input_hex}")
print(f"Encoded Key:  {binary_key} (17 bits)")
print(f"Final Hash:   {final_hash}\n\n")