
import requests
import base64
import time
def post_test():
    with open("./test.png", "rb") as f:
        image_bytes = f.read()

    url = "https://lismin.online:23333/search"

    data = {
        "image": base64.b64encode(image_bytes).decode("utf-8")
    }
    st = time.time()
    resp = requests.post(url, json=data).json()
    print(resp)
    # with open("./result.jpg", "wb") as f:
    #     f.write(base64.b64decode(resp["image"]))
    print(time.time()-st)

if __name__ == "__main__":
    post_test()