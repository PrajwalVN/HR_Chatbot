import subprocess
import threading

# Function to run the Rasa server
def run_rasa_server():
    subprocess.call(["rasa", "run", "--enable-api", "--cors", "*", "--port", "10000"])

# Function to run the Action server
def run_action_server():
    subprocess.call(["rasa", "run", "actions", "--port", "5055"])

# Run both servers in separate threads
if __name__ == "__main__":
    rasa_thread = threading.Thread(target=run_rasa_server)
    action_thread = threading.Thread(target=run_action_server)

    rasa_thread.start()
    action_thread.start()

    rasa_thread.join()
    action_thread.join()
