from flask import Flask, render_template
import speedtest

app = Flask(__name__)

def test_speed():
    # create speedtest object
    st = speedtest.Speedtest()
    
    # get best server
    st.get_best_server()
    
    # perform download and upload speed tests
    download_speed = st.download() / 10**6 # convert to megabits per second
    upload_speed = st.upload() / 10**6 # convert to megabits per second
    ping = st.results.ping
    
    # get client and server information
    server = st.get_best_server()
    server_name = server['name']
    server_country = server['country']
    server_location = f"{server['lat']}, {server['lon']}"
    client_ip = st.results.client['ip']
    
    # return results as dictionary
    return {
        "Server Name": server_name,
        "Server Country": server_country,
        "Server Location": server_location,
        "Client IP Address": client_ip,
        "Ping": f"{ping:.2f} ms",
        "Download Speed": f"{download_speed:.2f} Mbps",
        "Upload Speed": f"{upload_speed:.2f} Mbps",
        "Internet Speed": f"{st.results.download / 10**6:.2f} Mbps / {st.results.upload / 10**6:.2f} Mbps"
    }

@app.route('/')
def home():
    # run speed test and get results
    speedtest_results = test_speed()
    
    # render template with results
    return render_template('index.html', results=speedtest_results)

if __name__ == '__main__':
    app.run(debug=True)

