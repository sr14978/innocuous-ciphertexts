import pyshark
import pickle
from scipy.stats import chisquare
import arguments as args

def main(reset=None, output_file=None):

    args.setup_argument(0, "reset", False)
    args.setup_argument(1, "output", "test_urls")

    if reset == None:
        reset = args.args["reset"]
    if output_file == None:
        output_file = args.args["output"]

    if reset:
        with open(output_file, "wb") as f:
            pickle.dump([], f)

    capture = pyshark.LiveCapture(
        interface="ens33",
        display_filter='http && http.request.method == \
                        "GET" && http.request.uri != "/"'
        )

    sample_size = 100
    steps = 20
    jump = sample_size/steps
    for i in range(steps):
        print("read %i samples"%(i*jump), flush=True)
        capture.sniff(packet_count=jump)
        urls = [p.http.get_field_value("request_uri")[1:] for p in capture]
        with open(output_file, "rb") as f:
            current_urls = pickle.load(f)
        with open(output_file, "wb") as f:
	        pickle.dump(current_urls + urls, f)

    print("read %i samples"%(sample_size))

    capture.close()


if __name__ == "__main__":
    main()
