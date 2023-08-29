# Good
import requests
import asyncio


class NetworkClient:
    """
    Explanation: A class for managing asynchronous network requests.
    """

    async def delay_maker(self, seconds):
        """
        Explanation: Asynchronously delays the execution by the given number of seconds.
        """
        await asyncio.sleep(seconds)

    async def get_data(self, url):
        """
        Input: url (str): The URL to fetch data from.
        Explanation: Asynchronously retrieves data from a server URL and prints
                     the response or error.
        """
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