__author__ = "Alex Mourtos"
import sys
import argparse
import logging
from morse_dict import MORSE_2_ASCII
from morse_dict import ENG_2_MORSE

# +++ Setting up Logger config +++
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()


def encode_morse(text):
    text_list = text.split(" ")
    result = ""
    for word in text_list:
        for letter in word:
            result += (ENG_2_MORSE.get(letter.upper()))
        result += " "
    return result


def encode_bits(text):
    return


def decode_bits(bits):
    p = 0
    bits_list = []
    result = []

    for i in range(len(bits)):
        if bits[i] != bits[i-1]:
            bits_list.append(bits[p:i])
            p = i
        if i == len(bits)-1:
            bits_list.append(bits[p:])
    time_unit = min(len(string) for string in bits_list)
    for _, string in enumerate(bits_list):
        if "1" in string:
            if len(string) // time_unit == 3:
                result.append("-")
            if len(string) // time_unit == 1:
                result.append(".")
        elif "0" in string:
            if len(string) // time_unit == 3:
                result.append(" ")
            if len(string) // time_unit >= 7:
                result.append("   ")
    result = "".join(result)
    return result


def decode_morse(morse):
    message = ""
    morse_list = morse.split(" ")
    for i, letter in enumerate(morse_list):
        if i + 2 <= len(morse_list):
            if morse_list[i] == "" and morse_list[i + 1] == "":
                continue
        if MORSE_2_ASCII.get(letter) is None:
            message += " "
            continue
        message += MORSE_2_ASCII.get(letter)
    result = message.strip()
    return result


def options():
    decode_options = ["decode", "Decode"]
    encode_options = ["encode", "Encode"]
    morse_options = ["Morse", "morse"]
    bits_options = ["Bits", "bits"]

    try:
        decode_or_encode = input("Decode or Encode?: ")
        # decore or encode
        if (decode_or_encode not in decode_options
                and decode_or_encode not in encode_options):
            print("Please select a valid option")
        # if decode
        if decode_or_encode in decode_options:
            morse_or_bits = input("Are we decoding Morse or Bits?\n")

            if (morse_or_bits not in morse_options
                    and morse_or_bits not in bits_options):
                print("Please select valid option")
            # if morse
            if morse_or_bits in morse_options:
                morse = input("Please enter valid morse code to decode:\n")
                print("Input:  ", morse)
                print("Decoded:  ", decode_morse(morse))
            # if bits
            if morse_or_bits in bits_options:
                bits = input("Please enter valid bits to decode:\n")
                print("Input:  ", bits)
                print("Decoded:  ", decode_morse(decode_bits(bits)))

        # if encode
        if decode_or_encode in encode_options:
            morse_or_bits = input("Are we encoding Morse or Bits?\n")

            if (morse_or_bits not in morse_options
                    and morse_or_bits not in bits_options):
                print("Please select a valid option")

            # if morse
            if morse_or_bits in morse_options:
                text = input("Please enter text to encode to morse:\n")
                print("Input:   ", text)
                print("Encoded:   \n", encode_morse(text))

            # if bits
            if morse_or_bits in morse_options:
                text = input("Please enter text to encode to bits:\n")
                print("Input:   \n", text)
                print("Encoded:   \n", encode_bits(text))
    except Exception as e:
        print(e)


def main(args):
    print("Please select your desired function")
    options()

    return


if __name__ == "__main__":
    main(sys.argv[1:])
