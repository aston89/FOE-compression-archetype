import sys
from encoder_foe import compress_to_foe
from decoder_foe import decompress_foe_file

def main():
    if len(sys.argv) < 5:
        print("Usage:")
        print("  compress input.bin output.foe dict.json")
        print("  decompress input.foe output.bin dict.json")
        return

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    dict_file = sys.argv[4]

    if mode == "compress":
        compress_to_foe(input_file, dict_file, output_file)
    elif mode == "decompress":
        decompress_foe_file(input_file, dict_file, output_file)
    else:
        print("Unknown mode. Use compress or decompress.")

if __name__ == "__main__":
    main()
