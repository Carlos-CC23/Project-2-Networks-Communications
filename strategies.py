def nrz_encode(data: str) -> str: 
    """
    NRZ encoding: map '1' -> 'H' and '0' -> 'L'
    """
    encoded = ''.join('H' if bit == '1' else 'L' for bit in data)
    return encoded

def nrz_decode(encoded: str) -> str:
    """
    NRZ decoding: reverse the mapping 'H' -> '1' and 'L' -> '0'
    """
    decoded = ''.join('1' if signal == 'H' else '0' for signal in encoded)
    return decoded

def nrzi_encode(data: str, initial: str = 'L') -> str:
    """
    NRZI encoding:
    - Start with an initial signal level (default 'L').
    - For each bit:
        If the bit is '1', change (invert) the signal.
        If the bit is '0', keep the signal unchanged.
    """
    current = initial
    encoded = current  # include initial state as first transmitted signal
    for bit in data:
        if bit == '1':
            # Transition: change the signal level
            current = 'H' if current == 'L' else 'L'
        # For '0', current remains unchanged
        encoded += current
    return encoded

def nrzi_decode(encoded: str) -> str:
    """
    NRZI decoding:
    - The first signal is the known initial state.
    - For every subsequent signal:
        If it is different from the previous signal, output '1'
        Otherwise, output '0'
    """
    if not encoded:
        return ""
    decoded = ""
    previous = encoded[0]
    for current in encoded[1:]:
        if current != previous:
            decoded += '1'
        else:
            decoded += '0'
        previous = current
    return decoded

def manchester_encode(data: str) -> str:
    """
    Manchester encoding:
    For each bit:
      - '0' is encoded as 'L' followed by 'H' (low-to-high)
      - '1' is encoded as 'H' followed by 'L' (high-to-low)
    The encoded string will have twice the length of the input data.
    """
    encoded = ""
    for bit in data:
        if bit == '0':
            encoded += "LH"
        elif bit == '1':
            encoded += "HL"
        else:
            raise ValueError("Data should contain only '0' or '1'")
    return encoded

def manchester_decode(encoded: str) -> str:
    """
    Manchester decoding:
    The encoded string should have even length.
    Each pair is decoded:
      - "LH" -> '0'
      - "HL" -> '1'
    """
    if len(encoded) % 2 != 0:
        raise ValueError("Manchester encoded data length should be even")
    
    decoded = ""
    for i in range(0, len(encoded), 2):
        pair = encoded[i:i+2]
        if pair == "LH":
            decoded += '0'
        elif pair == "HL":
            decoded += '1'
        else:
            raise ValueError(f"Invalid Manchester encoding pair: {pair}")
    return decoded


# --- Example Usage and Testing ---

if __name__ == "__main__":
    # Sample binary data
    data = "1011001"
    print("Original data:     ", data)
    
    # NRZ
    nrz_enc = nrz_encode(data)
    nrz_dec = nrz_decode(nrz_enc)
    print("\nNRZ Encoding:")
    print("Encoded signal:    ", nrz_enc)
    print("Decoded data:      ", nrz_dec)
    
    # NRZI
    nrzi_enc = nrzi_encode(data, initial='L')
    nrzi_dec = nrzi_decode(nrzi_enc)
    print("\nNRZI Encoding (initial state 'L'):")
    print("Encoded signal:    ", nrzi_enc)
    print("Decoded data:      ", nrzi_dec)
    
    # Manchester
    manchester_enc = manchester_encode(data)
    manchester_dec = manchester_decode(manchester_enc)
    print("\nManchester Encoding:")
    print("Encoded signal:    ", manchester_enc)
    print("Decoded data:      ", manchester_dec)
