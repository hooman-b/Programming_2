import requests
import asyncio


class NetworkClient:
    # delay for a specific seconds 
    async def delay_maker(self, seconds):
        await asyncio.sleep(seconds)

    #get data from server
    async def get_data(self, url):
        service_response = requests.get(url)
        if service_response.status_code == 200:
            print(service_response.text)
        else:
            print(f"failed with error: {service_response.status_code}")

    async def main(self):
        task_list = [
            self.delay_maker(2),
            self.get_data('http://localhost:9000/Data/2000'),
            self.delay_maker(3),
            self.get_data('http://localhost:9000/Data/1890'),
            self.delay_maker(2),
            self.get_data('http://localhost:9000/Data/2001/2003'),
        ]
        await asyncio.gather(*task_list)

if __name__ == '__main__':
    asyncio.run(NetworkClient().main())