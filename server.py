# Name: Ari Zeto
# ONID: Zetoa@oregonstate.edu

# Microservice: Sends a pie chart containing data for how well a user did in partners project.

# Necessary imports.
import socket # Communication pipeline
import matplotlib.pyplot as plot # Graphing library
import io # Necessary for base64 conversion.
import base64 # Necessary for encoding and decoding


def make_chart(scores_string):
    """
    This function creates and returns a pie chart based on a string provided from the client.
    Takes parameter 'scores_string' (string). String is numbers correct and number of answers wrong separated by spaces.
    Ex: 2 (multiplication), 3 (addition), 2 (subtraction), 5 (wrong answers).
    Returns a pie chart to the client.
    """
    results_chart = [int(char) for char in scores_string.split() if char.isdigit()] # Array containing data per subject area and wrong answers.
    labels_chart = 'Addition', 'Subtraction', 'Multiplication', 'Wrong Answers'     # Design Pie Chart
    # Display results.
    pie_chart, pie_data = plot.subplots()
    pie_data.pie(results_chart, labels=labels_chart, autopct='%1.1f%%', shadow=True, startangle=90)
    pie_data.axis('equal')
    # Returns pie chart (encoded with base64) to client.
    return fig_to_base64(pie_chart)


def fig_to_base64(fig):
    """
    This method converts the image to base64.
    Takes parameter 'fig' - the figure that is returned from 'plot.subplots' from the function, make_chart().
    Returns an encoded image of the pie chart.
    """
    my_img = io.BytesIO()
    fig.savefig(my_img, format='png', bbox_inches='tight')
    my_img.seek(0)
    return base64.b64encode(my_img.getvalue())

# Initialize data for socket communication.
HOST = "127.0.0.1"
PORT = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Waiting for Client...")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print("Sending Results Chart...")
                encoded_pie_chart = make_chart(data)
                fh = open('text', 'wb')
                fh.write(encoded_pie_chart)
                fh.close()
                fh = open("text", "rb")
                str1 = fh.read()
                conn.sendall(str1)
            except socket.error:
                print("Error occurred")
                break