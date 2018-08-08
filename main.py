from market import Market

if __name__ == '__main__':
    m = Market('BTCUSD')
    m.initialize()
    m.create_database()

    while True:
        # Continue streaming data
        m.stream_data()
    
