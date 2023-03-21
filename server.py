def main(*args):
    args = args[0]

    from junc_protocol.jp import JP
    
    protocol = JP(port=5050, msize=4096)
    protocol.main_loop()









if __name__ == "__main__":
    from sys import argv
    main(argv[1:])