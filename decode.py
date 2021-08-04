__author__ = "Alex Mourtos"
import sys
import argparse
import logging
import signal
import time
import os
from morse_dict import MORSE_2_ASCII
from morse_dict import ENG_2_MORSE
from datetime import datetime

# +++ Setting up Logger config +++
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()


# +++ ------------------------------------------------------------------- +++
# functions to set banners and timers for uptime
def start_banner():
    file = __file__.split("/")[-1]
    start_time = datetime.now()
    start_banner = (
        "\n" +
        "-" * 80 +
        f"\n\tRunning {file}" +
        f"\n\tStarted on {start_time.isoformat()}\n" +
        "-" * 80 +
        "\n" +
        str(os.getpid())
    )
    logger.info(start_banner)
    return start_time


def end_banner(start_time):
    file = __file__.split("/")[-1]
    up_time = datetime.now() - start_time
    end_banner = (
        "\n" +
        "-" * 80 +
        f"\n\tStopping {file}" +
        f"\n\tUptime was {up_time}\n" +
        "-" * 80
    )
    logger.info(end_banner)
    return

# +++ ------------------------------------------------------------------- +++
exit_flag = False


def encode_morse(text):
    text_list = text.split(" ")
    result = ""
    for word in text_list:
        for letter in word:
            result += ENG_2_MORSE.get(letter.upper()) + " "
        result += "   "
    return result


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
    global exit_flag
    decode_options = ["decode", "Decode"]
    encode_options = ["encode", "Encode"]
    morse_options = ["Morse", "morse"]
    bits_options = ["Bits", "bits"]

    decode_or_encode = input("Decode or Encode?: ")
        # decode or encode
    if (decode_or_encode not in decode_options
            and decode_or_encode not in encode_options):
        print("Please select a valid option")
        exit_flag = True
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
            # enter text to encode
            text = input("Please enter text to encode to morse:\n")
            print("Input:   ", text)
            print("Encoded:   \n", encode_morse(text))
    else:
            print("Please select a valid option")

    return

def signal_handler(sig_num, frame):
    global exit_flag
    """Determines received signals for exiting the program"""
    logger.info('Received ' + signal.Signals(sig_num).name)
    print(sig_num)
    if sig_num == 2:
        logger.info("Program terminated.\n")
        logger.info("Press Enter to exit.")
        exit_flag = True
    if sig_num == 15:
        exit_flag == True
    return


def main(args):
    start = start_banner()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while not exit_flag:
        try:
            print("Please select your desired function")
            options()
        except Exception as e:
            logger.info(e)

    end_banner(start)
    return


if __name__ == "__main__":
    main(sys.argv[1:])
