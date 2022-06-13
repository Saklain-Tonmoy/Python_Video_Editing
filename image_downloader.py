import requests
import os
from datetime import datetime


class ImageDownloader:

    def __init__(self):
        self.image_urls = [
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217633.jpg?k=c41f57f6f62348f6f597b1f7553f340dbede523fbfeac3b818750f82c7c856a6&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/142082178.jpg?k=d8e4cf353805656df8f21369319542fd927e0d7c1abcf80cc6f65aa5806d6a83&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74216383.jpg?k=67f87d3ba00b0c722b72ccb210f6261eee1bc1a81aef6be291ddfb225b1749d9&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74216395.jpg?k=27fea14d4a0387bb4ab02927c123371966f6de2db9b5b2ee6169a4d9fe8f4bff&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74216725.jpg?k=4bf70ef4920b15729281d700eb8774563b46939332b482a6ee448ce4a8cf96ca&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217454.jpg?k=33a591df058c71337a2eb0c8d529510423c204e8f760544964e0ac638a1bc02c&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217583.jpg?k=630ef0cf5f3f89a075f7ffceaf4e52618fd635a06e4a361b106217b89732e1f9&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217291.jpg?k=4d017fc01076be1dfb1e7c3bdab810cceaa36ed6986f4484bbe1dcbd597781f3&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217364.jpg?k=6c7c0a9449070a848f86682d21a7460b991ba91b5d1a55087866e8ab03b48bf7&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217278.jpg?k=c6ccb8ba8b1b0e1665b8c0c01dbad7e80d7b9a1180b70de98429dda4776db4f9&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217288.jpg?k=a0fc6aa2b497def40afc89b0d9f0416aa95b67c08290f2d9fa1e1327d843c263&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217298.jpg?k=41f163859cae0771a5f948c47146cc373c7d33aeb522591571279bdb368ac6dd&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217366.jpg?k=66ab2178330e5c609601b906b2f88a274aa6e43ea6409228ae304d630af6c0b6&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217375.jpg?k=77a36bf929361cdf05ed87e71964dedd2e510939566e4aad057b4bba24521a33&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217422.jpg?k=00e32bae9c680c35188bf553c2c51222a18bbbf7aac957165d701e2551713a0f&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217436.jpg?k=76fa004734583d10afe688fca9f10341407796d747c4882ef9541097b7bb0a23&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217453.jpg?k=7377ebcbe7b7a0f612a4cba8c5bd9bb565809824d379018388f95b5d5e0ac45f&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217466.jpg?k=41442ac4f8d98d9148d9887ff24b752330768539b316278cd98859e8cdf1d272&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217504.jpg?k=08790e8c0fb59033b242a8783d9b4a4495e77d183920e7d2a0d0059bcff2845f&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217512.jpg?k=afafafb6485e1755fd5446103f43b3c7e617c0fb57e79ffa07ca1dfd3149dc58&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74217551.jpg?k=72b0196abd9c595f59fbb94bada3980e5fd000ee8838f35e69584c07170c67ae&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74222397.jpg?k=293ad654573d9a3ffc9c73989cc5dca366c91a8627b4e30c08ba2a6b3e0b9224&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74223457.jpg?k=664f65debcc55f871bf18e9b3e801035c3c8356993c0c6d78b632d71d7ec328b&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74669296.jpg?k=de5d8f856f9432fc8b47bece9d084927b1dfbd07d98c0db65e8749bfc235716b&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74672630.jpg?k=a9d150f22109c313bbf5a1538f4d462cc0dc41440fad3759cc4ddb5110be490a&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74672641.jpg?k=0e155a697faca9b7a1735cc5e35675cc14acf145ba1101ac381e334d170acf42&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/74672663.jpg?k=5d20720c782b6ad3bad1289abb3aa8f13c1b8133769d3f9c620435131270cf82&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/76354353.jpg?k=65ce20e30f7bdf9d262e3869996efcead7f5f2541841bdb49081d27a3278bac2&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/77073641.jpg?k=71f7718091c8f7a1b20bde3ed33760135f5e3c2113c8050adbae0093fa78be0c&o=",
            "https://q-xx.bstatic.com/xdata/images/hotel/max500/356082064.jpg?k=ff25e95a305ff66a40b579cb48c5cee3cc0405ab48342277ff9fc2bf15ab6233&o="
        ]

    def download_image(self):

        print("#######################################\n")
        print("          Downloading Images          ")
        print("#######################################\n")

        start_time = datetime.now().replace(microsecond=0)
        print(f"Start Time: {str(start_time)}")

        image_folder = os.getcwd() + "/images"

        if not os.path.exists(image_folder):
            os.mkdir(os.getcwd() + '/images')

        for index, url in enumerate(self.image_urls):
            url = url.replace('max500', 'max3000')
            response = requests.get(url)
            with open(f"{image_folder}/image_{index}.jpg", "wb") as image:
                image.write(response.content)

        end_time = datetime.now().replace(microsecond=0)
        execution_time = (end_time - start_time)
        print(f"End Time: {str(end_time)}")
        print(f"Execution Time: {str(execution_time)}")
