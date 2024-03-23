import client_overlay
import threading
import time
import total_assault_helper

def main():
    window_thread = threading.Thread(target=client_overlay.start)
    window_thread.start()

    time.sleep(1)

    total_assault_helper.start(client_overlay.update_display, client_overlay.update_progress_bar)
    # total_assault_helper_thread = threading.Thread(target=total_assault_helper.start)
    # total_assault_helper_thread.start()


if __name__ == '__main__':
    main()
