import client_overlay
import sys

def main():
    client_overlay.start()


# def old_main():
    # window_thread = threading.Thread(target=client_overlay.start)
    # window_thread.start()

    # time.sleep(1)
    # total_assault_helper_thread = threading.Thread(target=total_assault_helper.start)
    # total_assault_helper_thread.start()


if __name__ == '__main__':
    main()
