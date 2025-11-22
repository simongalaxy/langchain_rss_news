import os
import pprint


# write rss output to a text file under ./data.
def write_rss_to_file(feeds: list[dict]) -> None:
    filename = "rss_data.txt"
    filepath = "data/"
    
    with open(os.path.join(filepath, filename), "w") as f:
        
        f.write(f"Total no of feeds: {len(feeds)}" + "\n")
        f.write(f"Feed dicts:" + "\n")
        
        for i, feed in enumerate(feeds, start=1):
            if i == 1:
                f.write("---------------------------------------------------------------------------" + "\n")
            f.write(f"No.: {i}" + "\n")    
            pprint.pprint(feed, stream=f)
            f.write("-------------------------------------------------------------------------------" + "\n")
     
    return