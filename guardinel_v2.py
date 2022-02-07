if __name__ == '__main__':
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    config, entity = parse_args(argumentList)

    executor = ConcurrentExecutor(config, entity)
    results = executor.start()
    __logger.debug(__tag, 'results: {}'.format(results))

    if pr_needs_block(results):
        exit(1)